import os
import subprocess
import sys
from pathlib import Path


def test_packs_list_displays_available_packs():
    """The `packs list` command should print available packs with manifest data."""
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        [sys.executable, "-m", "rulebook_ai", "packs", "list"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    output = result.stdout
    assert "light-spec" in output
    assert "v0.1.0" in output
    assert "An advanced simplification" in output
