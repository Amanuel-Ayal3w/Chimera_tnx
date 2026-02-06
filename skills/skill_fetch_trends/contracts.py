"""Contracts for the trend fetching skill.

These functions are intentionally unimplemented; the failing tests define the
expected response schema and validation behaviors.
"""
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
    """Return a contract-compliant trend response payload.

    The implementation is pending. Tests call this function to assert that the
    returned object contains the deterministic envelope described in
    specs/technical.md as well as the skill README.
    """
    raise NotImplementedError("Contract assembly not implemented yet")
