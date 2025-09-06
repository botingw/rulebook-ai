import os
import subprocess
from pathlib import Path

def run_cli(args, repo_root, env):
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )

def test_packs_status_no_packs(tmp_path):
    project_dir = tmp_path / "status_project"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    result = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "status",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    assert "No packs are active" in result.stdout


def test_packs_status_one_pack(tmp_path):
    project_dir = tmp_path / "status_project2"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    add_result = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "add",
            "light-spec",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert add_result.returncode == 0, f"STDERR:\n{add_result.stderr}\nSTDOUT:\n{add_result.stdout}"

    status_result = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "status",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert status_result.returncode == 0, f"STDERR:\n{status_result.stderr}\nSTDOUT:\n{status_result.stdout}"
    assert "light-spec" in status_result.stdout
    assert "0.1.0" in status_result.stdout


def test_packs_status_multiple_packs(tmp_path):
    project_dir = tmp_path / "status_project_multi"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    first = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "add",
            "light-spec",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert first.returncode == 0, f"STDERR:\n{first.stderr}\nSTDOUT:\n{first.stdout}"

    second = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "add",
            "heavy-spec",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert second.returncode == 0, f"STDERR:\n{second.stderr}\nSTDOUT:\n{second.stdout}"

    status_result = run_cli(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "status",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert status_result.returncode == 0, f"STDERR:\n{status_result.stderr}\nSTDOUT:\n{status_result.stdout}"
    lines = status_result.stdout.strip().splitlines()
    assert "Active packs:" in lines[0]
    assert "1. light-spec" in lines[1]
    assert "2. heavy-spec" in lines[2]
