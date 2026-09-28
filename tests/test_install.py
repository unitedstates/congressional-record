"""An install without extras runs the parser and CLI but leaves out PostgreSQL."""

import os
import shutil
import subprocess  # nosec B404
import sys
import tempfile
import unittest
from importlib.util import find_spec

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The postgres extra's modules, then declarations nothing imports any more.
ABSENT = ["psycopg2", "sqlalchemy", "yaml", "unicodecsv", "numpy", "requests"]
UV = shutil.which("uv")
VENV = find_spec("venv") and find_spec("ensurepip")
# A caller's PYTHONPATH could supply packages the install should have to declare.
ENV = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}


def run(*cmd, cwd=None):
    # The argv comes from this file, never a shell.
    return subprocess.run(  # nosec B603
        cmd, capture_output=True, text=True, cwd=cwd, env=ENV
    )


@unittest.skipUnless(UV or VENV, "needs uv, or the venv and ensurepip modules")
class testCoreInstall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.cwd = tmp.name  # outside the checkout, so imports come from the install
        venv = os.path.join(tmp.name, "venv")
        bindir = os.path.join(venv, "Scripts" if os.name == "nt" else "bin")
        cls.python = os.path.join(bindir, "python")
        cls.cli = os.path.join(bindir, "congressionalrecord")
        # Editable (the README's install), so the check covers the declared
        # dependencies whichever subpackages the wheel lists.
        if UV:
            steps = [
                (UV, "venv", "--python", sys.executable, venv),
                (UV, "pip", "install", "--python", cls.python, "-e", REPO),
            ]
        else:
            steps = [
                (sys.executable, "-m", "venv", venv),
                (cls.python, "-m", "pip", "install", "-e", REPO),
            ]
        for step in steps:
            done = run(*step)
            if done.returncode:
                raise RuntimeError("{}\n{}".format(" ".join(step), done.stderr))

    def succeeds(self, *cmd):
        done = run(*cmd, cwd=self.cwd)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def test_parser_and_schema_import(self):
        self.succeeds(
            self.python,
            "-c",
            "import congressionalrecord.govinfo.cr_parser, congressionalrecord.schema",
        )

    def test_cli_help(self):
        self.assertIn("usage:", self.succeeds(self.cli, "--help"))

    def test_pg_mode_names_the_extra(self):
        done = run(self.cli, "2020-01-02", "2020-01-02", "pg", cwd=self.cwd)
        self.assertEqual(done.returncode, 2, done.stderr)
        self.assertIn("congressionalrecord[postgres]", done.stderr)

    def test_postgres_and_unused_packages_absent(self):
        present = self.succeeds(
            self.python,
            "-c",
            "import sys; from importlib.util import find_spec; "
            "print(*[m for m in sys.argv[1:] if find_spec(m)])",
            *ABSENT,
        )
        self.assertEqual(present.split(), [])
