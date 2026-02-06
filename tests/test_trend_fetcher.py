"""Contract tests for the trend fetcher skill.

These tests codify the JSON envelope and field-level requirements described in
specs/technical.md and skills/skill_fetch_trends/README.md. They currently fail
because the skill implementation does not yet assemble the response object.
"""
from __future__ import annotations

import pytest

from skills.skill_fetch_trends import contracts


@pytest.fixture
def sample_trends() -> list[dict[str, object]]:
    return [
        {
            "trend_id": "trend-123",
            "platform": "twitter",
            "topic": "#SolarThreads",
            "momentum_score": 0.82,
            "volume": 15432,
            "sentiment": 0.66,
            "summary": "Designers pairing solar fabrics with traditional Ethiopian patterns.",
            "source_citations": [
                {
                    "type": "tweet",
                    "url": "https://twitter.com/example",
                    "captured_at": "2026-02-05T10:02:00Z",
                }
            ],
        }
    ]


def test_trend_response_envelope(sample_trends: list[dict[str, object]]) -> None:
    response = contracts.assemble_trend_response(
        trace_id="trace-abc",
        planner_task_id="task-xyz",
        platform="twitter",
        topics=["solar fashion"],
        time_window={"start": "2026-02-01T00:00:00Z", "end": "2026-02-06T00:00:00Z"},
        signals={"include_news": True, "include_social": True, "include_commerce": False},
        geo="global",
        persona_priority=["eco-conscious"],
        trends=sample_trends,
    )

    assert response["version"] == "1.0"
    assert response["status"] == "SUCCESS"
    assert response["trace_id"] == "trace-abc"
    assert response["planner_task_id"] == "task-xyz"

    payload = response["payload"]
    assert payload["platform"] == "twitter"
    assert payload["topics"] == ["solar fashion"]
    assert payload["time_window"]["start"] == "2026-02-01T00:00:00Z"
    assert payload["signals"]["include_news"] is True

    trend = payload["trends"][0]
    for field in (
        "trend_id",
        "platform",
        "topic",
        "momentum_score",
        "volume",
        "sentiment",
        "summary",
        "source_citations",
    ):
        assert field in trend, f"missing {field} in trend payload"

    citation = trend["source_citations"][0]
    assert citation["type"] == "tweet"
    assert citation["url"].startswith("https://")
    assert citation["captured_at"].endswith("Z")
