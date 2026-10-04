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

    def test_protection_preserves_selected_speech_without_changing_the_cut(self):
        protected = compile_plan(self.plan)
        legacy = copy.deepcopy(self.plan)
        del legacy["protected_ranges"]
        unprotected = compile_plan(legacy)
        self.assertEqual(protected["segments"], unprotected["segments"])
        self.assertEqual(protected["protected_ranges"], self.plan["protected_ranges"])
        self.assertEqual(unprotected["protected_ranges"], [])
        self.assertFalse(protected["media_verified"])

    def test_protected_speech_cannot_be_silently_omitted_without_a_cut_note(self):
        self.plan["cuts"] = []
        self.plan["keep"][1]["start"] = 6.2
        with self.assertRaisesRegex(SpeechPlanError, "correct-price: protected range"):
            compile_plan(self.plan)

    def test_partial_protected_removal_is_rejected_even_without_word_metadata(self):
        self.plan["sources"][0].pop("words")
        self.plan["keep"][1]["end"] = 5.8
        with self.assertRaisesRegex(SpeechPlanError, "correct-price: protected range"):
            compile_plan(self.plan)

    def protection_plan(self):
        return {
            "version": "0.1", "mode": "linear-1x", "revision": "protected-001",
            "sources": [{"source_id": "a", "duration": 2}, {"source_id": "b", "duration": 1}],
            "keep": [
                {"segment_id": "a1", "source_id": "a", "start": 0, "end": 1},
                {"segment_id": "a2", "source_id": "a", "start": 1, "end": 2},
                {"segment_id": "b1", "source_id": "b", "start": 0, "end": 1},
            ],
            "protected_ranges": [
                {"protection_id": "sentence", "source_id": "a", "start": 0.25, "end": 1.75, "reason": "Keep this sentence intact."},
            ],
        }

    def test_adjacent_keeps_can_preserve_one_protected_sentence(self):
        self.assertEqual(compile_plan(self.protection_plan())["duration"], 3)

    def test_authorized_reordering_cannot_reverse_a_protected_sentence(self):
        plan = self.protection_plan()
        plan.update(allow_reorder=True, reorder_reason="Move complete sections.")
        plan["keep"][0], plan["keep"][1] = plan["keep"][1], plan["keep"][0]
        with self.assertRaisesRegex(SpeechPlanError, "protected range was removed or reordered"):
            compile_plan(plan)

    def test_unrelated_speech_cannot_be_inserted_inside_a_protected_sentence(self):
        plan = self.protection_plan()
        plan.update(allow_reorder=True, reorder_reason="Move complete sections.")
        plan["keep"] = [plan["keep"][0], plan["keep"][2], plan["keep"][1]]
        with self.assertRaisesRegex(SpeechPlanError, "unrelated speech inserted"):
            compile_plan(plan)

    def test_protection_requires_valid_identity_bounds_and_a_reason(self):
        for field, value in (("source_id", "missing"), ("start", -1), ("end", 11), ("reason", ""), ("extra", True)):
            with self.subTest(field=field):
                plan = copy.deepcopy(self.plan)
                plan["protected_ranges"][0][field] = value
                with self.assertRaises(SpeechPlanError):
                    compile_plan(plan)
        self.plan["protected_ranges"].append(copy.deepcopy(self.plan["protected_ranges"][0]))
        with self.assertRaisesRegex(SpeechPlanError, "duplicate protection_id"):
            compile_plan(self.plan)

    def test_review_windows_cover_changed_joins_and_trimmed_head_and_tail(self):
        windows = compile_plan(self.plan)["review_windows"]
        self.assertEqual([window["kind"] for window in windows], ["opening", "join", "join", "ending"])
        self.assertEqual([window["check_at"] for window in windows], [0, 2.6, 3.9, 5.9])
        self.assertEqual((windows[1]["timeline_start"], windows[1]["timeline_end"]), (1.1, 4.1))
        self.assertEqual(windows[1]["sides"]["left"]["source_time"], 3.5)
        self.assertEqual(windows[1]["sides"]["right"]["source_time"], 5.2)
        for window in windows:
            self.assertEqual(window["revision"], self.plan["revision"])
            self.assertLessEqual(window["timeline_start"], window["check_at"])
            self.assertGreaterEqual(window["timeline_end"], window["check_at"])
            self.assertGreater(window["timeline_end"], window["timeline_start"])

    def test_unchanged_source_partition_does_not_invent_review_joins(self):
        self.plan["keep"] = [
            {"segment_id": "part1", "source_id": "camera-a", "start": 0, "end": 2.4},
            {"segment_id": "part2", "source_id": "camera-a", "start": 2.4, "end": 10},
        ]
        self.plan["cuts"] = []
        self.assertEqual(compile_plan(self.plan)["review_windows"], [])

    def test_source_switch_at_equal_source_times_is_still_a_real_join(self):
        plan = self.protection_plan()
        plan["sources"][1]["duration"] = 3
        plan["keep"] = [
            {"segment_id": "a1", "source_id": "a", "start": 0, "end": 2},
            {"segment_id": "b1", "source_id": "b", "start": 2, "end": 3},
        ]
        window = compile_plan(plan)["review_windows"][0]
        self.assertEqual(window["kind"], "join")
        self.assertEqual(window["check_at"], 2)
        self.assertEqual(window["sides"]["left"]["source_id"], "a")
        self.assertEqual(window["sides"]["right"]["source_id"], "b")
        self.assertEqual(window["sides"]["left"]["source_time"], window["sides"]["right"]["source_time"])

    def test_overlapping_review_windows_stay_separate_and_within_media(self):
        windows = compile_plan(self.plan, review_context=100)["review_windows"]
        self.assertEqual(len(windows), 4)
        self.assertEqual(len({window["window_id"] for window in windows}), 4)
        for window in windows:
            self.assertEqual((window["timeline_start"], window["timeline_end"]), (0, 5.9))

    def test_new_revision_regenerates_review_positions(self):
        before = compile_plan(self.plan)["review_windows"]
        self.plan["revision"] = "roughcut-002"
        self.plan["keep"][0]["end"] = 3
        after = compile_plan(self.plan)["review_windows"]
        self.assertEqual(after[1]["check_at"], 2.1)
        self.assertEqual(after[1]["sides"]["left"]["source_time"], 3)
        self.assertTrue(all(window["revision"] == "roughcut-002" for window in after))
        self.assertTrue(all(window["revision"] == "roughcut-001" for window in before))

    def test_invalid_review_context_is_rejected(self):
        for context in (True, 0, -1, 1e-10, float("nan"), float("inf"), 10 ** 400):
            with self.subTest(context=context):
                with self.assertRaises(SpeechPlanError):
                    compile_plan(self.plan, review_context=context)

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

    def test_cli_review_context_sets_windows_without_claiming_media_verification(self):
        result = subprocess.run([
            sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(FIXTURE),
            "--review-context", "0.5",
        ], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        window = report["review_windows"][1]
        self.assertEqual((window["timeline_start"], window["timeline_end"]), (2.1, 3.1))
        self.assertFalse(report["media_verified"])

    def test_cli_rejects_protected_removal_without_saving_a_report(self):
        self.plan["cuts"] = []
        self.plan["keep"][1]["start"] = 6.2
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "plan.json"
            output = Path(temporary) / "report.json"
            source.write_text(json.dumps(self.plan), encoding="utf-8")
            before = source.read_bytes()
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/speech_edit_plan.py"), str(source),
                "--output", str(output),
            ], capture_output=True, text=True, encoding="utf-8", check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("correct-price: protected range", result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertFalse(output.exists())
            self.assertEqual(source.read_bytes(), before)

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
