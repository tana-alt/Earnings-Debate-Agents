"""Runtime prompt composition for workflow agents."""

from __future__ import annotations

from pathlib import Path


PROMPT_ROOT = Path(__file__).resolve().parent / "prompts"
SHARED_PROMPT_FILES = (
    "shared/global_policy.md",
    "shared/evidence_policy.md",
    "shared/output_policy.md",
)

AGENT_PROMPT_FILES = {
    "EarningsQualityAnalyst": "financial/earnings_quality_analyst.md",
    "CashFlowRiskAnalyst": "financial/cash_flow_risk_analyst.md",
    "ManagementIntentAnalyst": "presentation/management_intent_analyst.md",
    "GuidanceAnalyst": "presentation/guidance_analyst.md",
    "BullAgent": "debate/bull_agent.md",
    "BearAgent": "debate/bear_agent.md",
    "JudgeAgent": "debate/judge_agent.md",
}


def read_prompt(relative_path: str) -> str:
    path = (PROMPT_ROOT / relative_path).resolve()
    if PROMPT_ROOT not in path.parents:
        raise ValueError(f"prompt path escapes prompt root: {relative_path}")
    if "index" in path.relative_to(PROMPT_ROOT).parts:
        raise ValueError(f"runtime prompts cannot load index prompts: {relative_path}")
    return path.read_text(encoding="utf-8").strip()


def build_system_prompt(public_role: str, fallback_scope: str) -> str:
    """Compose shared policies plus exactly one runtime agent prompt."""

    try:
        agent_prompt_file = AGENT_PROMPT_FILES[public_role]
    except KeyError as exc:
        raise ValueError(f"unknown workflow agent role: {public_role}") from exc

    parts = [
        f"<!-- ROLE: {public_role} -->",
        f"あなたは米国株四半期決算レビューworkflowの {public_role} です。",
        f"責務: {fallback_scope}",
    ]
    parts.extend(read_prompt(path) for path in SHARED_PROMPT_FILES)
    parts.append(_mask_other_role_names(read_prompt(agent_prompt_file), public_role))
    return "\n\n".join(parts)


def _mask_other_role_names(text: str, public_role: str) -> str:
    """Keep role detection stable when prompt prose references peer agents."""

    for role in AGENT_PROMPT_FILES:
        if role != public_role:
            text = text.replace(role, role.replace("Analyst", " Analyst").replace("Agent", " Agent"))
    return text
