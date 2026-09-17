"""Check the terminal launcher with a tiny substitute command, never a full run."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class LauncherTests(unittest.TestCase):
    def launch(self, code):
        source=Path(__file__).resolve().parents[1]/'start_embeddings.sh'
        self.assertTrue(source.is_file(), 'Terminal launcher is missing')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copyfile(source,root/source.name)
            (root/'embed.sh').write_text('#!/bin/sh\nprintf "arguments: %s\\n" "$*"\nprintf "diagnostic\\n" >&2\nexit '+str(code)+'\n')
            (root/'embed.sh').chmod(0o755)
            p=subprocess.run(['bash',str(root/source.name)],capture_output=True,text=True)
            log=(root/'data/embeddings_run.log').read_text()
            self.assertIn('arguments: run --scope full',log)
            self.assertIn('diagnostic',log)
            self.assertIn('diagnostic',p.stdout)
            self.assertEqual(p.returncode,code)

    def test_success_is_logged(self):self.launch(0)
    def test_failure_is_not_hidden_by_logging(self):self.launch(7)


if __name__=='__main__':unittest.main()
