from src.expected_metrics import (
    MetricRequirement,
    MetricSourcePolicy,
    canonical_metric_availability,
    expected_metric_context,
    expected_metric_specs,
)
from src.workflow_models import (
    AgentRole,
    AvailabilityStatus,
    FinancialMetrics,
    MetricPeriodRole,
    SourceRef,
    SourceType,
)


def test_expected_metric_registry_marks_presentation_reference_only_non_cap():
    specs = expected_metric_specs(AgentRole.GUIDANCE)
    presentation_specs = [
        spec for spec in specs if spec.source_policy is MetricSourcePolicy.PRESENTATION_REFERENCE
    ]

    assert presentation_specs
    assert all(spec.requirement is MetricRequirement.REFERENCE_ONLY for spec in presentation_specs)
    assert all(not spec.cap_if_missing for spec in presentation_specs)


def financial_ref(metric_name, *, provider="sec_company_facts", reported_period="2025Q3"):
    return SourceRef(
        source_id=f"financial_api:NVDA:{reported_period}:{provider}:{metric_name}",
        source_type=SourceType.FINANCIAL_API,
        metric_name=metric_name,
        reported_period=reported_period,
        provider=provider,
        period_role=MetricPeriodRole.ACTUAL,
    )


def derived_fcf_ref(*, reported_period="2025Q3"):
    return SourceRef(
        source_id=f"metric:NVDA:{reported_period}:free_cash_flow:derived",
        source_type=SourceType.DERIVED_METRIC,
        metric_name="free_cash_flow",
        reported_period=reported_period,
        period_role=MetricPeriodRole.ACTUAL,
    )


def test_expected_metric_context_is_readable_for_agents():
    context = expected_metric_context(AgentRole.CASH_FLOW_RISK)

    assert context["role"] == "cash_flow_risk"
    assert "required" in context
    assert any(item["metric_key"] == "operating_cash_flow" for item in context["required"])
    assert any(item["metric_key"] == "free_cash_flow" for item in context["required"])
    assert all(item["cap_if_missing"] for item in context["required"])
    assert any(item["metric_key"] == "prior_period_metrics" for item in context["not_in_contract"])
    assert any(
        item["metric_key"] == "year_ago_period_metrics" for item in context["not_in_contract"]
    )


def test_expected_metric_registry_marks_all_requirement_buckets():
    context = expected_metric_context(AgentRole.GUIDANCE)

    assert any(item["metric_key"] == "revenue" for item in context["required"])
    assert any(item["metric_key"] == "eps_consensus" for item in context["optional"])
    assert any(
        item["metric_key"] == "presentation_metric_candidates" for item in context["reference_only"]
    )
    assert any(item["metric_key"] == "transcript_metrics" for item in context["not_in_contract"])
    assert all(not item["cap_if_missing"] for item in context["optional"])
    assert all(not item["cap_if_missing"] for item in context["not_in_contract"])


def test_canonical_metric_availability_caps_only_required_canonical_gaps():
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        operating_cash_flow=15_000_000_000,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            financial_ref("revenue"),
            financial_ref("eps", provider="yfinance"),
            financial_ref("operating_cash_flow"),
            financial_ref("capex"),
            derived_fcf_ref(),
        ],
    )

    items = canonical_metric_availability(metrics)

    assert all(item.status is AvailabilityStatus.AVAILABLE for item in items)


def test_presentation_sourced_top_level_value_does_not_satisfy_canonical_availability():
    presentation_ref = SourceRef(
        source_id="presentation:NVDA:2025Q3:revenue",
        source_type=SourceType.EARNINGS_PRESENTATION,
        document_id="deck",
        section_id="actuals",
        metric_name="revenue",
        reported_period="2025Q3",
        period_role=MetricPeriodRole.ACTUAL,
    )
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        operating_cash_flow=15_000_000_000,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            presentation_ref,
            financial_ref("eps", provider="yfinance"),
            financial_ref("operating_cash_flow"),
            financial_ref("capex"),
            derived_fcf_ref(),
        ],
    )

    by_key = {item.key: item for item in canonical_metric_availability(metrics)}

    assert by_key["revenue"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["eps"].status is AvailabilityStatus.AVAILABLE


def test_yfinance_p0_fallback_does_not_satisfy_sec_required_canonical_metrics():
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        operating_cash_flow=15_000_000_000,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            financial_ref("revenue", provider="yfinance"),
            financial_ref("eps", provider="yfinance"),
            financial_ref("operating_cash_flow", provider="yfinance"),
            financial_ref("capex", provider="yfinance"),
            derived_fcf_ref(),
        ],
    )

    by_key = {item.key: item for item in canonical_metric_availability(metrics)}

    assert by_key["eps"].status is AvailabilityStatus.AVAILABLE
    assert by_key["revenue"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["operating_cash_flow"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["capex"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["free_cash_flow"].status is AvailabilityStatus.REQUIRED_MISSING


def test_sec_eps_ref_does_not_satisfy_yfinance_required_eps():
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        operating_cash_flow=15_000_000_000,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            financial_ref("revenue"),
            financial_ref("eps", provider="sec_company_facts"),
            financial_ref("operating_cash_flow"),
            financial_ref("capex"),
            derived_fcf_ref(),
        ],
    )

    by_key = {item.key: item for item in canonical_metric_availability(metrics)}

    assert by_key["eps"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["revenue"].status is AvailabilityStatus.AVAILABLE


def test_stale_reported_period_source_ref_does_not_satisfy_canonical_availability():
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        operating_cash_flow=15_000_000_000,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            financial_ref("revenue", reported_period="2025Q2"),
            financial_ref("eps", provider="yfinance", reported_period="2025Q2"),
            financial_ref("operating_cash_flow", reported_period="2025Q2"),
            financial_ref("capex", reported_period="2025Q2"),
            derived_fcf_ref(reported_period="2025Q2"),
        ],
    )

    items = canonical_metric_availability(metrics)

    assert all(item.status is AvailabilityStatus.REQUIRED_MISSING for item in items)


def test_missing_required_canonical_metric_is_financial_api_gap():
    metrics = FinancialMetrics(
        ticker="NVDA",
        fiscal_period="2025Q3",
        revenue=35_000_000_000,
        eps=0.81,
        capex=-3_000_000_000,
        free_cash_flow=12_000_000_000,
        source_refs=[
            financial_ref("revenue"),
            financial_ref("eps", provider="yfinance"),
            financial_ref("capex"),
            derived_fcf_ref(),
        ],
    )

    items = canonical_metric_availability(metrics)
    by_key = {item.key: item for item in items}

    assert by_key["operating_cash_flow"].status is AvailabilityStatus.REQUIRED_MISSING
    assert by_key["operating_cash_flow"].source_type is SourceType.FINANCIAL_API
    assert by_key["operating_cash_flow"].blocks_verdict is False
    assert "presentation" not in by_key
