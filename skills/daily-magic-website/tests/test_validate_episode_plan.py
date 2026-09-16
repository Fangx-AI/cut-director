from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_episode_plan.py"
TEMPLATE_PATH = SKILL_DIR / "assets" / "episode-plan.template.json"

SPEC = importlib.util.spec_from_file_location("daily_magic_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def load_plan() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


class ValidatorTests(unittest.TestCase):
    def test_template_passes_plan_stage(self) -> None:
        self.assertEqual([], VALIDATOR.validate(load_plan(), "plan"))

    def test_rejects_landscape_format(self) -> None:
        plan = load_plan()
        plan["format"]["width"] = 1920
        plan["format"]["height"] = 1080
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any("format.width" in error for error in errors))
        self.assertTrue(any("format.height" in error for error in errors))

    def test_rejects_unapproved_motion_recipe(self) -> None:
        plan = load_plan()
        plan["beats"][3]["motionRecipes"].append("random-3d-spin")
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any("disallowed motion recipes" in error for error in errors))

    def test_rejects_synthetic_product_ui(self) -> None:
        plan = load_plan()
        plan["materials"][2]["synthetic"] = True
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any("synthetic must be false" in error for error in errors))

    def test_rejects_noncontiguous_beats(self) -> None:
        plan = load_plan()
        plan["beats"][4]["startFrame"] += 1
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any("B05.startFrame" in error for error in errors))

    def test_rejects_demo_transition(self) -> None:
        plan = load_plan()
        plan["beats"][4]["demoClips"][2]["join"] = "cross-dissolve"
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any(".join must be hard-cut" in error for error in errors))

    def test_final_requires_qa_and_delivery(self) -> None:
        errors = VALIDATOR.validate(load_plan(), "final")
        self.assertTrue(any("qa.referenceProfileVerified" in error for error in errors))
        self.assertTrue(any("delivery.projectId" in error for error in errors))
        self.assertTrue(any("verifiedFrames" in error for error in errors))

    def test_complete_final_plan_passes(self) -> None:
        plan = copy.deepcopy(load_plan())
        for key in plan["qa"]:
            plan["qa"][key] = True
        plan["delivery"].update(
            {
                "projectId": "project-1",
                "timelineId": "timeline-1",
                "timelineName": "每日神器网站｜000｜示例网站｜EHOrMdeO-v1",
                "verifiedFrames": list(range(14)),
                "status": "review",
            }
        )
        self.assertEqual([], VALIDATOR.validate(plan, "final"))


if __name__ == "__main__":
    unittest.main()
