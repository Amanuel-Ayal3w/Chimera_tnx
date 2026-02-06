#!/usr/bin/env python3
"""Lightweight spec conformance checks for Project Chimera.

This script purposely focuses on structural guarantees that keep code aligned with
the SRS-derived specs. It can be expanded over time with semantic checks as the
system matures.
"""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_SPEC_FILES = [
    Path("specs/_meta.md"),
    Path("specs/functional.md"),
    Path("specs/technical.md"),
]

REQUIRED_SKILL_READMES = [
    Path("skills/README.md"),
    Path("skills/skill_fetch_trends/README.md"),
    Path("skills/skill_generate_multimodal_content/README.md"),
    Path("skills/skill_validate_content/README.md"),
]

REQUIRED_TESTS = [
    Path("tests/test_trend_fetcher.py"),
    Path("tests/test_skills_interface.py"),
]


def check_files(paths: list[Path], label: str) -> list[str]:
    missing: list[str] = []
    for path in paths:
        if not path.exists():
            missing.append(f"Missing {label}: {path}")
        elif path.stat().st_size == 0:
            missing.append(f"Empty {label}: {path}")
    return missing


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cwd = Path.cwd()
    if cwd != root:
        # Ensure relative paths resolve correctly.
        print(f"[spec-check] Warning: expected to run from repo root {root}, got {cwd}")

    problems: list[str] = []
    problems += check_files(REQUIRED_SPEC_FILES, "spec file")
    problems += check_files(REQUIRED_SKILL_READMES, "skill README")
    problems += check_files(REQUIRED_TESTS, "contract test")

    if problems:
        for problem in problems:
            print(problem)
        print(f"[spec-check] FAILED with {len(problems)} issue(s)")
        return 1

    print("[spec-check] All required spec artifacts and tests are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
