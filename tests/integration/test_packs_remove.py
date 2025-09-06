import json
import os
import subprocess
from pathlib import Path

TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"


def test_packs_remove_light_spec(tmp_path):
    project_dir = tmp_path / "remove_project"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    add_result = subprocess.run(
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
    assert add_result.returncode == 0, f"STDERR:\n{add_result.stderr}\nSTDOUT:\n{add_result.stdout}"

    remove_result = subprocess.run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "remove",
            "light-spec",
            "--project-dir",
            str(project_dir),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )
    assert remove_result.returncode == 0, f"STDERR:\n{remove_result.stderr}\nSTDOUT:\n{remove_result.stdout}"

    rulebook_dir = project_dir / ".rulebook-ai"
    assert not rulebook_dir.exists()

    memory_dir = project_dir / TARGET_MEMORY_BANK_DIR
    tools_dir = project_dir / TARGET_TOOLS_DIR
    assert not memory_dir.exists() or not any(memory_dir.iterdir())
    assert not tools_dir.exists() or not any(tools_dir.iterdir())

    assert not (project_dir / ".cursor").exists()


def test_packs_remove_nonexistent_pack(tmp_path):
    project_dir = tmp_path / "remove_missing_project"
    project_dir.mkdir()

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    add_result = subprocess.run(
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
    assert add_result.returncode == 0, f"STDERR:\n{add_result.stderr}\nSTDOUT:\n{add_result.stdout}"

    remove_result = subprocess.run(
        [
            "python",
            "-m",
            "rulebook_ai",
            "packs",
            "remove",
            "ghost-pack",
            "--project-dir",
            str(project_dir),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )
    assert remove_result.returncode != 0
    assert "Pack 'ghost-pack' is not active" in remove_result.stdout

    # selection.json should remain with the original pack
    selection_file = project_dir / ".rulebook-ai" / "selection.json"
    data = json.loads(selection_file.read_text())
    assert any(p["name"] == "light-spec" for p in data.get("packs", []))
