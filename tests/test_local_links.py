import tempfile
import unittest
from pathlib import Path
from scripts.check_local_links import missing_links

class LocalLinksTest(unittest.TestCase):
    def test_relative_encoded_image_and_missing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'image with space.png').touch()
            text='[image](image%20with%20space.png) <img src="missing.gif"> [web](https://example.org/no) [part](#intro)'
            self.assertEqual(missing_links(root/'README.md',text),['missing.gif'])

    def test_code_examples_are_not_file_dependencies(self):
        self.assertEqual(missing_links(Path('/tmp/test.md'),'```md\n[example](missing.md)\n```'),[])
