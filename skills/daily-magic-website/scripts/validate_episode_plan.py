#!/usr/bin/env python3
"""Validate a Daily Magic Website Master V1 episode plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SHOT_SPECS = [
    ("S01", "hook", 0, 90, 28, 14),
    ("S02", "identity-proof", 90, 210, 36, 16),
    ("S03", "core-operation", 210, 360, 38, 16),
    ("S04", "concrete-result", 360, 510, 38, 16),
    ("S05", "audience-value", 510, 630, 32, 18),
    ("S06", "clean-close", 630, 720, 26, 18),
]

FLOW_VARIANTS = {
    "browse-filter-detail",
    "input-action-result",
    "query-filter-result",
    "input-progress-output",
    "overview-example-detail",
}

MATERIAL_TYPES = {
    "official-video",
    "official-image",
    "browser-screenshot",
    "browser-recording",
    "user-provided",
}

EVIDENCE_TYPES = {
    "official-page",
    "official-media",
    "official-docs",
    "user-provided",
}

MOTION_SET = ["hard-cut", "masked-push", "focus-lock", "slow-crop"]

FINAL_QA_KEYS = [
    "sixShotsVerified",
    "realUiOnly",
    "claimsVerified",
    "operationResultMatch",
    "typographySafe",
    "singleAccent",
    "motionSetCompliant",
    "noClippingOrEmptyUi",
    "finalUrlHoldVerified",
    "dayiSegmentsVerified",
    "shotBoundariesVerified",
]


def text_units(value: str) -> int:
    """Use a conservative, deterministic visible-character count."""
    return len("".join(str(value).split()))


def require_dict(parent: dict, key: str, errors: list[str]) -> dict:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_list(parent: dict, key: str, errors: list[str]) -> list:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be an array")
        return []
    return value


def validate(plan: dict, stage: str) -> list[str]:
    errors: list[str] = []

    if plan.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if plan.get("series") != "daily-magic-website":
        errors.append("series must be daily-magic-website")
    if plan.get("masterVersion") != "daily-magic-website-v1":
        errors.append("masterVersion must be daily-magic-website-v1")
    master_reference = require_dict(plan, "masterReference", errors)
    if master_reference.get("status") not in {"provisional", "approved"}:
        errors.append("masterReference.status must be provisional or approved")
    if master_reference.get("referenceType") not in {
        "chatcut-timeline",
        "exported-video",
    }:
        errors.append(
            "masterReference.referenceType must be chatcut-timeline or exported-video"
        )
    if not str(plan.get("episodeId", "")).strip():
        errors.append("episodeId is required")

    website = require_dict(plan, "website", errors)
    for key in ("name", "url", "audience", "oneSentenceValue", "accentColor"):
        if not str(website.get(key, "")).strip():
            errors.append(f"website.{key} is required")
    if website.get("url") and not str(website["url"]).startswith(("http://", "https://")):
        errors.append("website.url must be http(s)")
    accent = str(website.get("accentColor", ""))
    if accent and (len(accent) != 7 or not accent.startswith("#")):
        errors.append("website.accentColor must be #RRGGBB")

    fmt = require_dict(plan, "format", errors)
    expected_format = {
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "durationFrames": 720,
        "voiceProvider": "doubao",
        "voiceId": "dayi",
        "voiceSpeedRatioMax": 1.18,
    }
    for key, expected in expected_format.items():
        if fmt.get(key) != expected:
            errors.append(f"format.{key} must be {expected!r}")

    visual = require_dict(plan, "visualSystem", errors)
    if visual.get("fontFamily") != "Smiley Sans":
        errors.append("visualSystem.fontFamily must be Smiley Sans")
    if visual.get("paletteMode") != "source-native-single-accent":
        errors.append(
            "visualSystem.paletteMode must be source-native-single-accent"
        )
    if visual.get("motionSet") != MOTION_SET:
        errors.append(f"visualSystem.motionSet must exactly equal {MOTION_SET}")
    if visual.get("generatedProductUiAllowed") is not False:
        errors.append("visualSystem.generatedProductUiAllowed must be false")

    if plan.get("flowVariant") not in FLOW_VARIANTS:
        errors.append(
            "flowVariant must be one of " + ", ".join(sorted(FLOW_VARIANTS))
        )

    claims = require_list(plan, "claims", errors)
    claim_map: dict[str, dict] = {}
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] must be an object")
            continue
        claim_id = str(claim.get("id", "")).strip()
        if not claim_id:
            errors.append(f"claims[{index}].id is required")
        elif claim_id in claim_map:
            errors.append(f"duplicate claim id {claim_id}")
        else:
            claim_map[claim_id] = claim
        if not str(claim.get("text", "")).strip():
            errors.append(f"claim {claim_id or index} text is required")
        source_url = str(claim.get("sourceUrl", ""))
        if not source_url.startswith(("http://", "https://")):
            errors.append(f"claim {claim_id or index} sourceUrl must be http(s)")
        if claim.get("evidenceType") not in EVIDENCE_TYPES:
            errors.append(f"claim {claim_id or index} has invalid evidenceType")
        if claim.get("evidenceCaptured") is not True:
            errors.append(f"claim {claim_id or index} evidenceCaptured must be true")

    materials = require_list(plan, "materials", errors)
    material_map: dict[str, dict] = {}
    for index, material in enumerate(materials):
        if not isinstance(material, dict):
            errors.append(f"materials[{index}] must be an object")
            continue
        material_id = str(material.get("id", "")).strip()
        if not material_id:
            errors.append(f"materials[{index}].id is required")
        elif material_id in material_map:
            errors.append(f"duplicate material id {material_id}")
        else:
            material_map[material_id] = material
        if material.get("type") not in MATERIAL_TYPES:
            errors.append(f"material {material_id or index} has invalid type")
        if material.get("provenanceVerified") is not True:
            errors.append(
                f"material {material_id or index} provenanceVerified must be true"
            )
        if not str(material.get("rightsStatus", "")).strip():
            errors.append(f"material {material_id or index} rightsStatus is required")
        if not (
            str(material.get("sourceUrl", "")).strip()
            or str(material.get("localPath", "")).strip()
        ):
            errors.append(
                f"material {material_id or index} needs sourceUrl or localPath"
            )

    shots = require_list(plan, "shots", errors)
    if len(shots) != len(SHOT_SPECS):
        errors.append("shots must contain exactly S01-S06")
    for index, spec in enumerate(SHOT_SPECS):
        shot_id, job, start, end, voice_max, text_max = spec
        if index >= len(shots) or not isinstance(shots[index], dict):
            errors.append(f"missing valid shot {shot_id}")
            continue
        shot = shots[index]
        if shot.get("id") != shot_id:
            errors.append(f"shots[{index}].id must be {shot_id}")
        if shot.get("job") != job:
            errors.append(f"{shot_id}.job must be {job}")
        if shot.get("startFrame") != start or shot.get("endFrame") != end:
            errors.append(f"{shot_id} must span frames {start}-{end - 1}")
        source_ref = str(shot.get("sourceRef", "")).strip()
        if source_ref not in material_map:
            errors.append(f"{shot_id}.sourceRef must reference a material")
        voiceover = str(shot.get("voiceover", "")).strip()
        if not voiceover:
            errors.append(f"{shot_id}.voiceover is required")
        elif text_units(voiceover) > voice_max:
            errors.append(
                f"{shot_id}.voiceover exceeds {voice_max} units "
                f"({text_units(voiceover)})"
            )
        onscreen = str(shot.get("onScreenText", "")).strip()
        if not onscreen:
            errors.append(f"{shot_id}.onScreenText is required")
        elif text_units(onscreen) > text_max:
            errors.append(
                f"{shot_id}.onScreenText exceeds {text_max} units "
                f"({text_units(onscreen)})"
            )
        claim_ids = shot.get("claimIds")
        if not isinstance(claim_ids, list):
            errors.append(f"{shot_id}.claimIds must be an array")
        else:
            for claim_id in claim_ids:
                if claim_id not in claim_map:
                    errors.append(f"{shot_id} references unknown claim {claim_id}")

    qa = require_dict(plan, "qa", errors)
    delivery = require_dict(plan, "delivery", errors)
    if stage == "final":
        if master_reference.get("status") != "approved":
            errors.append("masterReference.status must be approved for final stage")
        if not str(master_reference.get("referenceId", "")).strip():
            errors.append("masterReference.referenceId is required for final stage")
        if not str(master_reference.get("approvedAt", "")).strip():
            errors.append("masterReference.approvedAt is required for final stage")
        for key in FINAL_QA_KEYS:
            if qa.get(key) is not True:
                errors.append(f"qa.{key} must be true for final stage")
        for key in ("projectId", "timelineId", "timelineName"):
            if not str(delivery.get(key, "")).strip():
                errors.append(f"delivery.{key} is required for final stage")
        verified_frames = delivery.get("verifiedFrames")
        if not isinstance(verified_frames, list) or len(verified_frames) < 7:
            errors.append(
                "delivery.verifiedFrames must contain at least 7 frames for final stage"
            )
        if delivery.get("status") not in {"review", "approved", "exported"}:
            errors.append(
                "delivery.status must be review, approved, or exported for final stage"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--stage", choices=("plan", "final"), default="plan")
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: plan not found: {args.plan}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(plan, args.stage)
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS: {args.stage} validation succeeded for "
        f"{plan['episodeId']} / {plan['website']['name']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
