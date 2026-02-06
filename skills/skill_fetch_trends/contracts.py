"""Contracts for the trend fetching skill."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def assemble_trend_response(
    *,
    trace_id: str,
    planner_task_id: str,
    platform: str,
    topics: List[str],
    time_window: Dict[str, str],
    signals: Dict[str, bool],
    geo: Optional[str],
    persona_priority: Optional[List[str]],
    trends: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Return a contract-compliant trend response payload."""
    raise NotImplementedError("Trend response contract not implemented yet")
