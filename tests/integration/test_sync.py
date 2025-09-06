import os
import subprocess
from pathlib import Path


def _setup_project(tmp_path):
    project_dir = tmp_path / "sync_project"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    add = subprocess.run(
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
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )
    assert add.returncode == 0, f"STDERR:\n{add.stderr}\nSTDOUT:\n{add.stdout}"
    return project_dir, repo_root, env


def test_sync_regenerates_rules(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)

    meta = project_dir / "project_rules" / "01-rules" / "00-meta-rules.md"
    original = meta.read_text()
    updated = original + "\nEXTRA LINE"
    meta.write_text(updated)

    sync = subprocess.run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "sync",
            "--all",
            "--project-dir",
            str(project_dir),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )
    assert sync.returncode == 0, f"STDERR:\n{sync.stderr}\nSTDOUT:\n{sync.stdout}"

    gh_file = project_dir / ".github" / "copilot-instructions.md"
    assert gh_file.is_file()
    content = gh_file.read_text()
    assert "EXTRA LINE" in content


def test_sync_generates_platform_rules(tmp_path):
    project_dir, repo_root, env = _setup_project(tmp_path)

    for path in [
        project_dir / ".cursor",
        project_dir / ".roo",
        project_dir / "CLAUDE.md",
        project_dir / ".github" / "copilot-instructions.md",
    ]:
        if path.is_dir():
            subprocess.run(["rm", "-rf", str(path)])
        elif path.exists():
            path.unlink()

    sync = subprocess.run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "sync",
            "--all",
            "--project-dir",
            str(project_dir),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )
    assert sync.returncode == 0, f"STDERR:\n{sync.stderr}\nSTDOUT:\n{sync.stdout}"

    assert (project_dir / ".cursor" / "rules" / "01-meta-rules.mdc").is_file()
    assert (project_dir / ".roo" / "rules" / "00-meta-rules.md").is_file()
    assert (
        project_dir / ".roo" / "rules-architect" / "01-plan_v1.md"
    ).is_file()
    assert (project_dir / "CLAUDE.md").is_file()
    assert (project_dir / ".github" / "copilot-instructions.md").is_file()
