"""Skill interface contract tests."""
from __future__ import annotations

from datetime import datetime

import pytest

from skills.skill_fetch_trends import interface as trend_interface
from skills.skill_generate_multimodal_content import interface as multimodal_interface
from skills.skill_validate_content import interface as validation_interface


def test_fetch_trends_interface_signature() -> None:
    response = trend_interface.fetch_trends(
        trace_id="trace-abc",
        planner_task_id="task-xyz",
        platform="twitter",
        topics=["solar fashion"],
        time_window={"start": "2026-02-01T00:00:00Z", "end": "2026-02-06T00:00:00Z"},
        signals={"include_news": True, "include_social": True, "include_commerce": False},
        geo="global",
        persona_priority=["eco-conscious"],
    )

    assert response["version"] == "1.0"


def test_generate_multimodal_interface_contract() -> None:
    response = multimodal_interface.generate_artifacts(
        trace_id="trace-123",
        planner_task_id="task-789",
        campaign_id="campaign-111",
        agent_id="agent-222",
        persona_profile_ref="filesystem://agents/liyu/SOUL.md",
        trend_context={"trend_id": "trend-456", "insight_summary": "..."},
        artifact_plan=[
            {
                "artifact_id": "artifact-1",
                "modality": "text",
                "platform": "instagram",
                "length": {"min_tokens": 60, "max_tokens": 120},
            }
        ],
        guardrails={"max_budget_usd": 0.45, "banned_topics": ["politics"]},
    )

    assert response["status"] == "SUCCESS"


def test_validate_content_interface_contract() -> None:
    response = validation_interface.validate_artifact(
        trace_id="trace-987",
        planner_task_id="task-654",
        artifact={
            "artifact_id": "artifact-2",
            "modality": "text",
            "platform": "instagram",
            "content": "Solar denim drop",
        },
        policy_bundle={
            "brand_voice_ref": "filesystem://policies/brand/aiqem.md",
            "regulatory_refs": ["compliance://eu-ai-act/disclosure"],
            "platform_rules": ["platform://instagram/2026-01/publish"],
        },
        delivery_target={
            "geo": "ET",
            "audience_segment": "gen-z",
            "release_window": datetime.utcnow().isoformat() + "Z",
        },
        risk_toggles={
            "require_disclosure": True,
            "max_negative_sentiment": 0.3,
            "require_wallet_callout": False,
        },
    )

    assert response["payload"]["validation_result"] in {"APPROVED", "NEEDS_REVIEW", "REJECTED"}
