#!/usr/bin/env python3
"""Validate linear speech selections and map source anchors to the edited cut."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


EPSILON = 1e-9
CUT_KINDS = {"filler", "false_start", "retake", "redundancy", "production_aside", "silence"}


class SpeechPlanError(ValueError):
    """The plan cannot describe an unambiguous linear edit."""


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpeechPlanError(f"{label}: expected a finite number")
    try:
        number = float(value)
    except OverflowError as error:
        raise SpeechPlanError(f"{label}: expected a finite number") from error
    if not math.isfinite(number):
        raise SpeechPlanError(f"{label}: expected a finite number")
    return number


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpeechPlanError(f"{label}: expected non-empty text")
    return value


def _rows(value: Any, label: str, *, nonempty: bool = False) -> list[dict[str, Any]]:
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise SpeechPlanError(f"{label}: expected an array of objects")
    if nonempty and not value:
        raise SpeechPlanError(f"{label}: at least one item is required")
    return value


def _fields(row: dict[str, Any], allowed: set[str], label: str) -> None:
    if set(row) - allowed:
        raise SpeechPlanError(f"{label}: unsupported fields: {sorted(set(row) - allowed)}")


def _interval(row: dict[str, Any], duration: float, label: str) -> tuple[float, float]:
    start = _number(row.get("start"), f"{label}.start")
    end = _number(row.get("end"), f"{label}.end")
    if start < 0 or end > duration or end - start <= EPSILON:
        raise SpeechPlanError(f"{label}: range must satisfy 0 <= start < end <= source duration")
    return start, end


def _unique_ids(rows: list[dict[str, Any]], key: str, label: str) -> None:
    identifiers = [_text(row.get(key), f"{label}.{key}") for row in rows]
    if len(set(identifiers)) != len(identifiers):
        raise SpeechPlanError(f"{label}: duplicate {key}")


def _overlap(left: tuple[float, float], right: tuple[float, float]) -> bool:
    return min(left[1], right[1]) - max(left[0], right[0]) > EPSILON


def validate_plan(plan: Any) -> None:
    if not isinstance(plan, dict):
        raise SpeechPlanError("plan: expected an object")
    _fields(plan, {"version", "mode", "revision", "allow_reorder", "reorder_reason", "sources", "keep", "cuts"}, "plan")
    if plan.get("version") != "0.1" or plan.get("mode") != "linear-1x":
        raise SpeechPlanError("only version 0.1 linear-1x plans are supported")
    _text(plan.get("revision"), "revision")
    allow_reorder = plan.get("allow_reorder", False)
    if not isinstance(allow_reorder, bool):
        raise SpeechPlanError("allow_reorder: expected a boolean")
    if allow_reorder:
        _text(plan.get("reorder_reason"), "reorder_reason")

    sources = _rows(plan.get("sources"), "sources", nonempty=True)
    keeps = _rows(plan.get("keep"), "keep", nonempty=True)
    cuts = _rows(plan.get("cuts", []), "cuts")
    _unique_ids(sources, "source_id", "sources")
    _unique_ids(keeps, "segment_id", "keep")
    _unique_ids(cuts, "cut_id", "cuts")
    source_lookup = {source["source_id"]: source for source in sources}
    source_order = {source["source_id"]: index for index, source in enumerate(sources)}

    for source in sources:
        _fields(source, {"source_id", "duration", "words"}, "source")
        source_id = source["source_id"]
        duration = _number(source.get("duration"), f"{source_id}.duration")
        if duration <= 0:
            raise SpeechPlanError(f"{source_id}: duration must be positive")
        words = _rows(source.get("words", []), f"{source_id}.words")
        _unique_ids(words, "word_id", f"{source_id}.words")
        previous_start = -1.0
        for word in words:
            _fields(word, {"word_id", "text", "start", "end"}, "word")
            start, _ = _interval(word, duration, f"word {word['word_id']}")
            _text(word.get("text"), f"word {word['word_id']}.text")
            if start < previous_start:
                raise SpeechPlanError(f"{source_id}: words must be in source-time order")
            previous_start = start

    kept_by_source: dict[str, list[tuple[float, float]]] = {key: [] for key in source_lookup}
    sequence: list[tuple[int, float]] = []
    for row in keeps:
        _fields(row, {"segment_id", "source_id", "start", "end", "rate"}, "keep")
    for row in cuts:
        _fields(row, {"cut_id", "source_id", "start", "end", "kind", "reason"}, "cut")
    for row in keeps + cuts:
        source_id = _text(row.get("source_id"), "range.source_id")
        if source_id not in source_lookup:
            raise SpeechPlanError(f"unknown source_id: {source_id}")
        source = source_lookup[source_id]
        label = row.get("segment_id", row.get("cut_id", "range"))
        start, end = _interval(row, source["duration"], str(label))
        if "rate" in row and _number(row["rate"], f"{label}.rate") != 1:
            raise SpeechPlanError("variable speed requires the host's actual timeline mapping")
        # Only supplied, trusted word boundaries can prove that a cut avoids a word.
        for boundary in (start, end):
            for word in source.get("words", []):
                if word["start"] + EPSILON < boundary < word["end"] - EPSILON:
                    raise SpeechPlanError(f"{label}: boundary splits word {word['word_id']} ({word['text']})")
        if "segment_id" in row:
            previous = kept_by_source[source_id]
            if any(_overlap((start, end), span) for span in previous):
                raise SpeechPlanError(f"{source_id}: reused or overlapping kept ranges are unsupported")
            previous.append((start, end))
            sequence.append((source_order[source_id], start))
        else:
            if not isinstance(row.get("kind"), str) or row["kind"] not in CUT_KINDS:
                raise SpeechPlanError(f"{label}: unknown cut kind")
            _text(row.get("reason"), f"{label}.reason")
    if not allow_reorder and sequence != sorted(sequence):
        raise SpeechPlanError("source order changed without allow_reorder and reorder_reason")
    cut_by_source: dict[str, list[tuple[float, float]]] = {key: [] for key in source_lookup}
    for cut in cuts:
        source_id = cut["source_id"]
        span = (cut["start"], cut["end"])
        if any(_overlap(span, kept) for kept in kept_by_source[source_id]):
            raise SpeechPlanError(f"{cut['cut_id']}: declared cut overlaps kept speech")
        if any(_overlap(span, previous) for previous in cut_by_source[source_id]):
            raise SpeechPlanError(f"{cut['cut_id']}: overlapping cut explanations")
        cut_by_source[source_id].append(span)


def _removed_ranges(duration: float, spans: list[tuple[float, float]]) -> list[dict[str, float]]:
    removed = []
    cursor = 0.0
    for start, end in sorted(spans):
        if start - cursor > EPSILON:
            removed.append({"start": round(cursor, 9), "end": round(start, 9)})
        cursor = end
    if duration - cursor > EPSILON:
        removed.append({"start": round(cursor, 9), "end": round(duration, 9)})
    return removed


def compile_plan(plan: dict[str, Any]) -> dict[str, Any]:
    validate_plan(plan)
    segments = []
    cursor = 0.0
    for row in plan["keep"]:
        duration = row["end"] - row["start"]
        segments.append({
            "segment_id": row["segment_id"], "source_id": row["source_id"],
            "source_start": row["start"], "source_end": row["end"],
            "timeline_start": round(cursor, 9), "timeline_end": round(cursor + duration, 9),
        })
        cursor += duration
    source_reports = []
    for source in plan["sources"]:
        spans = [(row["start"], row["end"]) for row in plan["keep"] if row["source_id"] == source["source_id"]]
        source_reports.append({
            "source_id": source["source_id"], "duration": source["duration"],
            "removed_ranges": _removed_ranges(source["duration"], spans),
            "word_boundaries_checked": bool(source.get("words")),
        })
    return {
        "version": "0.1", "revision": plan["revision"], "mode": "linear-1x",
        "duration": round(cursor, 9), "segments": segments, "sources": source_reports,
        "cuts": plan.get("cuts", []), "media_verified": False,
    }


def map_anchor(plan: dict[str, Any], source_id: str, start: float, end: float) -> dict[str, Any]:
    compiled = compile_plan(plan)
    sources = {source["source_id"]: source for source in plan["sources"]}
    if source_id not in sources:
        raise SpeechPlanError(f"unknown anchor source_id: {source_id}")
    start, end = _interval({"start": start, "end": end}, sources[source_id]["duration"], "anchor")
    matches = []
    retained = 0.0
    for segment in compiled["segments"]:
        if segment["source_id"] != source_id:
            continue
        left = max(start, segment["source_start"])
        right = min(end, segment["source_end"])
        if right - left <= EPSILON:
            continue
        retained += right - left
        matches.append({
            "segment_id": segment["segment_id"], "source_start": left, "source_end": right,
            "timeline_start": round(segment["timeline_start"] + left - segment["source_start"], 9),
            "timeline_end": round(segment["timeline_start"] + right - segment["source_start"], 9),
        })
    fully_retained = abs(retained - (end - start)) <= EPSILON
    return {
        "revision": plan["revision"], "source_id": source_id,
        "source_start": start, "source_end": end, "spans": matches,
        "fully_retained": fully_retained, "single_span": len(matches) == 1,
        "requires_reanchor": not fully_retained or len(matches) != 1,
    }


def main() -> int:
    # The CLI emits machine-readable UTF-8 JSON, including on Windows pipes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--anchor", nargs=3, metavar=("SOURCE_ID", "START", "END"))
    parser.add_argument("--output", type=Path, help="Save compiled internal state; no media or timeline is changed")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
        result = compile_plan(plan)
        if args.anchor:
            source_id, start, end = args.anchor
            result["anchor"] = map_anchor(plan, source_id, float(start), float(end))
        rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            if args.output.resolve() == args.plan.resolve() or (
                args.output.exists() and args.output.samefile(args.plan)
            ):
                raise SpeechPlanError("output must not overwrite the input plan")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"Speech plan error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
