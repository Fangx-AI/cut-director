#!/usr/bin/env python3
"""Validate an EHOrMdeO-calibrated Daily Magic Website episode plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REFERENCE_ID = "EHOrMdeO-master-v1"
REFERENCE_SHA256 = "EBBAC4B21E6DB3427602CAB71AE866B1FC18E2EA8C7A8A30025320A56A0E7AD0"

LAYOUT_MODES = [
    "type-stage",
    "logo-stage",
    "floating-proof-card",
    "immersive-ui-crop",
]

MOTION_RECIPES = [
    "staggered-line-drop",
    "badge-diagonal-peel",
    "hook-logo-collapse",
    "hand-drawn-pointer",
    "diagonal-page-curl",
    "stacked-bubble-pop",
    "radial-zoom-bridge",
    "focus-lens",
    "overzoom-settle",
    "hard-cut",
    "evidence-circle-draw",
    "scroll-focus",
    "return-state-settle",
]

BEAT_SPECS = [
    (
        "B01",
        "series-hook",
        50,
        80,
        {"type-stage"},
        {"staggered-line-drop", "badge-diagonal-peel"},
    ),
    (
        "B02",
        "identity-anchor",
        42,
        70,
        {"logo-stage"},
        {"hook-logo-collapse", "hand-drawn-pointer"},
    ),
    (
        "B03",
        "value-proof",
        70,
        120,
        {"floating-proof-card"},
        {"diagonal-page-curl", "stacked-bubble-pop"},
    ),
    (
        "B04",
        "navigation-proof",
        110,
        200,
        {"immersive-ui-crop"},
        {"radial-zoom-bridge", "focus-lens"},
    ),
    (
        "B05",
        "demo-run",
        300,
        480,
        {"floating-proof-card"},
        {"overzoom-settle", "hard-cut"},
    ),
    (
        "B06",
        "credibility-proof",
        70,
        125,
        {"immersive-ui-crop", "floating-proof-card"},
        {"radial-zoom-bridge", "evidence-circle-draw"},
    ),
    (
        "B07",
        "friction-proof",
        40,
        90,
        {"immersive-ui-crop", "floating-proof-card"},
        {"radial-zoom-bridge", "evidence-circle-draw"},
    ),
    (
        "B08",
        "access-path",
        120,
        210,
        {"floating-proof-card", "immersive-ui-crop"},
        {"scroll-focus", "radial-zoom-bridge", "focus-lens"},
    ),
    (
        "B09",
        "return-close",
        24,
        60,
        {"floating-proof-card"},
        {"return-state-settle"},
    ),
]

MATERIAL_TYPES = {
    "official-logo",
    "official-image",
    "official-video",
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

FINAL_QA_KEYS = [
    "referenceProfileVerified",
    "nineBeatOrderVerified",
    "realUiOnly",
    "claimsVerified",
    "layoutModesVerified",
    "motionRecipesVerified",
    "demoHardCutsVerified",
    "captionsVerified",
    "noEmptyOrUnreadableUi",
    "audioContinuityVerified",
    "finalProductStateVerified",
    "frameInspectionComplete",
]


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


def valid_url(value: object) -> bool:
    return str(value or "").startswith(("https://", "http://"))


def validate_reference(plan: dict, errors: list[str]) -> None:
    reference = require_dict(plan, "reference", errors)
    if reference.get("id") != REFERENCE_ID:
        errors.append(f"reference.id must be {REFERENCE_ID}")
    if reference.get("sha256") != REFERENCE_SHA256:
        errors.append("reference.sha256 does not match the approved master")
    if reference.get("matchMode") != "grammar-not-content":
        errors.append("reference.matchMode must be grammar-not-content")


def validate_format(plan: dict, errors: list[str]) -> int:
    fmt = require_dict(plan, "format", errors)
    expected = {
        "profile": "portrait-reference-v1",
        "width": 1080,
        "height": 1920,
        "fps": 30,
    }
    for key, value in expected.items():
        if fmt.get(key) != value:
            errors.append(f"format.{key} must be {value!r}")

    duration = fmt.get("durationFrames")
    if not isinstance(duration, int):
        errors.append("format.durationFrames must be an integer")
        return 0
    if not 900 <= duration <= 1350:
        errors.append("format.durationFrames must be between 900 and 1350")
    return duration


def validate_audio(plan: dict, errors: list[str]) -> None:
    audio = require_dict(plan, "audio", errors)
    if not str(audio.get("voiceProvider", "")).strip():
        errors.append("audio.voiceProvider is required")
    if not str(audio.get("voiceId", "")).strip():
        errors.append("audio.voiceId is required")
    if audio.get("continuousNarration") is not True:
        errors.append("audio.continuousNarration must be true")

    silence = audio.get("maxInternalSilenceMs")
    if not isinstance(silence, (int, float)) or not 0 <= silence <= 180:
        errors.append("audio.maxInternalSilenceMs must be between 0 and 180")

    loudness = audio.get("targetIntegratedLufs")
    if not isinstance(loudness, (int, float)) or not -14.5 <= loudness <= -11.0:
        errors.append("audio.targetIntegratedLufs must be between -14.5 and -11.0")

    speed = audio.get("maxVoiceSpeedRatio")
    if not isinstance(speed, (int, float)) or not 1.0 <= speed <= 1.15:
        errors.append("audio.maxVoiceSpeedRatio must be between 1.0 and 1.15")


def validate_visual_system(plan: dict, errors: list[str]) -> None:
    visual = require_dict(plan, "visualSystem", errors)
    if visual.get("layoutModes") != LAYOUT_MODES:
        errors.append(f"visualSystem.layoutModes must exactly equal {LAYOUT_MODES}")
    if visual.get("motionRecipes") != MOTION_RECIPES:
        errors.append(
            f"visualSystem.motionRecipes must exactly equal {MOTION_RECIPES}"
        )
    if visual.get("generatedProductUiAllowed") is not False:
        errors.append("visualSystem.generatedProductUiAllowed must be false")


def validate_website(plan: dict, errors: list[str]) -> None:
    website = require_dict(plan, "website", errors)
    for key in ("name", "audience", "oneSentenceValue", "sourceAccentColor"):
        if not str(website.get(key, "")).strip():
            errors.append(f"website.{key} is required")
    if not valid_url(website.get("url")):
        errors.append("website.url must be http(s)")
    color = str(website.get("sourceAccentColor", ""))
    if color and not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        errors.append("website.sourceAccentColor must be #RRGGBB")


def validate_claims(plan: dict, errors: list[str]) -> dict[str, dict]:
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
        label = claim_id or f"claims[{index}]"
        if not str(claim.get("text", "")).strip():
            errors.append(f"{label}.text is required")
        if not valid_url(claim.get("sourceUrl")):
            errors.append(f"{label}.sourceUrl must be http(s)")
        if claim.get("evidenceType") not in EVIDENCE_TYPES:
            errors.append(f"{label}.evidenceType is invalid")
        if not str(claim.get("capturedAt", "")).strip():
            errors.append(f"{label}.capturedAt is required")
        if claim.get("evidenceCaptured") is not True:
            errors.append(f"{label}.evidenceCaptured must be true")
    return claim_map


def validate_materials(plan: dict, errors: list[str]) -> dict[str, dict]:
    materials = require_list(plan, "materials", errors)
    material_map: dict[str, dict] = {}
    product_ui_count = 0
    recording_count = 0

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
        label = material_id or f"materials[{index}]"

        material_type = material.get("type")
        if material_type not in MATERIAL_TYPES:
            errors.append(f"{label}.type is invalid")
        if material_type in {"browser-recording", "official-video"}:
            recording_count += 1
        if material.get("containsProductUi") is True:
            product_ui_count += 1
        if material.get("synthetic") is not False:
            errors.append(f"{label}.synthetic must be false")
        if material.get("provenanceVerified") is not True:
            errors.append(f"{label}.provenanceVerified must be true")
        if not str(material.get("rightsStatus", "")).strip():
            errors.append(f"{label}.rightsStatus is required")
        if not str(material.get("capturedAt", "")).strip():
            errors.append(f"{label}.capturedAt is required")
        if not (
            valid_url(material.get("sourceUrl"))
            or str(material.get("localPath", "")).strip()
        ):
            errors.append(f"{label} needs sourceUrl or localPath")

    if product_ui_count < 4:
        errors.append("materials must contain at least four real product-UI assets")
    if recording_count < 3:
        errors.append("materials must contain at least three real recordings/videos")
    return material_map


def validate_demo_clips(
    beat: dict,
    material_map: dict[str, dict],
    errors: list[str],
) -> None:
    clips = beat.get("demoClips")
    if not isinstance(clips, list) or not 3 <= len(clips) <= 5:
        errors.append("B05.demoClips must contain three to five clips")
        return

    expected_start = beat.get("startFrame")
    for index, clip in enumerate(clips):
        label = f"B05.demoClips[{index}]"
        if not isinstance(clip, dict):
            errors.append(f"{label} must be an object")
            continue
        if clip.get("startFrame") != expected_start:
            errors.append(f"{label} must be contiguous with the previous clip")
        start = clip.get("startFrame")
        end = clip.get("endFrame")
        if not isinstance(start, int) or not isinstance(end, int) or end <= start:
            errors.append(f"{label} has an invalid frame range")
        else:
            if not 30 <= end - start <= 180:
                errors.append(f"{label} must last 30–180 frames")
            expected_start = end
        source_ref = str(clip.get("sourceRef", "")).strip()
        if source_ref not in material_map:
            errors.append(f"{label}.sourceRef must reference a material")
        if not str(clip.get("caption", "")).strip():
            errors.append(f"{label}.caption is required")
        expected_join = "opening" if index == 0 else "hard-cut"
        if clip.get("join") != expected_join:
            errors.append(f"{label}.join must be {expected_join}")

    if expected_start != beat.get("endFrame"):
        errors.append("B05.demoClips must fill the complete B05 frame range")


def validate_beats(
    plan: dict,
    duration: int,
    claim_map: dict[str, dict],
    material_map: dict[str, dict],
    errors: list[str],
) -> None:
    beats = require_list(plan, "beats", errors)
    if len(beats) != len(BEAT_SPECS):
        errors.append("beats must contain exactly B01–B09")

    expected_start = 0
    for index, spec in enumerate(BEAT_SPECS):
        beat_id, family, minimum, maximum, layouts, motions = spec
        if index >= len(beats) or not isinstance(beats[index], dict):
            errors.append(f"missing valid beat {beat_id}")
            continue
        beat = beats[index]

        if beat.get("id") != beat_id:
            errors.append(f"beats[{index}].id must be {beat_id}")
        if beat.get("family") != family:
            errors.append(f"{beat_id}.family must be {family}")

        start = beat.get("startFrame")
        end = beat.get("endFrame")
        if start != expected_start:
            errors.append(f"{beat_id}.startFrame must be {expected_start}")
        if not isinstance(start, int) or not isinstance(end, int) or end <= start:
            errors.append(f"{beat_id} has an invalid frame range")
        else:
            beat_duration = end - start
            if not minimum <= beat_duration <= maximum:
                errors.append(
                    f"{beat_id} duration must be {minimum}–{maximum} frames "
                    f"(got {beat_duration})"
                )
            expected_start = end

        if beat.get("layoutMode") not in layouts:
            errors.append(
                f"{beat_id}.layoutMode must be one of {sorted(layouts)}"
            )

        recipes = beat.get("motionRecipes")
        if not isinstance(recipes, list) or not recipes:
            errors.append(f"{beat_id}.motionRecipes must be a non-empty array")
        else:
            unknown = set(recipes) - motions
            if unknown:
                errors.append(
                    f"{beat_id} contains disallowed motion recipes: "
                    + ", ".join(sorted(unknown))
                )
            if len(recipes) != len(set(recipes)):
                errors.append(f"{beat_id}.motionRecipes must not contain duplicates")

        for key in ("viewerJob", "voiceover", "onScreenText"):
            if not str(beat.get(key, "")).strip():
                errors.append(f"{beat_id}.{key} is required")

        source_refs = beat.get("sourceRefs")
        if not isinstance(source_refs, list):
            errors.append(f"{beat_id}.sourceRefs must be an array")
        else:
            if beat_id != "B01" and not source_refs:
                errors.append(f"{beat_id}.sourceRefs must not be empty")
            for source_ref in source_refs:
                if source_ref not in material_map:
                    errors.append(
                        f"{beat_id}.sourceRefs contains unknown material {source_ref}"
                    )

        claim_ids = beat.get("claimIds")
        if not isinstance(claim_ids, list):
            errors.append(f"{beat_id}.claimIds must be an array")
        else:
            for claim_id in claim_ids:
                if claim_id not in claim_map:
                    errors.append(f"{beat_id} references unknown claim {claim_id}")

        if beat_id in {"B06", "B07"} and not claim_ids:
            errors.append(f"{beat_id} must reference at least one verified claim")
        if beat_id == "B05":
            validate_demo_clips(beat, material_map, errors)

    if expected_start != duration:
        errors.append(
            f"beats must end at format.durationFrames ({duration}), got {expected_start}"
        )


def validate_final(plan: dict, errors: list[str]) -> None:
    qa = require_dict(plan, "qa", errors)
    delivery = require_dict(plan, "delivery", errors)

    for key in FINAL_QA_KEYS:
        if qa.get(key) is not True:
            errors.append(f"qa.{key} must be true for final stage")

    for key in ("projectId", "timelineId", "timelineName"):
        if not str(delivery.get(key, "")).strip():
            errors.append(f"delivery.{key} is required for final stage")

    verified_frames = delivery.get("verifiedFrames")
    if not isinstance(verified_frames, list) or len(verified_frames) < 14:
        errors.append(
            "delivery.verifiedFrames must contain at least 14 frames for final stage"
        )
    if delivery.get("status") not in {"review", "approved", "exported"}:
        errors.append(
            "delivery.status must be review, approved, or exported for final stage"
        )


def validate(plan: dict, stage: str) -> list[str]:
    errors: list[str] = []

    if plan.get("schemaVersion") != 2:
        errors.append("schemaVersion must be 2")
    if plan.get("series") != "daily-magic-website":
        errors.append("series must be daily-magic-website")
    if not str(plan.get("episodeId", "")).strip():
        errors.append("episodeId is required")

    validate_reference(plan, errors)
    validate_website(plan, errors)
    duration = validate_format(plan, errors)
    validate_audio(plan, errors)
    validate_visual_system(plan, errors)
    claim_map = validate_claims(plan, errors)
    material_map = validate_materials(plan, errors)
    validate_beats(plan, duration, claim_map, material_map, errors)

    require_dict(plan, "qa", errors)
    require_dict(plan, "delivery", errors)
    if stage == "final":
        validate_final(plan, errors)

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
