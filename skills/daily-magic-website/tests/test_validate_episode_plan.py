import importlib.util
import json
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_episode_plan.py"
TEMPLATE_PATH = SKILL_DIR / "assets" / "episode-plan.template.json"

SPEC = importlib.util.spec_from_file_location("episode_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


def load_template():
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


class EpisodePlanValidationTests(unittest.TestCase):
    def test_template_passes_plan_stage(self):
        self.assertEqual(VALIDATOR.validate(load_template(), "plan"), [])

    def test_rejects_random_timing_change(self):
        plan = load_template()
        plan["shots"][2]["startFrame"] = 218
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(any("S03 must span frames" in error for error in errors))

    def test_rejects_generated_product_ui(self):
        plan = load_template()
        plan["visualSystem"]["generatedProductUiAllowed"] = True
        errors = VALIDATOR.validate(plan, "plan")
        self.assertIn(
            "visualSystem.generatedProductUiAllowed must be false",
            errors,
        )

    def test_rejects_unverified_claim(self):
        plan = load_template()
        plan["claims"][0]["evidenceCaptured"] = False
        errors = VALIDATOR.validate(plan, "plan")
        self.assertTrue(
            any("evidenceCaptured must be true" in error for error in errors)
        )

    def test_final_stage_requires_completed_qa(self):
        errors = VALIDATOR.validate(load_template(), "final")
        self.assertTrue(any(error.startswith("qa.") for error in errors))
        self.assertTrue(any(error.startswith("delivery.") for error in errors))

    def test_completed_template_passes_final_stage(self):
        plan = load_template()
        plan["masterReference"].update(
            {
                "status": "approved",
                "referenceId": "timeline-master-v1",
                "approvedAt": "2026-07-27",
            }
        )
        for key in VALIDATOR.FINAL_QA_KEYS:
            plan["qa"][key] = True
        plan["delivery"].update(
            {
                "projectId": "project-123",
                "timelineId": "timeline-123",
                "timelineName": "每日神器网站 000｜示例网站｜Master V1",
                "verifiedFrames": [45, 150, 285, 435, 570, 675, 719],
                "status": "review",
            }
        )
        self.assertEqual(VALIDATOR.validate(plan, "final"), [])


if __name__ == "__main__":
    unittest.main()
