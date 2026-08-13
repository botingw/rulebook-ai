from pathlib import Path

from rulebook_ai.cli import main
from rulebook_ai.scripts.sync_pack_docs import DESTINATION_RELATIVE, SOURCE_FILES, sync_docs


def _project_fixture(tmp_path: Path) -> Path:
    project_dir = tmp_path / "project"
    for dest_name, source_path in SOURCE_FILES.items():
        path = project_dir / source_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"source: {dest_name}\n", encoding="utf-8")
    (project_dir / DESTINATION_RELATIVE).mkdir(parents=True)
    return project_dir


def test_sync_docs_copies_all_canonical_sources(tmp_path):
    project_dir = _project_fixture(tmp_path)

    assert sync_docs(project_dir) == 0

    for dest_name in SOURCE_FILES:
        destination = project_dir / DESTINATION_RELATIVE / dest_name
        assert destination.read_text(encoding="utf-8") == f"source: {dest_name}\n"


def test_sync_docs_fails_before_copying_when_source_is_missing(tmp_path):
    project_dir = _project_fixture(tmp_path)
    missing_source = project_dir / next(iter(SOURCE_FILES.values()))
    missing_source.unlink()

    assert sync_docs(project_dir) == 1
    assert not (project_dir / DESTINATION_RELATIVE / missing_source.name).exists()


def test_sync_docs_is_available_through_cli(tmp_path):
    project_dir = _project_fixture(tmp_path)

    assert main(["sync-docs", "--project-dir", str(project_dir)]) == 0
    assert (project_dir / DESTINATION_RELATIVE / "pack_structure_spec.md").exists()
