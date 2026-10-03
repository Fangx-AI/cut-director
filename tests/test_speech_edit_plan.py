import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.speech_edit_plan import SpeechPlanError, compile_plan, map_anchor


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/speech/natural-cleanup.json"


class SpeechEditPlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_known_edit_is_contiguous_and_duration_matches_retained_source(self):
        result = compile_plan(self.plan)
        self.assertAlmostEqual(result["duration"], 5.9)
        segments = result["segments"]
        self.assertEqual(segments[0]["timeline_start"], 0)
        for previous, current in zip(segments, segments[1:]):
            self.assertEqual(previous["timeline_end"], current["timeline_start"])
        self.assertFalse(result["media_verified"])
        self.assertTrue(result["sources"][0]["word_boundaries_checked"])

    def test_removal_offsets_later_keyword_and_gesture_anchor(self):
        mapped = map_anchor(self.plan, "camera-a", 7.2, 8.6)
        self.assertEqual(mapped["spans"][0]["timeline_start"], 4.1)
        self.assertEqual(mapped["spans"][0]["timeline_end"], 5.5)
        self.assertTrue(mapped["fully_retained"])
        self.assertFalse(mapped["requires_reanchor"])

    def test_removed_failed_take_has_no_live_animation_anchor(self):
        mapped = map_anchor(self.plan, "camera-a", 3.5, 4.2)
        self.assertEqual(mapped["spans"], [])
        self.assertFalse(mapped["fully_retained"])
        self.assertTrue(mapped["requires_reanchor"])

    def test_partially_deleted_anchor_does_not_silently_use_first_fragment(self):
        mapped = map_anchor(self.plan, "camera-a", 3, 6.2)
        self.assertEqual(len(mapped["spans"]), 2)
        self.assertFalse(mapped["fully_retained"])
        self.assertTrue(mapped["requires_reanchor"])

    def test_full_anchor_across_separate_keeps_still_requires_review(self):
        self.plan["keep"].insert(1, {"segment_id": "extra", "source_id": "camera-a", "start": 3.5, "end": 5.2})
        self.plan["cuts"] = []
        mapped = map_anchor(self.plan, "camera-a", 3, 6.2)
        self.assertTrue(mapped["fully_retained"])
        self.assertTrue(mapped["requires_reanchor"])

    def test_supplied_chinese_words_and_emphasis_are_not_automatically_deleted(self):
        for start, end in ((1.5, 2.4), (3, 3.4), (7.2, 8.6)):
            self.assertFalse(map_anchor(self.plan, "camera-a", start, end)["requires_reanchor"])
        self.assertEqual(self.plan["sources"][0]["words"][2]["text"], "免费额度")

    def test_start_or_end_inside_a_trusted_word_is_rejected(self):
        for boundary in ("start", "end"):
            with self.subTest(boundary=boundary):
                plan = copy.deepcopy(self.plan)
                plan["keep"][0][boundary] = 1.8
                with self.assertRaisesRegex(SpeechPlanError, "splits word w3"):
                    compile_plan(plan)

    def test_explicit_cut_cannot_split_a_word_or_overlap_retained_speech(self):
        for start, end, error in ((0.3, 0.6, "splits word"), (1, 1.4, "overlaps kept")):
            with self.subTest(start=start):
                self.plan["cuts"][0].update(start=start, end=end)
                with self.assertRaisesRegex(SpeechPlanError, error):
                    compile_plan(self.plan)

    def test_missing_words_discloses_unchecked_boundaries(self):
        del self.plan["sources"][0]["words"]
        self.assertFalse(compile_plan(self.plan)["sources"][0]["word_boundaries_checked"])

    def test_out_of_bounds_zero_length_and_nonfinite_times_are_rejected(self):
        for start, end in ((-1, 2), (1, 11), (1, 1), (float("nan"), 2), (1, float("inf")), (True, 2), (1, 10 ** 400)):
            with self.subTest(start=start, end=end):
                plan = copy.deepcopy(self.plan)
                plan["keep"][0].update(start=start, end=end)
                with self.assertRaises(SpeechPlanError):
                    compile_plan(plan)

    def test_duplicate_ids_unknown_sources_and_overlaps_are_rejected(self):
        invalid = []
        duplicate = copy.deepcopy(self.plan)
        duplicate["keep"][1]["segment_id"] = "setup"
        invalid.append(duplicate)
        unknown = copy.deepcopy(self.plan)
        unknown["keep"][1]["source_id"] = "missing"
        invalid.append(unknown)
        overlap = copy.deepcopy(self.plan)
        overlap["keep"][1].update(start=3, end=6.5)
        invalid.append(overlap)
        for plan in invalid:
            with self.subTest(plan=plan["keep"]):
                with self.assertRaises(SpeechPlanError):
                    compile_plan(plan)

    def test_reordering_requires_explicit_plan_intent_and_reason(self):
        self.plan["keep"].reverse()
        with self.assertRaisesRegex(SpeechPlanError, "source order changed"):
            compile_plan(self.plan)
        self.plan["allow_reorder"] = True
        with self.assertRaisesRegex(SpeechPlanError, "reorder_reason"):
            compile_plan(self.plan)
        self.plan["reorder_reason"] = "User requested emphasis first."
        self.assertEqual(compile_plan(self.plan)["segments"][0]["segment_id"], "emphasis")

    def test_multiple_sources_follow_import_order_and_map_independently(self):
        self.plan["sources"].append({"source_id": "camera-b", "duration": 3})
        self.plan["keep"].append({"segment_id": "closing", "source_id": "camera-b", "start": 1, "end": 3})
        mapped = map_anchor(self.plan, "camera-b", 1.5, 2.5)
        self.assertEqual(mapped["spans"][0]["timeline_start"], 6.4)
        self.assertEqual(mapped["spans"][0]["timeline_end"], 7.4)
        self.assertEqual(compile_plan(self.plan)["duration"], 7.9)

    def test_omitted_ranges_are_reported_even_without_explicit_cut_notes(self):
        self.plan["cuts"] = []
        self.assertEqual(compile_plan(self.plan)["sources"][0]["removed_ranges"], [
            {"start": 0, "end": 0.9}, {"start": 3.5, "end": 5.2},
            {"start": 6.5, "end": 7}, {"start": 9, "end": 10},
        ])

    def test_unsupported_speed_and_effect_fields_fail_instead_of_mismapping(self):
        for field, value in (("rate", 2), ("speed", 2), ("transition", "crossfade")):
            with self.subTest(field=field):
                plan = copy.deepcopy(self.plan)
                plan["keep"][0][field] = value
                with self.assertRaises(SpeechPlanError):
                    compile_plan(plan)

    def test_new_revision_changes_map_and_never_mutates_the_input(self):
        original = copy.deepcopy(self.plan)
        compile_plan(self.plan)
        self.assertEqual(self.plan, original)
        self.plan["revision"] = "roughcut-002"
        self.plan["keep"][0]["end"] = 3
        mapped = map_anchor(self.plan, "camera-a", 7.2, 8.6)
        self.assertEqual(mapped["revision"], "roughcut-002")
        self.assertEqual(mapped["spans"][0]["timeline_start"], 3.6)

    def test_unknown_or_invalid_anchor_is_rejected(self):
        for source_id, start, end in (("wrong", 1, 2), ("camera-a", 8, 7), ("camera-a", 0, 11)):
            with self.subTest(source_id=source_id, start=start):
                with self.assertRaises(SpeechPlanError):
                    map_anchor(self.plan, source_id, start, end)

    def test_cli_outputs_current_mapping_and_does_not_modify_source_plan(self):
        original = FIXTURE.read_bytes()
        result = subprocess.run([
            sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(FIXTURE),
            "--anchor", "camera-a", "7.2", "8.6",
        ], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["anchor"]["spans"][0]["timeline_start"], 4.1)
        self.assertEqual(FIXTURE.read_bytes(), original)

    def test_cli_rejects_corrupt_input_without_writing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "invalid.json"
            output = Path(temporary) / "compiled.json"
            source.write_text('{"version":', encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(source), "--output", str(output),
            ], capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

    def test_cli_cannot_overwrite_its_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "plan.json"
            source.write_bytes(FIXTURE.read_bytes())
            before = source.read_bytes()
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(source), "--output", str(source),
            ], capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), before)

    def test_cli_cannot_overwrite_its_plan_through_a_hard_link(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "plan.json"
            source.write_bytes(FIXTURE.read_bytes())
            linked = Path(temporary) / "compiled.json"
            try:
                os.link(source, linked)
            except OSError as error:
                self.skipTest(f"Filesystem does not support hard links: {error}")
            before = source.read_bytes()
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(source), "--output", str(linked),
            ], capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
