import json
import unittest
from pathlib import Path

from scripts.sync_chatcut_prompt_library import parse_cards, render_catalog_json, render_catalog, compare_catalogs


class PromptCatalogTest(unittest.TestCase):
    def test_metadata_diff_does_not_treat_rename_as_new_template(self):
        old = [{"reference_id":"one", "name":"Old"}, {"reference_id":"removed"}]
        new = [{"reference_id":"one", "name":"New"}, {"reference_id":"added"}]
        report=compare_catalogs(old,new)
        self.assertEqual(report["added"],["added"])
        self.assertEqual(report["removed"],["removed"])
        self.assertEqual(report["changed"],[{"reference_id":"one","fields":["name"]}])

    def test_duplicate_reference_id_is_rejected(self):
        with self.assertRaises(ValueError):
            compare_catalogs([], [{"reference_id":"one"},{"reference_id":"one"}])

    def test_future_category_is_visible_in_markdown(self):
        card={"category":"New category","name":"Example","description":"A useful example","reference_id":"new","entry_url":"https://example.org"}
        self.assertIn("## New category",render_catalog([card]))

    def setUp(self):
        self.page = Path("tests/fixtures/prompt-library-sample.html").read_text(
            encoding="utf-8"
        )

    def test_extracts_video_preview_metadata(self):
        cards = parse_cards(self.page)
        video = next(card for card in cards if card["target"] == "video-gen")
        self.assertEqual(video["reference_id"], "video-preset-1")
        self.assertEqual(video["preview_video_url"], "https://cdn.example/video.mp4")
        self.assertEqual(video["poster_url"], "https://cdn.example/poster.jpg")

    def test_motion_graphic_uses_live_entry_without_fake_video(self):
        cards = parse_cards(self.page)
        mg = next(card for card in cards if card["target"] == "motion-graphics")
        self.assertEqual(mg["reference_id"], "mg-template-1")
        self.assertEqual(mg["preview_video_url"], "")
        self.assertEqual(mg["poster_url"], "")

    def test_json_catalog_is_machine_readable(self):
        payload = json.loads(render_catalog_json(parse_cards(self.page), "2026-07-16"))
        self.assertEqual(payload["count"], 2)
        self.assertEqual(len(payload["entries"]), 2)
        self.assertEqual(payload["synced_on"], "2026-07-16")


if __name__ == "__main__":
    unittest.main()
