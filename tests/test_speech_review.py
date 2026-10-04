import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.evaluate_speech_review import ReviewError, compare_reviews, input_packet, score_review


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/speech/review-cases.json"


class SpeechReviewTest(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.response = {
            "version": "1.0", "cases": [{
                "case_id": case["case_id"], "audio_verified": False, "next_step": "Text-only proposal.",
                "decisions": [{"unit_id": rule["unit_id"], "action": rule["acceptable"][0],
                               "reason": "Synthetic scorer fixture, not a model response."}
                              for rule in case["expected"]],
            } for case in self.fixture["cases"]],
        }

    def test_reference_actions_pass_without_media_claim(self):
        report = score_review(self.fixture, self.response)
        self.assertEqual(report["cases_passed"], 8)
        self.assertEqual(report["correct_units"], report["unit_count"])
        self.assertEqual(report["critical_errors"], 0)
        self.assertFalse(report["media_verified"])

    def test_agent_packet_has_inputs_but_no_answer_keys(self):
        packet = input_packet(self.fixture)
        self.assertEqual(len(packet["cases"]), 8)
        for case in packet["cases"]:
            self.assertEqual(set(case), {"case_id", "request", "context", "units"})
        self.assertIn("expected", self.fixture["cases"][0])

    def test_false_audio_claim_is_a_critical_failure(self):
        self.response["cases"][0]["audio_verified"] = True
        report = score_review(self.fixture, self.response)
        self.assertEqual(report["critical_errors"], 1)
        self.assertEqual(report["cases_passed"], 7)
        self.assertFalse(report["media_verified"])

    def test_deleting_a_qualifier_is_a_critical_error(self):
        self.response["cases"][2]["decisions"][-1]["action"] = "cut"
        report = score_review(self.fixture, self.response)
        self.assertEqual(report["critical_errors"], 1)
        self.assertEqual(report["correct_units"], report["unit_count"] - 1)

    def test_missed_production_aside_is_not_confused_with_overcutting(self):
        self.response["cases"][4]["decisions"][1]["action"] = "keep"
        report = score_review(self.fixture, self.response)
        self.assertEqual(report["critical_errors"], 0)
        self.assertEqual(report["cases_passed"], 7)

    def test_multiple_valid_editorial_choices_are_accepted(self):
        self.response["cases"][3]["decisions"][0]["action"] = "cut"
        self.response["cases"][3]["decisions"][-1]["action"] = "review"
        self.assertEqual(score_review(self.fixture, self.response)["cases_passed"], 8)

    def test_missing_unknown_and_duplicate_cases_are_rejected(self):
        for operation in ("missing", "unknown", "duplicate"):
            with self.subTest(operation=operation):
                response = copy.deepcopy(self.response)
                if operation == "missing":
                    response["cases"].pop()
                elif operation == "unknown":
                    response["cases"][0]["case_id"] = "invented"
                else:
                    response["cases"].append(copy.deepcopy(response["cases"][0]))
                with self.assertRaises(ReviewError):
                    score_review(self.fixture, response)

    def test_missing_unknown_and_duplicate_units_are_rejected(self):
        for operation in ("missing", "unknown", "duplicate"):
            with self.subTest(operation=operation):
                response = copy.deepcopy(self.response)
                decisions = response["cases"][0]["decisions"]
                if operation == "missing":
                    decisions.pop()
                elif operation == "unknown":
                    decisions[0]["unit_id"] = "invented"
                else:
                    decisions.append(copy.deepcopy(decisions[0]))
                with self.assertRaises(ReviewError):
                    score_review(self.fixture, response)

    def test_invalid_actions_types_and_empty_reasons_are_rejected(self):
        for field, value in (("action", "rewrite"), ("action", []), ("reason", "")):
            with self.subTest(field=field):
                response = copy.deepcopy(self.response)
                response["cases"][0]["decisions"][0][field] = value
                with self.assertRaises(ReviewError):
                    score_review(self.fixture, response)
        self.response["cases"][0]["audio_verified"] = "false"
        with self.assertRaises(ReviewError):
            score_review(self.fixture, self.response)

    def test_invalid_answer_keys_and_non_synthetic_sources_are_rejected(self):
        for mutation in ("coverage", "contradiction", "action", "source"):
            with self.subTest(mutation=mutation):
                fixture = copy.deepcopy(self.fixture)
                rule = fixture["cases"][0]["expected"][0]
                if mutation == "coverage":
                    rule["unit_id"] = "invented"
                elif mutation == "contradiction":
                    rule["critical_actions"] = rule["acceptable"][:]
                elif mutation == "action":
                    rule["acceptable"] = ["rewrite"]
                else:
                    fixture["source_type"] = "real_media"
                with self.assertRaises(ReviewError):
                    input_packet(fixture)

    def test_comparison_reports_a_tie_without_inventing_improvement(self):
        report = compare_reviews(self.fixture, self.response, copy.deepcopy(self.response))
        self.assertEqual(report["cutdirector_minus_baseline"], {
            "correct_units": 0, "cases_passed": 0, "critical_errors": 0,
        })
        self.assertFalse(report["media_verified"])

    def test_comparison_direction_matches_actual_errors(self):
        worse = copy.deepcopy(self.response)
        worse["cases"][0]["decisions"][1]["action"] = "cut"
        report = compare_reviews(self.fixture, self.response, worse)
        self.assertEqual(report["cutdirector_minus_baseline"]["correct_units"], -1)
        self.assertEqual(report["cutdirector_minus_baseline"]["critical_errors"], 1)

    def test_saved_independent_responses_reproduce_the_recorded_tie(self):
        records = ROOT / "tests/records/speech-review-2026-10-04"
        responses = [json.loads((records / name).read_text(encoding="utf-8"))
                     for name in ("baseline.json", "cutdirector.json")]
        report = compare_reviews(self.fixture, *responses)
        for label in ("baseline", "cutdirector"):
            self.assertEqual(report[label]["unit_count"], 34)
            self.assertEqual(report[label]["correct_units"], 34)
            self.assertEqual(report[label]["cases_passed"], 8)
            self.assertEqual(report[label]["critical_errors"], 0)
            self.assertEqual(report[label]["review_units"], 3)
        self.assertTrue(all(value == 0 for value in report["cutdirector_minus_baseline"].values()))
        self.assertFalse(report["media_verified"])

    def test_unknown_fields_versions_and_empty_case_arrays_are_rejected(self):
        for field, value in (("version", "2.0"), ("cases", []), ("unexpected", True)):
            with self.subTest(field=field):
                response = copy.deepcopy(self.response)
                response[field] = value
                with self.assertRaises(ReviewError):
                    score_review(self.fixture, response)

    def test_cli_packet_is_utf8_and_does_not_mutate_fixture(self):
        before = FIXTURE.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_speech_review.py"),
                                 str(FIXTURE), "--packet"], capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("expected", json.loads(result.stdout)["cases"][0])
        self.assertEqual(FIXTURE.read_bytes(), before)

    def test_cli_invalid_review_writes_no_report_and_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            response_path = Path(temporary) / "response.json"
            output_path = Path(temporary) / "report.json"
            response_path.write_text("{}", encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_speech_review.py"),
                                     str(FIXTURE), "--baseline", str(response_path),
                                     "--cutdirector", str(response_path), "--output", str(output_path)],
                                    capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertFalse(output_path.exists())
            self.assertEqual(response_path.read_text(encoding="utf-8"), "{}")

    def test_cli_output_cannot_overwrite_a_response(self):
        with tempfile.TemporaryDirectory() as temporary:
            response_path = Path(temporary) / "response.json"
            response_path.write_text(json.dumps(self.response), encoding="utf-8")
            before = response_path.read_bytes()
            result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_speech_review.py"),
                                     str(FIXTURE), "--baseline", str(response_path),
                                     "--cutdirector", str(response_path), "--output", str(response_path)],
                                    capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertIn("must not overwrite", result.stderr)
            self.assertEqual(response_path.read_bytes(), before)

    def test_cli_success_matches_saved_responses_without_modifying_them(self):
        records = ROOT / "tests/records/speech-review-2026-10-04"
        paths = [records / name for name in ("baseline.json", "cutdirector.json")]
        before = [path.read_bytes() for path in paths]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "nested/report.json"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_speech_review.py"),
                                     str(FIXTURE), "--baseline", str(paths[0]),
                                     "--cutdirector", str(paths[1]), "--output", str(output)],
                                    capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report, json.loads(result.stdout))
            self.assertEqual(report["baseline"]["correct_units"], 34)
            self.assertFalse(report["media_verified"])
        self.assertEqual([path.read_bytes() for path in paths], before)


if __name__ == "__main__":
    unittest.main()
