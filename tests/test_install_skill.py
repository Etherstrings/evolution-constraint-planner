import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = ROOT / "scripts" / "install_skill.sh"


class InstallSkillTests(unittest.TestCase):
    def test_install_script_copies_repo_into_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["CODEX_HOME"] = tmpdir
            completed = subprocess.run(
                ["bash", str(INSTALL_SCRIPT)],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            installed_root = Path(tmpdir) / "skills" / "evolution-constraint-planner"
            self.assertTrue((installed_root / "SKILL.md").exists())
            self.assertTrue((installed_root / "scripts" / "ecl.py").exists())
            self.assertTrue((installed_root / "references" / "stage-playbook.md").exists())


if __name__ == "__main__":
    unittest.main()
