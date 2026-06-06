"""Central registry for agent-facing expected financial metrics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .workflow_models import (
    AgentRole,
    AvailabilityItem,
    AvailabilityStatus,
    FinancialMetrics,
    MetricPeriodRole,
    SourceType,
)


class MetricRequirement(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    REFERENCE_ONLY = "reference_only"
    NOT_IN_CONTRACT = "not_in_contract"


class MetricSourcePolicy(str, Enum):
    CANONICAL = "canonical"
    CONSENSUS = "consensus"
    DERIVED = "derived"
    PRESENTATION_REFERENCE = "presentation_reference"
    DOCUMENT_TEXT = "document_text"


@dataclass(frozen=True)
class ExpectedMetricSpec:
    metric_key: str
    roles: tuple[AgentRole, ...]
    requirement: MetricRequirement
    source_policy: MetricSourcePolicy
    preferred_sources: tuple[str, ...]
    period_role: MetricPeriodRole
    cap_if_missing: bool = False
    source_type: SourceType = SourceType.FINANCIAL_API
    sec_tags: tuple[str, ...] = ()
    description: str = ""

    def for_context(self) -> dict[str, Any]:
        return {
            "metric_key": self.metric_key,
            "requirement": self.requirement.value,
            "source_policy": self.source_policy.value,
            "preferred_sources": list(self.preferred_sources),
            "period_role": self.period_role.value,
            "cap_if_missing": self.cap_if_missing,
            "source_type": self.source_type.value,
            "sec_tags": list(self.sec_tags),
            "description": self.description,
        }


EXPECTED_METRICS: tuple[ExpectedMetricSpec, ...] = (
    ExpectedMetricSpec(
        metric_key="revenue",
        roles=(
            AgentRole.EARNINGS_QUALITY,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.GUIDANCE,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.REQUIRED,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("sec_company_facts",),
        period_role=MetricPeriodRole.ACTUAL,
        cap_if_missing=True,
        sec_tags=(
            "Revenues",
            "SalesRevenueNet",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
        ),
        description="Current-period revenue used for earnings quality and summary context.",
    ),
    ExpectedMetricSpec(
        metric_key="eps",
        roles=(
            AgentRole.EARNINGS_QUALITY,
            AgentRole.GUIDANCE,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.REQUIRED,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("yfinance",),
        period_role=MetricPeriodRole.ACTUAL,
        cap_if_missing=True,
        sec_tags=("EarningsPerShareDiluted", "EarningsPerShareBasic"),
        description="Actual EPS. SEC GAAP EPS requires basis metadata before reconciliation.",
    ),
    ExpectedMetricSpec(
        metric_key="operating_cash_flow",
        roles=(
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.REQUIRED,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("sec_company_facts",),
        period_role=MetricPeriodRole.ACTUAL,
        cap_if_missing=True,
        sec_tags=("NetCashProvidedByUsedInOperatingActivities",),
        description="Current-period operating cash flow.",
    ),
    ExpectedMetricSpec(
        metric_key="capex",
        roles=(
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.REQUIRED,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("sec_company_facts",),
        period_role=MetricPeriodRole.ACTUAL,
        cap_if_missing=True,
        sec_tags=(
            "PaymentsToAcquirePropertyPlantAndEquipment",
            "PaymentsToAcquireProductiveAssets",
        ),
        description="Current-period capital expenditures, normalized as an outflow.",
    ),
    ExpectedMetricSpec(
        metric_key="free_cash_flow",
        roles=(
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.REQUIRED,
        source_policy=MetricSourcePolicy.DERIVED,
        preferred_sources=("derived_from_operating_cash_flow_and_capex",),
        period_role=MetricPeriodRole.ACTUAL,
        cap_if_missing=True,
        source_type=SourceType.DERIVED_METRIC,
        description="Derived as operating cash flow minus absolute capex.",
    ),
    ExpectedMetricSpec(
        metric_key="revenue_consensus",
        roles=(AgentRole.EARNINGS_QUALITY, AgentRole.GUIDANCE),
        requirement=MetricRequirement.OPTIONAL,
        source_policy=MetricSourcePolicy.CONSENSUS,
        preferred_sources=("yfinance",),
        period_role=MetricPeriodRole.CONSENSUS,
        description="Consensus revenue estimate when available.",
    ),
    ExpectedMetricSpec(
        metric_key="eps_consensus",
        roles=(AgentRole.EARNINGS_QUALITY, AgentRole.GUIDANCE),
        requirement=MetricRequirement.OPTIONAL,
        source_policy=MetricSourcePolicy.CONSENSUS,
        preferred_sources=("yfinance",),
        period_role=MetricPeriodRole.CONSENSUS,
        description="Consensus EPS estimate when available.",
    ),
    ExpectedMetricSpec(
        metric_key="operating_margin_pct",
        roles=(AgentRole.EARNINGS_QUALITY, AgentRole.MANAGEMENT_INTENT),
        requirement=MetricRequirement.OPTIONAL,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("yfinance", "sec_company_facts"),
        period_role=MetricPeriodRole.ACTUAL,
        description="Operating margin if precomputed.",
    ),
    ExpectedMetricSpec(
        metric_key="presentation_metric_candidates",
        roles=(
            AgentRole.EARNINGS_QUALITY,
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.GUIDANCE,
        ),
        requirement=MetricRequirement.REFERENCE_ONLY,
        source_policy=MetricSourcePolicy.PRESENTATION_REFERENCE,
        preferred_sources=("earnings_presentation",),
        period_role=MetricPeriodRole.AUDIT_ONLY,
        source_type=SourceType.EARNINGS_PRESENTATION,
        description=(
            "Presentation numeric candidates are auxiliary only and must not be "
            "canonical or confidence-cap inputs."
        ),
    ),
    ExpectedMetricSpec(
        metric_key="transcript_metrics",
        roles=(AgentRole.MANAGEMENT_INTENT, AgentRole.GUIDANCE),
        requirement=MetricRequirement.NOT_IN_CONTRACT,
        source_policy=MetricSourcePolicy.DOCUMENT_TEXT,
        preferred_sources=("earnings_call",),
        period_role=MetricPeriodRole.AUDIT_ONLY,
        source_type=SourceType.EARNINGS_CALL,
        description="Transcript metrics are not part of the current canonical input contract.",
    ),
    ExpectedMetricSpec(
        metric_key="prior_period_metrics",
        roles=(
            AgentRole.EARNINGS_QUALITY,
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.GUIDANCE,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.NOT_IN_CONTRACT,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("sec_company_facts", "yfinance"),
        period_role=MetricPeriodRole.PRIOR_PERIOD,
        source_type=SourceType.FINANCIAL_API,
        description=(
            "Previous-quarter metrics are not fetched by the current P0 contract; "
            "agents may report them as a follow-up data need but must not treat them as missing."
        ),
    ),
    ExpectedMetricSpec(
        metric_key="year_ago_period_metrics",
        roles=(
            AgentRole.EARNINGS_QUALITY,
            AgentRole.CASH_FLOW_RISK,
            AgentRole.MANAGEMENT_INTENT,
            AgentRole.GUIDANCE,
            AgentRole.BULL,
            AgentRole.BEAR,
            AgentRole.JUDGE,
        ),
        requirement=MetricRequirement.NOT_IN_CONTRACT,
        source_policy=MetricSourcePolicy.CANONICAL,
        preferred_sources=("sec_company_facts", "yfinance"),
        period_role=MetricPeriodRole.PRIOR_PERIOD,
        source_type=SourceType.FINANCIAL_API,
        description=(
            "Year-ago comparable quarter metrics are not fetched by the current P0 contract; "
            "agents may report them as a follow-up data need but must not treat them as missing."
        ),
    ),
)


def expected_metric_specs(role: AgentRole | None = None) -> tuple[ExpectedMetricSpec, ...]:
    if role is None:
        return EXPECTED_METRICS
    return tuple(spec for spec in EXPECTED_METRICS if role in spec.roles)


def expected_metric_context(role: AgentRole) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {
        requirement.value: [] for requirement in MetricRequirement
    }
    for spec in expected_metric_specs(role):
        grouped[spec.requirement.value].append(spec.for_context())
    return {"role": role.value, **grouped}


def canonical_metric_availability(metrics: FinancialMetrics) -> list[AvailabilityItem]:
    items: list[AvailabilityItem] = []
    seen: set[str] = set()
    for spec in EXPECTED_METRICS:
        if (
            spec.metric_key in seen
            or spec.requirement is not MetricRequirement.REQUIRED
            or spec.source_policy is MetricSourcePolicy.PRESENTATION_REFERENCE
            or not spec.cap_if_missing
        ):
            continue
        seen.add(spec.metric_key)
        if not _canonical_metric_is_available(metrics, spec):
            items.append(
                AvailabilityItem(
                    key=spec.metric_key,
                    status=AvailabilityStatus.REQUIRED_MISSING,
                    reason=(
                        f"Required canonical metric {spec.metric_key} was not available "
                        "from accepted SEC/yfinance/derived source refs."
                    ),
                    source_type=spec.source_type,
                    blocks_verdict=False,
                )
            )
        else:
            items.append(
                AvailabilityItem(
                    key=spec.metric_key,
                    status=AvailabilityStatus.AVAILABLE,
                    reason=f"Required canonical metric {spec.metric_key} is available.",
                    source_type=spec.source_type,
                )
            )
    return items


def _canonical_metric_is_available(metrics: FinancialMetrics, spec: ExpectedMetricSpec) -> bool:
    value = getattr(metrics, spec.metric_key, None)
    if value is None:
        return False
    if spec.source_policy is MetricSourcePolicy.DERIVED:
        return _has_accepted_derived_metric(metrics, spec)
    return _has_accepted_source_ref(metrics, spec)


def _has_accepted_source_ref(metrics: FinancialMetrics, spec: ExpectedMetricSpec) -> bool:
    for metric in metrics.canonical_metrics:
        if (
            metric.metric_name != spec.metric_key
            or metric.period_role != spec.period_role
            or metric.fiscal_period != metrics.fiscal_period
        ):
            continue
        if _source_ref_satisfies(metric.source_ref, spec, metrics.fiscal_period):
            return True
    return any(
        ref.metric_name == spec.metric_key
        and _source_ref_satisfies(ref, spec, metrics.fiscal_period)
        for ref in metrics.source_refs
    )


def _has_accepted_derived_metric(metrics: FinancialMetrics, spec: ExpectedMetricSpec) -> bool:
    component_specs = {
        component.metric_key: component
        for component in EXPECTED_METRICS
        if component.metric_key in {"operating_cash_flow", "capex"}
        and component.requirement is MetricRequirement.REQUIRED
    }
    for metric in metrics.derived_metrics:
        if (
            metric.metric_name != spec.metric_key
            or metric.period_role != spec.period_role
            or metric.fiscal_period != metrics.fiscal_period
        ):
            continue
        if metric.source_ref.source_type is not SourceType.DERIVED_METRIC:
            continue
        if metric.source_ref.reported_period != metrics.fiscal_period:
            continue
        component_refs = {ref.metric_name: ref for ref in metric.component_source_refs}
        if all(
            component_key in component_refs
            and _source_ref_satisfies(
                component_refs[component_key],
                component_spec,
                metrics.fiscal_period,
            )
            for component_key, component_spec in component_specs.items()
        ):
            return True
    source_refs_by_metric = {ref.metric_name: ref for ref in metrics.source_refs if ref.metric_name}
    derived_ref = source_refs_by_metric.get(spec.metric_key)
    if derived_ref is None or derived_ref.source_type is not SourceType.DERIVED_METRIC:
        return False
    if derived_ref.period_role is not spec.period_role:
        return False
    if derived_ref.reported_period != metrics.fiscal_period:
        return False
    return all(
        component_key in source_refs_by_metric
        and _source_ref_satisfies(
            source_refs_by_metric[component_key],
            component_spec,
            metrics.fiscal_period,
        )
        for component_key, component_spec in component_specs.items()
    )


def _source_ref_satisfies(ref: Any, spec: ExpectedMetricSpec, fiscal_period: str) -> bool:
    if ref.source_type is not spec.source_type:
        return False
    if ref.period_role is not spec.period_role:
        return False
    if ref.reported_period != fiscal_period:
        return False
    provider = ref.provider
    if spec.preferred_sources and provider not in spec.preferred_sources:
        return False
    return True


def with_canonical_metric_availability(metrics: FinancialMetrics) -> FinancialMetrics:
    canonical_items = canonical_metric_availability(metrics)
    canonical_keys = {item.key for item in canonical_items}
    provider_items = [
        item
        for item in metrics.availability
        if item.key not in canonical_keys or item.status is AvailabilityStatus.CONFLICTING
    ]
    return metrics.model_copy(update={"availability": [*provider_items, *canonical_items]})
