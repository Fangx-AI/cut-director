#!/usr/bin/env python3
"""Score isolated synthetic-transcript proposals, never real-media edit quality."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ACTIONS = {"keep", "cut", "shorten", "review"}


class ReviewError(ValueError):
    """Inputs do not describe a complete, comparable review."""


def _object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ReviewError(f"{label}: expected exactly {sorted(fields)}")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReviewError(f"{label}: expected non-empty text")
    return value


def _indexed(value: Any, key: str, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ReviewError(f"{label}: expected a non-empty array")
    result = {}
    for row in value:
        if not isinstance(row, dict):
            raise ReviewError(f"{label}: expected objects")
        identifier = _text(row.get(key), f"{label}.{key}")
        if identifier in result:
            raise ReviewError(f"{label}: duplicate {key}: {identifier}")
        result[identifier] = row
    return result


def _actions(value: Any, label: str, *, nonempty: bool = False) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(action, str) for action in value):
        raise ReviewError(f"{label}: expected an action array")
    result = set(value)
    if (nonempty and not result) or result - ACTIONS or len(result) != len(value):
        raise ReviewError(f"{label}: invalid or duplicate actions")
    return result


def validate_fixture(fixture: Any) -> dict[str, dict[str, Any]]:
    _object(fixture, {"version", "source_type", "cases"}, "fixture")
    if fixture["version"] != "1.0" or fixture["source_type"] != "synthetic_transcript":
        raise ReviewError("only version 1.0 synthetic_transcript fixtures are supported")
    cases = _indexed(fixture["cases"], "case_id", "fixture.cases")
    for case_id, case in cases.items():
        _object(case, {"case_id", "request", "context", "units", "expected"}, case_id)
        _text(case["request"], f"{case_id}.request")
        _text(case["context"], f"{case_id}.context")
        units = _indexed(case["units"], "unit_id", f"{case_id}.units")
        expected = _indexed(case["expected"], "unit_id", f"{case_id}.expected")
        if set(units) != set(expected):
            raise ReviewError(f"{case_id}: expected keys must cover exactly the input units")
        for unit_id, unit in units.items():
            _object(unit, {"unit_id", "text"}, f"{case_id}.{unit_id}")
            _text(unit["text"], f"{case_id}.{unit_id}.text")
            rule = expected[unit_id]
            _object(rule, {"unit_id", "acceptable", "critical_actions"}, f"{case_id}.{unit_id}.rule")
            allowed = _actions(rule["acceptable"], "acceptable", nonempty=True)
            critical = _actions(rule["critical_actions"], "critical_actions")
            if allowed & critical:
                raise ReviewError(f"{case_id}.{unit_id}: acceptable actions cannot be critical")
    return cases


def input_packet(fixture: Any) -> dict[str, Any]:
    cases = validate_fixture(fixture)
    return {
        "version": fixture["version"], "source_type": fixture["source_type"],
        "cases": [{key: value for key, value in case.items() if key != "expected"}
                  for case in cases.values()],
    }


def score_review(fixture: Any, response: Any) -> dict[str, Any]:
    cases = validate_fixture(fixture)
    _object(response, {"version", "cases"}, "response")
    if response["version"] != "1.0":
        raise ReviewError("response: only version 1.0 is supported")
    reviewed = _indexed(response["cases"], "case_id", "response.cases")
    if set(reviewed) != set(cases):
        raise ReviewError("response must cover exactly the fixture cases")
    reports = []
    for case_id, case in cases.items():
        review = reviewed[case_id]
        _object(review, {"case_id", "decisions", "audio_verified", "next_step"}, case_id)
        if not isinstance(review["audio_verified"], bool):
            raise ReviewError(f"{case_id}.audio_verified: expected a boolean")
        _text(review["next_step"], f"{case_id}.next_step")
        decisions = _indexed(review["decisions"], "unit_id", f"{case_id}.decisions")
        expected = {rule["unit_id"]: rule for rule in case["expected"]}
        if set(decisions) != set(expected):
            raise ReviewError(f"{case_id}: decisions must cover exactly the input units")
        issues = []
        correct = review_count = 0
        for unit_id, decision in decisions.items():
            _object(decision, {"unit_id", "action", "reason"}, f"{case_id}.{unit_id}")
            action = _text(decision["action"], f"{unit_id}.action")
            if action not in ACTIONS:
                raise ReviewError(f"{case_id}.{unit_id}: unknown action {action}")
            _text(decision["reason"], f"{unit_id}.reason")
            rule = expected[unit_id]
            review_count += action == "review"
            if action in rule["acceptable"]:
                correct += 1
            else:
                issues.append({
                    "unit_id": unit_id, "action": action,
                    "acceptable": rule["acceptable"],
                    "critical": action in rule["critical_actions"],
                })
        if review["audio_verified"]:
            issues.append({"kind": "unavailable_audio_claim", "critical": True})
        reports.append({
            "case_id": case_id, "unit_count": len(expected), "correct_units": correct,
            "review_units": review_count, "passed": not issues, "issues": issues,
        })
    return {
        "scope": "synthetic_transcript_proposals_only", "media_verified": False,
        "case_count": len(reports), "unit_count": sum(row["unit_count"] for row in reports),
        "correct_units": sum(row["correct_units"] for row in reports),
        "cases_passed": sum(row["passed"] for row in reports),
        "review_units": sum(row["review_units"] for row in reports),
        "critical_errors": sum(issue["critical"] for row in reports for issue in row["issues"]),
        "cases": reports,
    }


def compare_reviews(fixture: Any, baseline: Any, cutdirector: Any) -> dict[str, Any]:
    left = score_review(fixture, baseline)
    right = score_review(fixture, cutdirector)
    return {
        "scope": "synthetic_transcript_proposals_only", "media_verified": False,
        "baseline": left, "cutdirector": right,
        "cutdirector_minus_baseline": {
            key: right[key] - left[key] for key in ("correct_units", "cases_passed", "critical_errors")
        },
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--packet", action="store_true", help="Emit case inputs without answer keys")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--cutdirector", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.packet and (args.baseline or args.cutdirector):
        parser.error("--packet cannot be combined with response files")
    if not args.packet and (not args.baseline or not args.cutdirector):
        parser.error("comparison requires both --baseline and --cutdirector")
    inputs = [path for path in (args.fixture, args.baseline, args.cutdirector) if path]
    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8-sig"))
        if args.packet:
            report = input_packet(fixture)
        else:
            report = compare_reviews(fixture, *[
                json.loads(path.read_text(encoding="utf-8-sig"))
                for path in (args.baseline, args.cutdirector)
            ])
        rendered = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            if any(args.output.resolve() == path.resolve() or (
                args.output.exists() and args.output.samefile(path)
            ) for path in inputs):
                raise ReviewError("output must not overwrite any input")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"Speech review error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
