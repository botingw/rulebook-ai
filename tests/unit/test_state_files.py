import json
from pathlib import Path

from rulebook_ai.core import RuleManager, SelectionState


def test_selection_json_profiles_schema(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    manager = RuleManager(project_root=str(project_dir))
    state = SelectionState(packs=[], profiles={"frontend": ["light-spec"]})
    manager._save_selection(project_dir, state)

    loaded = manager._load_selection(project_dir)
    assert loaded.profiles == {"frontend": ["light-spec"]}
    raw = json.loads((project_dir / ".rulebook-ai" / "selection.json").read_text())
    assert raw["profiles"] == {"frontend": ["light-spec"]}


def test_sync_status_recording(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    manager = RuleManager(project_root=str(project_dir))
    manager.add_pack("light-spec", project_dir=str(project_dir))
    manager.project_sync(assistants=["cursor"], project_dir=str(project_dir))

    data = json.loads((project_dir / ".rulebook-ai" / "sync_status.json").read_text())
    assert "cursor" in data
    assert data["cursor"]["mode"] == "all"
    assert data["cursor"]["packs"] == ["light-spec"]
    assert data["cursor"]["pack_count"] == 1


def test_rule_generation_idempotence(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    manager = RuleManager(project_root=str(project_dir))
    manager.add_pack("light-spec", project_dir=str(project_dir))
    manager.project_sync(assistants=["cursor"], project_dir=str(project_dir))

    manifest_before = (project_dir / ".rulebook-ai" / "file_manifest.json").read_text()
    arch_path = project_dir / "memory" / "docs" / "architecture_template.md"
    content_before = arch_path.read_text()

    manager.project_sync(assistants=["cursor"], project_dir=str(project_dir))

    manifest_after = (project_dir / ".rulebook-ai" / "file_manifest.json").read_text()
    content_after = arch_path.read_text()

    assert manifest_before == manifest_after
    assert content_before == content_after

