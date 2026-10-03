import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.check_local_links import markdown_paths, missing_links

class LocalLinksTest(unittest.TestCase):
    def test_relative_encoded_image_and_missing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'image with space.png').touch()
            text='[image](image%20with%20space.png) <img src="missing.gif"> [web](https://example.org/no) [part](#intro)'
            self.assertEqual(missing_links(root/'README.md',text),['missing.gif'])

    def test_code_examples_are_not_file_dependencies(self):
        self.assertEqual(missing_links(Path('/tmp/test.md'),'```md\n[example](missing.md)\n```'),[])

    def test_copied_installation_without_git_checks_docs_but_not_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('README.md', 'references/guide.md', 'test-results/private.md', 'node_modules/dependency.md'):
                file=root/name;file.parent.mkdir(parents=True,exist_ok=True);file.touch()
            with patch('scripts.check_local_links.subprocess.run',side_effect=FileNotFoundError):
                self.assertEqual(markdown_paths(root),['README.md','references/guide.md'])

    def test_git_source_set_is_used_when_available(self):
        from subprocess import CompletedProcess
        with patch('scripts.check_local_links.subprocess.run',side_effect=[
            CompletedProcess(['git'],0,stdout=str(Path('.').resolve()).encode('utf-8'),stderr=b''),
            CompletedProcess(['git'],0,stdout=b'README.md\0references/guide.md\0example.py\0',stderr=b''),
        ]):
            self.assertEqual(markdown_paths(Path('.')),['README.md','references/guide.md'])

    def test_install_inside_another_git_checkout_uses_its_own_files(self):
        from subprocess import CompletedProcess
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'nested-skill';root.mkdir();(root/'README.md').touch()
            with patch('scripts.check_local_links.subprocess.run',return_value=CompletedProcess(
                ['git'],0,stdout=str(root.parent).encode('utf-8'),stderr=b''
            )):
                self.assertEqual(markdown_paths(root),['README.md'])
