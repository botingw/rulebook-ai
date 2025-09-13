import os
import subprocess
from pathlib import Path
import pytest


@pytest.fixture
def run_cli():
    repo_root = Path(__file__).resolve().parents[2]

    def _run_cli(args, project_dir, input_text=None, env=None):
        base_env = os.environ.copy()
        base_env["PYTHONPATH"] = str(repo_root / "src")
        if env:
            base_env.update(env)
        cmd = ["python", "-m", "rulebook_ai", *args, "--project-dir", str(project_dir)]
        return subprocess.run(
            cmd, input=input_text, capture_output=True, text=True, env=base_env
        )

    return _run_cli


@pytest.fixture
def synced_project(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    run_cli(["packs", "add", "light-spec"], project_dir)
    run_cli(["project", "sync", "--assistant", "cursor"], project_dir)
    return project_dir
