import json
import subprocess
from pathlib import Path


CACHE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "rulebook_ai"
    / "community"
    / "index_cache"
    / "packs.json"
)


def _create_repo(base: Path, slug: str) -> tuple[Path, str]:
    repo_dir = base / Path(slug)
    repo_dir.mkdir(parents=True)
    rules_dir = repo_dir / "rules" / "01-rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "01-rule.md").write_text("rule")
    (repo_dir / "manifest.yaml").write_text(
        f"name: {Path(slug).name}\nversion: 0.1.0\nsummary: test pack\n"
    )
    (repo_dir / "README.md").write_text("readme")
    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=repo_dir, capture_output=True
    )
    subprocess.run(["git", "add", "-A"], cwd=repo_dir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=repo_dir, capture_output=True
    )
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True
    ).stdout.strip()
    return repo_dir, commit


def _write_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2))


def test_packs_update_refreshes_cache(tmp_path, run_cli):
    index_file = tmp_path / "packs.json"
    data = {
        "packs": [
            {
                "name": "good-pack",
                "username": "user",
                "repo": "good-pack",
                "description": "desc",
            }
        ]
    }
    index_file.write_text(json.dumps(data))
    _write_cache({"packs": []})
    result = run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": index_file.as_uri()},
    )
    assert result.returncode == 0, result.stderr
    cached = json.loads(CACHE_PATH.read_text())
    assert cached == data


def test_packs_update_invalid_json_retains_old_cache(tmp_path, run_cli):
    bad_index = tmp_path / "bad.json"
    bad_index.write_text("{" )
    old = {"packs": [ {"name": "old", "username": "u", "repo": "r", "description": "d"} ]}
    _write_cache(old)
    result = run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": bad_index.as_uri()},
    )
    assert result.returncode != 0
    cached = json.loads(CACHE_PATH.read_text())
    assert cached == old


def test_add_pack_by_name_uses_cache(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/good-pack"
    _, commit = _create_repo(base, slug)
    index = {
        "packs": [
            {
                "name": "good-pack",
                "username": "user",
                "repo": "good-pack",
                "description": "desc",
                "commit": commit,
            }
        ]
    }
    index_file = tmp_path / "packs.json"
    index_file.write_text(json.dumps(index))
    _write_cache({"packs": []})
    run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": index_file.as_uri()},
    )
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", "good-pack"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode == 0, result.stderr
    dest = project_dir / ".rulebook-ai" / "packs" / "good-pack"
    assert dest.is_dir()
    meta = json.loads((dest / "pack.json").read_text())
    assert meta["slug"] == slug
    assert meta["commit"] == commit


def test_add_unknown_pack_name_fails(tmp_path, run_cli):
    index_file = tmp_path / "packs.json"
    index_file.write_text(json.dumps({"packs": []}))
    _write_cache({"packs": []})
    run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": index_file.as_uri()},
    )
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli([
        "packs",
        "add",
        "unknown",
    ], project_dir)
    assert result.returncode != 0
    dest = project_dir / ".rulebook-ai" / "packs" / "unknown"
    assert not dest.exists()


def test_add_pack_name_mismatch_fails(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/good-pack"
    _, commit = _create_repo(base, slug)
    index = {
        "packs": [
            {
                "name": "wrong-name",
                "username": "user",
                "repo": "good-pack",
                "description": "desc",
                "commit": commit,
            }
        ]
    }
    index_file = tmp_path / "packs.json"
    index_file.write_text(json.dumps(index))
    _write_cache({"packs": []})
    run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": index_file.as_uri()},
    )
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", "wrong-name"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode != 0
    dest = project_dir / ".rulebook-ai" / "packs" / "good-pack"
    assert not dest.exists()


def test_installed_pack_records_slug_metadata(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/good-pack"
    _, commit = _create_repo(base, slug)
    index = {
        "packs": [
            {
                "name": "good-pack",
                "username": "user",
                "repo": "good-pack",
                "description": "desc",
                "commit": commit,
            }
        ]
    }
    index_file = tmp_path / "packs.json"
    index_file.write_text(json.dumps(index))
    _write_cache({"packs": []})
    run_cli(
        ["packs", "update"],
        tmp_path,
        env={"RULEBOOK_AI_INDEX_URL": index_file.as_uri()},
    )
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    run_cli(
        ["packs", "add", "good-pack"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    selection = json.loads(
        (project_dir / ".rulebook-ai" / "selection.json").read_text()
    )
    entry = selection["packs"][0]
    assert entry["slug"] == slug
    assert entry["commit"] == commit
