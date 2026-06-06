"""SEC Company Facts acquisition and canonical P0 metric normalization."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from typing import Any

import requests

from .metric_normalizer import SOURCE_ALIASES
from .workflow_models import (
    AvailabilityItem,
    AvailabilityStatus,
    FinancialMetrics,
    MetricPeriodRole,
    SourceRef,
    SourceType,
)

SEC_PROVIDER = "sec_company_facts"
SEC_PERIOD_END_TOLERANCE_DAYS = 15
SEC_P0_METRICS = ("revenue", "operating_cash_flow", "capex")
SEC_FORMS = {"10-Q", "10-K", "10-Q/A", "10-K/A"}


@dataclass(frozen=True)
class SecFactValue:
    metric_name: str
    value: float
    tag: str
    unit: str
    start: date | None
    end: date
    filed: date | None
    form: str
    method: str
    accn: str | None = None
    prior_start: date | None = None
    prior_end: date | None = None
    prior_filed: date | None = None
    prior_form: str | None = None
    prior_accn: str | None = None


def fetch_sec_company_facts(
    ticker: str,
    *,
    cik: int | None = None,
    session: requests.Session | None = None,
) -> tuple[dict[str, Any], int]:
    sec_session = session or _sec_session()
    resolved_cik = cik if cik is not None else resolve_cik(ticker, session=sec_session)
    response = sec_session.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{resolved_cik:010d}.json",
        timeout=30,
    )
    response.raise_for_status()
    return response.json(), resolved_cik


def resolve_cik(ticker: str, *, session: requests.Session | None = None) -> int:
    sec_session = session or _sec_session()
    response = sec_session.get("https://www.sec.gov/files/company_tickers.json", timeout=30)
    response.raise_for_status()
    ticker_map = response.json()
    normalized = ticker.upper()
    for entry in ticker_map.values():
        if str(entry.get("ticker", "")).upper() == normalized:
            return int(entry["cik_str"])
    raise ValueError(f"SEC CIK not found for ticker: {ticker}")


def build_sec_company_facts_metrics(
    ticker: str,
    fiscal_period: str,
    *,
    target_period_end_date: date | None,
    facts: dict[str, Any] | None = None,
    cik: int | None = None,
    session: requests.Session | None = None,
) -> FinancialMetrics:
    if target_period_end_date is None:
        return _empty_sec_metrics(
            ticker,
            fiscal_period,
            AvailabilityStatus.PERIOD_UNVERIFIED,
            "target_period_end_date is required to promote SEC Company Facts metrics.",
        )

    resolved_cik = cik
    if facts is None:
        facts, resolved_cik = fetch_sec_company_facts(ticker, cik=cik, session=session)

    selected = {
        metric_name: select_sec_fact_value(
            facts,
            metric_name,
            target_period_end_date=target_period_end_date,
        )
        for metric_name in SEC_P0_METRICS
    }
    source_refs = [
        _sec_source_ref(
            ticker=ticker,
            fiscal_period=fiscal_period,
            cik=resolved_cik,
            value=value,
        )
        for value in selected.values()
        if value is not None
    ]
    availability: list[AvailabilityItem] = []
    for metric_name, value in selected.items():
        if value is None:
            availability.append(
                AvailabilityItem(
                    key=f"sec:{metric_name}",
                    status=AvailabilityStatus.OPTIONAL_MISSING,
                    reason=(
                        f"SEC Company Facts did not provide a verified {metric_name} "
                        f"value for {target_period_end_date.isoformat()}."
                    ),
                    source_type=SourceType.FINANCIAL_API,
                )
            )

    from .preprocessor import build_financial_metrics

    return build_financial_metrics(
        ticker=ticker,
        fiscal_period=fiscal_period,
        target_period_end_date=target_period_end_date,
        revenue=_metric_value(selected["revenue"]),
        operating_cash_flow=_metric_value(selected["operating_cash_flow"]),
        capex=_metric_value(selected["capex"]),
        source_refs=source_refs,
        availability=availability,
    )


def select_sec_fact_value(
    facts: dict[str, Any],
    metric_name: str,
    *,
    target_period_end_date: date,
    tolerance_days: int = SEC_PERIOD_END_TOLERANCE_DAYS,
) -> SecFactValue | None:
    rows = _fact_rows(facts, metric_name)
    candidates = [
        row for row in rows if abs((row["end"] - target_period_end_date).days) <= tolerance_days
    ]
    direct = _select_direct_quarter(candidates, target_period_end_date)
    if direct is not None:
        return _row_value(metric_name, direct, "direct_quarter")
    ytd = _select_ytd_difference(rows, candidates, target_period_end_date)
    if ytd is not None:
        current, prior = ytd
        value = float(current["value"]) - float(prior["value"])
        return _row_value(metric_name, current, "ytd_difference", value=value, prior=prior)
    return None


def _metric_value(value: SecFactValue | None) -> float | None:
    if value is None:
        return None
    if value.metric_name == "capex":
        return -abs(float(value.value))
    return float(value.value)


def _fact_rows(facts: dict[str, Any], metric_name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in SOURCE_ALIASES.get("sec", {}).get(metric_name, ()):
        fact = us_gaap.get(tag)
        if not fact:
            continue
        for unit, unit_rows in fact.get("units", {}).items():
            if not str(unit).upper().startswith("USD"):
                continue
            for raw in unit_rows:
                if raw.get("form") not in SEC_FORMS:
                    continue
                end = _parse_date(raw.get("end"))
                if end is None or raw.get("val") is None:
                    continue
                start = _parse_date(raw.get("start"))
                filed = _parse_date(raw.get("filed"))
                duration = (end - start).days if start is not None else None
                rows.append(
                    {
                        "tag": tag,
                        "unit": unit,
                        "value": float(raw["val"]),
                        "start": start,
                        "end": end,
                        "filed": filed,
                        "duration": duration,
                        "form": str(raw["form"]),
                        "accn": str(raw.get("accn") or ""),
                    }
                )
    return rows


def _select_direct_quarter(
    rows: list[dict[str, Any]],
    target_period_end_date: date,
) -> dict[str, Any] | None:
    direct = [row for row in rows if _is_quarter_duration(row.get("duration"))]
    if not direct:
        return None
    return sorted(direct, key=lambda row: _candidate_sort_key(row, target_period_end_date))[0]


def _select_ytd_difference(
    all_rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    target_period_end_date: date,
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    ytd_candidates = [
        row
        for row in candidates
        if row.get("start") is not None
        and row.get("duration") is not None
        and int(row["duration"]) > 110
    ]
    for current in sorted(
        ytd_candidates,
        key=lambda row: _candidate_sort_key(row, target_period_end_date),
    ):
        priors = [
            row
            for row in all_rows
            if row["tag"] == current["tag"]
            and row["unit"] == current["unit"]
            and row["start"] == current["start"]
            and row["end"] < current["end"]
            and row.get("duration") is not None
            and int(row["duration"]) < int(current["duration"])
            and _is_immediate_ytd_prior(current, row)
        ]
        if priors:
            return current, sorted(priors, key=_row_sort_key, reverse=True)[0]
    return None


def _row_value(
    metric_name: str,
    row: dict[str, Any],
    method: str,
    *,
    value: float | None = None,
    prior: dict[str, Any] | None = None,
) -> SecFactValue:
    return SecFactValue(
        metric_name=metric_name,
        value=float(row["value"] if value is None else value),
        tag=str(row["tag"]),
        unit=str(row["unit"]),
        start=row.get("start"),
        end=row["end"],
        filed=row.get("filed"),
        form=str(row["form"]),
        method=method,
        accn=str(row.get("accn") or "") or None,
        prior_start=prior.get("start") if prior else None,
        prior_end=prior.get("end") if prior else None,
        prior_filed=prior.get("filed") if prior else None,
        prior_form=str(prior.get("form")) if prior else None,
        prior_accn=(str(prior.get("accn") or "") or None) if prior else None,
    )


def _sec_source_ref(
    *,
    ticker: str,
    fiscal_period: str,
    cik: int | None,
    value: SecFactValue,
) -> SourceRef:
    cik_part = f":{cik:010d}" if cik is not None else ""
    title_parts = [
        f"SEC Company Facts {value.tag}",
        f"method={value.method}",
        f"form={value.form}",
        f"end={value.end.isoformat()}",
    ]
    if value.accn:
        title_parts.append(f"accn={value.accn}")
    if value.prior_end is not None:
        title_parts.append(f"prior_end={value.prior_end.isoformat()}")
    if value.prior_accn:
        title_parts.append(f"prior_accn={value.prior_accn}")
    return SourceRef(
        source_id=f"financial_api:{ticker.upper()}:{fiscal_period}:sec{cik_part}:{value.metric_name}",
        source_type=SourceType.FINANCIAL_API,
        metric_name=value.metric_name,
        title=" ".join(title_parts),
        reported_period=fiscal_period,
        provider=SEC_PROVIDER,
        provider_column_date=value.end,
        as_of_date=value.filed,
        period_role=MetricPeriodRole.ACTUAL,
    )


def _empty_sec_metrics(
    ticker: str,
    fiscal_period: str,
    status: AvailabilityStatus,
    reason: str,
) -> FinancialMetrics:
    from .preprocessor import build_financial_metrics

    return build_financial_metrics(
        ticker=ticker,
        fiscal_period=fiscal_period,
        availability=[
            AvailabilityItem(
                key=f"sec:{metric_name}",
                status=status,
                reason=reason,
                source_type=SourceType.FINANCIAL_API,
            )
            for metric_name in SEC_P0_METRICS
        ],
        source_refs=[],
    )


def _parse_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _is_quarter_duration(duration: Any) -> bool:
    return duration is not None and 70 <= int(duration) <= 110


def _is_immediate_ytd_prior(current: dict[str, Any], prior: dict[str, Any]) -> bool:
    current_duration = current.get("duration")
    prior_duration = prior.get("duration")
    if current_duration is None or prior_duration is None:
        return False
    duration_gap = int(current_duration) - int(prior_duration)
    end_gap = (current["end"] - prior["end"]).days
    return _is_quarter_duration(duration_gap) and _is_quarter_duration(end_gap)


def _row_sort_key(row: dict[str, Any]) -> tuple[str, str, date]:
    filed = row.get("filed") or date.min
    return (str(row.get("end") or ""), str(row.get("accn") or ""), filed)


def _candidate_sort_key(row: dict[str, Any], target_period_end_date: date) -> tuple[int, int, str]:
    filed = row.get("filed") or date.min
    return (
        abs((row["end"] - target_period_end_date).days),
        -filed.toordinal(),
        str(row.get("accn") or ""),
    )


def _sec_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": os.getenv(
                "SEC_USER_AGENT",
                "earnings-debate-agent contact@example.com",
            ),
            "Accept": "application/json",
        }
    )
    return session
