import json
import subprocess
from pathlib import Path


def _create_repo(
    base: Path,
    slug: str,
    *,
    manifest_name: str = "good-pack",
    include_rules: bool = True,
    include_manifest: bool = True,
):
    repo_dir = base / Path(slug)
    repo_dir.mkdir(parents=True)
    if include_rules:
        rules_dir = repo_dir / "rules" / "01-rules"
        rules_dir.mkdir(parents=True)
        (rules_dir / "01-rule.md").write_text("rule")
    if include_manifest:
        (repo_dir / "manifest.yaml").write_text(
            f"name: {manifest_name}\nversion: 0.1.0\nsummary: test pack\n"
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


def test_add_pack_by_slug_installs_to_folder(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/good-pack"
    _, commit = _create_repo(base, slug)
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"github:{slug}"],
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
    selection = json.loads(
        (project_dir / ".rulebook-ai" / "selection.json").read_text()
    )
    entry = selection["packs"][0]
    assert entry["slug"] == slug
    assert entry["commit"] == commit


def test_add_pack_conflicting_name_fails(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/conflict-pack"
    _create_repo(base, slug, manifest_name="light-spec")
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"github:{slug}"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode != 0
    dest = project_dir / ".rulebook-ai" / "packs" / "light-spec"
    assert not dest.exists()


def test_add_pack_invalid_structure_fails(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/invalid-pack"
    _create_repo(base, slug, include_rules=False)
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"github:{slug}"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode != 0
    dest = project_dir / ".rulebook-ai" / "packs" / "invalid-pack"
    assert not dest.exists()


def test_add_pack_user_decline_aborts(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/decline-pack"
    _create_repo(base, slug, manifest_name="decline-pack")
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"github:{slug}"],
        project_dir,
        input_text="no\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode == 0
    dest = project_dir / ".rulebook-ai" / "packs" / "decline-pack"
    assert not dest.exists()

def test_add_pack_by_local_path(tmp_path, run_cli):
    # 1. Create a local pack directory
    local_pack_dir = tmp_path / "my-local-pack"
    rules_dir = local_pack_dir / "rules" / "01-rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "01-rule.md").write_text("local rule")
    (local_pack_dir / "manifest.yaml").write_text(
        "name: my-local-pack\nversion: 1.0.0\nsummary: A local test pack\n"
    )
    (local_pack_dir / "README.md").write_text("readme")

    # 2. Run the CLI command
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"local:{local_pack_dir}"],
        project_dir,
    )

    # 3. Assert results
    assert result.returncode == 0, result.stderr
    dest = project_dir / ".rulebook-ai" / "packs" / "my-local-pack"
    assert dest.is_dir()
    assert (dest / "rules" / "01-rules" / "01-rule.md").read_text() == "local rule"

    selection = json.loads(
        (project_dir / ".rulebook-ai" / "selection.json").read_text()
    )
    entry = selection["packs"][0]
    assert entry["name"] == "my-local-pack"
    assert entry["version"] == "1.0.0"