import yaml
from pathlib import Path
import pytest

from rulebook_ai.community_packs import validate_pack_structure


def _write_manifest(root: Path, name="demo"):
    content = {
        "name": name,
        "version": "1.0.0",
        "summary": "demo pack",
    }
    (root / "manifest.yaml").write_text(yaml.dump(content))


def _setup_valid_pack(root: Path):
    _write_manifest(root)
    (root / "README.md").write_text("readme")
    rules = root / "rules"
    dir1 = rules / "01-rules"
    dir1.mkdir(parents=True)
    (dir1 / "01-general.md").write_text("rule")
    dir2 = rules / "02-rules-code"
    dir2.mkdir()
    (dir2 / "01-code.md").write_text("code rule")


def test_validate_pack_structure_ok(tmp_path):
    _setup_valid_pack(tmp_path)
    name, manifest = validate_pack_structure(tmp_path)
    assert name == "demo"
    assert manifest["version"] == "1.0.0"


def test_validate_pack_structure_missing_readme(tmp_path):
    _write_manifest(tmp_path)
    (tmp_path / "rules" / "01-rules").mkdir(parents=True)
    (tmp_path / "rules" / "01-rules" / "01-general.md").write_text("rule")
    with pytest.raises(ValueError):
        validate_pack_structure(tmp_path)


def test_validate_pack_structure_invalid_file_prefix(tmp_path):
    _setup_valid_pack(tmp_path)
    bad_file = tmp_path / "rules" / "02-rules-code" / "code.md"
    bad_file.write_text("bad")
    with pytest.raises(ValueError):
        validate_pack_structure(tmp_path)


def test_validate_pack_structure_invalid_extension(tmp_path):
    _setup_valid_pack(tmp_path)
    bad_file = tmp_path / "rules" / "02-rules-code" / "01-code.txt"
    bad_file.write_text("bad")
    with pytest.raises(ValueError):
        validate_pack_structure(tmp_path)


def test_validate_pack_structure_invalid_manifest_name(tmp_path):
    _setup_valid_pack(tmp_path)
    _write_manifest(tmp_path, name="Bad Name")
    with pytest.raises(ValueError):
        validate_pack_structure(tmp_path)


def test_validate_pack_structure_uppercase_manifest_name(tmp_path):
    _setup_valid_pack(tmp_path)
    _write_manifest(tmp_path, name="Good-Pack")
    name, _ = validate_pack_structure(tmp_path)
    assert name == "Good-Pack"


def test_validate_pack_structure_duplicate_directory_prefix(tmp_path):
    _setup_valid_pack(tmp_path)
    dup_dir = tmp_path / "rules" / "02-rules-debug"
    dup_dir.mkdir()
    (dup_dir / "01-debug.md").write_text("dbg")
    with pytest.raises(ValueError):
        validate_pack_structure(tmp_path)
