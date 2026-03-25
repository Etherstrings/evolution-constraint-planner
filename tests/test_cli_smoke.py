import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ECL = ROOT / "scripts" / "ecl.py"
VALIDATE = ROOT / "scripts" / "validate_ecl_bundle.py"
EXAMPLE_BUNDLE = ROOT / "examples" / "stage-a-sample" / "bundle"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class CliSmokeTests(unittest.TestCase):
    def test_help_commands_return_success(self) -> None:
        commands = [
            ("python3", str(ECL), "--help"),
            ("python3", str(ECL), "pre", "--help"),
            ("python3", str(ECL), "plan", "--help"),
            ("python3", str(ECL), "code", "--help"),
            ("python3", str(ECL), "achieve", "--help"),
        ]
        for command in commands:
            with self.subTest(command=command):
                completed = run_command(*command)
                self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_example_bundle_validates(self) -> None:
        completed = run_command("python3", str(VALIDATE), str(EXAMPLE_BUNDLE))
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_pre_generates_a_valid_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            output_dir = tmp_path / "bundle"
            case_path = tmp_path / "case.json"
            completed = run_command(
                "python3",
                str(ECL),
                "pre",
                "--request",
                "Build a tiny dashboard with one empty state.",
                "--output",
                str(output_dir),
                "--case-json-out",
                str(case_path),
                "--repo-path",
                str(ROOT),
                "--project-path",
                str(ROOT),
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(case_path.exists())
            self.assertTrue((output_dir / "00-overview.md").exists())
            self.assertTrue((output_dir / "99-code-handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
