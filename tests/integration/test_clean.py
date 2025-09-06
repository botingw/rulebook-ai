import os
import subprocess
from pathlib import Path

TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"


def _run(cmd, project_dir, env, repo_root, input=None):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
        input=input,
    )


def _setup_project(tmp_path):
    project_dir = tmp_path / "clean_project"
    project_dir.mkdir()
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    add = _run(
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
        project_dir,
        env,
        repo_root,
    )
    assert add.returncode == 0, f"STDERR:\n{add.stderr}\nSTDOUT:\n{add.stdout}"
    return project_dir, repo_root, env


def test_clean_confirm_yes(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)
    result = _run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "clean",
            "--project-dir",
            str(project_dir),
        ],
        project_dir,
        env,
        repo_root,
        input="yes\n",
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    assert not (project_dir / ".rulebook-ai").exists()
    assert not (project_dir / TARGET_MEMORY_BANK_DIR).exists()
    assert not (project_dir / TARGET_TOOLS_DIR).exists()


def test_clean_confirm_no(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)
    result = _run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "clean",
            "--project-dir",
            str(project_dir),
        ],
        project_dir,
        env,
        repo_root,
        input="no\n",
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    assert (project_dir / ".rulebook-ai").exists()


def test_clean_rules(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)
    result = _run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "clean-rules",
            "--project-dir",
            str(project_dir),
        ],
        project_dir,
        env,
        repo_root,
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    assert not (project_dir / ".rulebook-ai").exists()
    assert (project_dir / TARGET_MEMORY_BANK_DIR).exists()
    assert (project_dir / TARGET_TOOLS_DIR).exists()


def test_clean_rules_removes_platform_artifacts(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)
    assert (project_dir / ".cursor").exists()
    assert (project_dir / "CLAUDE.md").is_file()
    assert (project_dir / ".github" / "copilot-instructions.md").is_file()

    result = _run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "clean-rules",
            "--project-dir",
            str(project_dir),
        ],
        project_dir,
        env,
        repo_root,
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    assert not (project_dir / ".cursor").exists()
    assert not (project_dir / "CLAUDE.md").exists()
    assert not (project_dir / ".github" / "copilot-instructions.md").exists()
    assert (project_dir / TARGET_MEMORY_BANK_DIR).exists()
    assert (project_dir / TARGET_TOOLS_DIR).exists()
