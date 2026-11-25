"""Regression tests for the vendored UI-tree helpers (stdlib only)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
XML = (
    '<hierarchy><node text="Other" bounds="[0,0][10,10]"/>'
    '<node text="Settings" clickable="true" bounds="[100,200][300,260]"/>'
    "</hierarchy>\nERROR: /dev/tty"
)


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *map(str, args)],
        capture_output=True,
        text=True,
        check=False,
    )


class UiHelpersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dump = Path(self.tmp.name) / "ui.xml"
        self.dump.write_text(XML)

    def test_pick_returns_bounds_centre(self):
        result = run("ui_pick.py", self.dump, "Settings")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "200 230")

    def test_pick_missing_node_is_error(self):
        result = run("ui_pick.py", self.dump, "TidakAda")
        self.assertEqual(result.returncode, 2)
        self.assertIn("node not found", result.stderr)

    def test_summarize_includes_interactive_node(self):
        out = Path(self.tmp.name) / "summary.txt"
        result = run("ui_tree_summarize.py", self.dump, out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('text="Settings"', out.read_text())


if __name__ == "__main__":
    unittest.main()
