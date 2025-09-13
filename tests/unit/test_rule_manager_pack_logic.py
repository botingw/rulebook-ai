import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from rulebook_ai.core import RuleManager

def test_list_packs_reads_manifest(tmp_path, capsys):
    """list_packs should read manifest.yaml and print version and summary."""
    # Create a fake pack with manifest
    pack_dir = tmp_path / "demo-pack"
    pack_dir.mkdir()
    (pack_dir / "manifest.yaml").write_text(
        "name: demo-pack\nversion: 1.2.3\nsummary: Demo pack for testing\n"
    )

    manager = RuleManager(project_root=str(tmp_path))
    manager.source_packs_dir = tmp_path

    manager.list_packs()
    captured = capsys.readouterr().out

    assert "demo-pack" in captured
    assert "v1.2.3" in captured
    assert "Demo pack for testing" in captured

