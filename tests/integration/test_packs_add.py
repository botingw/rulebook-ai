import json
import os
import subprocess
from pathlib import Path

TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"


def run_cli(args, repo_root, env):
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        env=env,
        cwd=repo_root,
    )


def test_packs_add_light_spec(tmp_path):
    project_dir = tmp_path / "add_project"
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
            "add",
            "light-spec",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert result.returncode == 0, f"STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # verify memory and tools directories
    assert (project_dir / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (project_dir / TARGET_TOOLS_DIR).is_dir()

    # verify internal state and pack copy
    rulebook_dir = project_dir / ".rulebook-ai"
    assert rulebook_dir.is_dir()
    assert (rulebook_dir / "packs" / "light-spec").is_dir()

    # verify selection.json records the pack
    selection_file = project_dir / ".rulebook-ai" / "selection.json"
    assert selection_file.is_file()
    data = json.loads(selection_file.read_text())
    assert any(
        p["name"] == "light-spec" and p.get("version") == "0.1.0"
        for p in data.get("packs", [])
    )

    # ensure sync generated some assistant rules
    assert (project_dir / ".cursor" / "rules").is_dir()


def test_packs_add_second_pack(tmp_path):
    project_dir = tmp_path / "multi_project"
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

    mem_files_before = sorted((project_dir / TARGET_MEMORY_BANK_DIR).rglob("*"))
    tool_files_before = sorted((project_dir / TARGET_TOOLS_DIR).rglob("*"))

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

    # verify selection.json contains both packs in order
    selection_file = project_dir / ".rulebook-ai" / "selection.json"
    data = json.loads(selection_file.read_text())
    names = [p["name"] for p in data.get("packs", [])]
    assert names == ["light-spec", "heavy-spec"]

    rulebook_dir = project_dir / ".rulebook-ai" / "packs"
    assert (rulebook_dir / "heavy-spec").is_dir()

    # verify existing starter files were not overwritten
    mem_files_after = sorted((project_dir / TARGET_MEMORY_BANK_DIR).rglob("*"))
    tool_files_after = sorted((project_dir / TARGET_TOOLS_DIR).rglob("*"))
    assert mem_files_after == mem_files_before
    assert tool_files_after == tool_files_before

    # implicit sync should have run
    assert (project_dir / ".cursor" / "rules").is_dir()


def test_packs_add_nonexistent_pack(tmp_path):
    project_dir = tmp_path / "missing_pack_project"
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
            "add",
            "ghost-pack",
            "--project-dir",
            str(project_dir),
        ],
        repo_root,
        env,
    )
    assert result.returncode != 0
    assert "Pack 'ghost-pack' not found" in result.stdout
    assert not (project_dir / ".rulebook-ai").exists()
