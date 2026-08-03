"""Integration regression tests for ``github:user/repo[/path]`` semantics.

These tests pin the end-to-end behavior of community-pack resolution when a
GitHub repository contains the pack inside a subdirectory:

* ``parse_slug`` splits ``user/repo/path/to/pack`` into username/repo/subpath.
* The community index schema accepts an optional ``path`` string.
* The install flow uses that subpath to locate the pack root in the clone.
* ``packs list`` and ``packs status`` embed the subpath in the rendered
  README / source URL.
"""

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


def _create_repo_with_subpath_pack(base: Path, slug: str) -> tuple[str, str]:
    """Create a git repo at ``base/slug`` whose pack lives under ``sub/pack``.

    The repository slug follows the ``user/repo`` convention; the actual pack
    is two directories deep at ``sub/pack``. Returns ``(subpath_slug, commit)``
    where ``subpath_slug`` is ``user/repo/sub/pack``.
    """
    username, repo = slug.split("/", 1)
    repo_dir = base / username / repo
    repo_dir.mkdir(parents=True)

    pack_root = repo_dir / "sub" / "pack"
    rules_dir = pack_root / "rules" / "01-rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "01-rule.md").write_text("rule")

    # A sibling top-level "distractor" ensures the installer really picks the
    # subpath and not the repo root.
    (repo_dir / "README.md").write_text("repo readme")

    (pack_root / "manifest.yaml").write_text(
        "name: nested-pack\nversion: 0.1.0\nsummary: nested test pack\n"
    )
    (pack_root / "README.md").write_text("nested readme")

    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo_dir,
        capture_output=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=repo_dir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=repo_dir, capture_output=True
    )
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True
    ).stdout.strip()
    return f"{username}/{repo}/sub/pack", commit


def _write_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2))


def test_parse_slug_extracts_subpath():
    from rulebook_ai.community_packs import parse_slug

    assert parse_slug("user/repo") == ("user", "repo", "")
    assert parse_slug("user/repo/sub/pack") == ("user", "repo", "sub/pack")
    # Trailing slashes do not introduce empty path components.
    assert parse_slug("user/repo/sub") == ("user", "repo", "sub")


def test_add_pack_by_slug_with_subpath_installs_to_folder(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/monorepo"
    subpath_slug, commit = _create_repo_with_subpath_pack(base, slug)

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "add", f"github:{subpath_slug}"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode == 0, result.stderr

    dest = project_dir / ".rulebook-ai" / "packs" / "nested-pack"
    assert dest.is_dir()
    # Content must come from the subpath, not the repo root.
    assert (dest / "rules" / "01-rules" / "01-rule.md").is_file()
    assert (dest / "manifest.yaml").read_text().startswith("name: nested-pack")

    meta = json.loads((dest / "pack.json").read_text())
    assert meta["slug"] == subpath_slug
    assert meta["commit"] == commit

    selection = json.loads(
        (project_dir / ".rulebook-ai" / "selection.json").read_text()
    )
    entry = selection["packs"][0]
    assert entry["slug"] == subpath_slug
    assert entry["commit"] == commit


def test_add_pack_by_index_with_path_uses_subpath(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/monorepo"
    subpath_slug, commit = _create_repo_with_subpath_pack(base, slug)

    index = {
        "packs": [
            {
                "name": "nested-pack",
                "username": "user",
                "repo": "monorepo",
                "description": "nested",
                "path": "sub/pack",
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
        ["packs", "add", "nested-pack"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )
    assert result.returncode == 0, result.stderr

    dest = project_dir / ".rulebook-ai" / "packs" / "nested-pack"
    assert dest.is_dir()
    meta = json.loads((dest / "pack.json").read_text())
    assert meta["slug"] == subpath_slug
    assert meta["commit"] == commit


def test_packs_list_embeds_subpath_in_readme_url(tmp_path, run_cli):
    _write_cache(
        {
            "packs": [
                {
                    "name": "nested-pack",
                    "username": "user",
                    "repo": "monorepo",
                    "description": "nested",
                    "path": "sub/pack",
                }
            ]
        }
    )
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(["packs", "list"], project_dir)
    assert result.returncode == 0, result.stderr
    assert "nested-pack (community)" in result.stdout
    assert (
        "https://github.com/user/monorepo/blob/main/sub/pack/README.md"
        in result.stdout
    )


def test_packs_status_embeds_subpath_in_source_url(tmp_path, run_cli):
    base = tmp_path / "repos"
    slug = "user/monorepo"
    subpath_slug, _commit = _create_repo_with_subpath_pack(base, slug)

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    run_cli(
        ["packs", "add", f"github:{subpath_slug}"],
        project_dir,
        input_text="yes\n",
        env={"RULEBOOK_AI_GIT_BASE": str(base)},
    )

    result = run_cli(["packs", "status"], project_dir)
    assert result.returncode == 0, result.stderr
    assert (
        "https://github.com/user/monorepo/blob/main/sub/pack/README.md"
        in result.stdout
    )