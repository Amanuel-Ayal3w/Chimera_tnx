"""Runtime interface for the trend fetching skill.

Workers will eventually call `fetch_trends` to collect multi-source signals. The
function currently raises `NotImplementedError` so tests can define the missing
behavior.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def fetch_trends(
    *,
    trace_id: str,
    planner_task_id: str,
    platform: str,
    topics: List[str],
    time_window: Dict[str, str],
    signals: Dict[str, bool],
    geo: Optional[str],
    persona_priority: Optional[List[str]],
) -> Dict[str, Any]:
    """Fetch normalized trend data aligned with the skill contract."""
    raise NotImplementedError("trend fetching not implemented yet")
