from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml


INDEX_CACHE_PATH = Path(__file__).parent / "community" / "index_cache" / "packs.json"
DEFAULT_INDEX_URL = (
    "https://raw.githubusercontent.com/rulebook-ai/community-index/main/packs.json"
)


def parse_slug(slug: str) -> tuple[str, str, str]:
    parts = slug.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid slug")
    username, repo = parts[0], parts[1]
    subpath = "/".join(parts[2:]) if len(parts) > 2 else ""
    return username, repo, subpath


def validate_pack_structure(
    pack_root: Path, expected_name: Optional[str] = None
) -> tuple[str, Dict[str, Any]]:
    """Validate pack structure and optional name, returning name and manifest."""
    manifest_path = pack_root / "manifest.yaml"
    rules_dir = pack_root / "rules"
    if not manifest_path.is_file() or not rules_dir.is_dir():
        raise ValueError("Invalid pack structure.")
    manifest = yaml.safe_load(manifest_path.read_text()) or {}
    name = manifest.get("name")
    if not name:
        raise ValueError("manifest.yaml missing 'name'.")
    if expected_name and name != expected_name:
        raise ValueError(f"name mismatch: {name} != {expected_name}")
    return name, manifest


def _load_index_cache() -> Dict[str, List[Dict[str, str]]]:
    if INDEX_CACHE_PATH.exists():
        try:
            return json.loads(INDEX_CACHE_PATH.read_text())
        except Exception:
            pass
    return {"packs": []}


def load_index_cache() -> Dict[str, List[Dict[str, str]]]:
    """Return the cached community index."""
    return _load_index_cache()


def _save_index_cache(data: Dict[str, List[Dict[str, str]]]) -> None:
    INDEX_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_CACHE_PATH.write_text(json.dumps(data, indent=2))


def _validate_index(data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    if not isinstance(data, dict):
        raise ValueError("Index must be a JSON object")
    packs = data.get("packs")
    if not isinstance(packs, list):
        raise ValueError("Index missing 'packs' list")
    for entry in packs:
        for field in ["name", "username", "repo", "description"]:
            if field not in entry or not isinstance(entry[field], str):
                raise ValueError(f"Index entry missing '{field}'")
        if "path" in entry and not isinstance(entry["path"], str):
            raise ValueError("Index 'path' must be string")
        if "commit" in entry and not isinstance(entry["commit"], str):
            raise ValueError("Index 'commit' must be string")
    return packs


def update_index_cache() -> int:
    url = os.environ.get("RULEBOOK_AI_INDEX_URL", DEFAULT_INDEX_URL)
    last_err: Optional[str] = None
    for _ in range(2):
        try:
            with urllib.request.urlopen(url) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            _validate_index(data)
            _save_index_cache(data)
            print("Community index updated.")
            return 0
        except Exception as e:  # pragma: no cover - network errors vary
            last_err = str(e)
    print(f"Failed to update community index: {last_err}")
    return 1


def add_pack_from_index(
    name: str,
    project_root: Path,
    source_packs_dir: Path,
    load_selection: Callable[[Path], object],
    save_selection: Callable[[Path, object], None],
) -> int:
    index = load_index_cache().get("packs", [])
    entry = next((p for p in index if p.get("name") == name), None)
    if not entry:
        print(f"Pack '{name}' not found in community index.")
        return 1
    slug_parts = [entry["username"], entry["repo"]]
    if entry.get("path"):
        slug_parts.append(entry["path"])
    slug = "/".join(slug_parts)
    ref = entry.get("commit")
    return add_pack_from_slug(
        slug,
        project_root,
        source_packs_dir,
        load_selection,
        save_selection,
        ref=ref,
        expected_name=entry["name"],
    )


def add_pack_from_slug(
    slug: str,
    project_root: Path,
    source_packs_dir: Path,
    load_selection: Callable[[Path], object],
    save_selection: Callable[[Path, object], None],
    ref: Optional[str] = None,
    expected_name: Optional[str] = None,
) -> int:
    try:
        username, repo, subpath = parse_slug(slug)
    except ValueError:
        print(f"Invalid slug '{slug}'.")
        return 1

    base = os.environ.get("RULEBOOK_AI_GIT_BASE", "https://github.com")
    if base.startswith("http://") or base.startswith("https://"):
        repo_url = f"{base.rstrip('/')}/{username}/{repo}"
    else:
        repo_url = str(Path(base) / username / repo)

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = Path(tmpdir) / "repo"
        result = subprocess.run(
            ["git", "clone", repo_url, str(clone_dir)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip())
            return 1

        if ref:
            checkout = subprocess.run(
                ["git", "-C", str(clone_dir), "checkout", ref],
                capture_output=True,
                text=True,
            )
            if checkout.returncode != 0:
                print(checkout.stderr.strip())
                return 1

        pack_root = clone_dir / subpath if subpath else clone_dir
        try:
            pack_name, manifest = validate_pack_structure(
                pack_root, expected_name
            )
        except ValueError as e:
            print(str(e))
            return 1

        builtins = {d.name for d in source_packs_dir.iterdir() if d.is_dir()}
        if pack_name in builtins:
            print(f"Pack name '{pack_name}' conflicts with built-in pack names.")
            return 1

        dest_dir = project_root / ".rulebook-ai" / "packs" / pack_name

        if dest_dir.exists():
            meta_path = dest_dir / "pack.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                if meta.get("slug") != slug:
                    print(
                        f"Pack '{pack_name}' already installed from a different source."
                    )
                    return 1
                shutil.rmtree(dest_dir)
            else:
                print(f"Pack '{pack_name}' already installed as built-in pack.")
                return 1

        commit = (
            subprocess.run(
                ["git", "-C", str(clone_dir), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
            ).stdout.strip()
        )

        warning = (
            f"WARNING: You are installing a community pack from {slug}"
            + (f"@{ref}" if ref else "")
            + ". This code is not audited."
        )
        if not ref:
            warning += " Installing without a pinned commit may change unexpectedly."
        print(warning)
        try:
            resp = input("Proceed? (yes/No): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nInstallation cancelled.")
            return 1
        if resp not in {"y", "yes"}:
            print("Installation cancelled by user.")
            return 0

        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(pack_root, dest_dir)

        meta = {"name": pack_name, "slug": slug, "commit": commit}
        (dest_dir / "pack.json").write_text(json.dumps(meta, indent=2))

        selection = load_selection(project_root)
        version = manifest.get("version", "0.0.0")
        entry = {
            "name": pack_name,
            "version": version,
            "slug": slug,
            "commit": commit,
        }
        existing = next((p for p in selection.packs if p["name"] == pack_name), None)
        if existing:
            existing.update(entry)
        else:
            selection.packs.append(entry)
        save_selection(project_root, selection)

        print(f"Added community pack '{pack_name}'.")
        return 0
