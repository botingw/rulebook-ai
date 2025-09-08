
import json


def test_add_multiple_packs(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    result = run_cli(["packs", "add", "light-spec", "heavy-spec"], project_dir)
    assert result.returncode == 0, result.stderr

    selection = json.loads((project_dir / ".rulebook-ai" / "selection.json").read_text())
    assert [p["name"] for p in selection["packs"]] == ["light-spec", "heavy-spec"]


def test_add_nonexistent_pack_fails(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    result = run_cli(["packs", "add", "ghost-pack"], project_dir)
    assert result.returncode != 0
    assert "not found" in result.stdout
    assert not (project_dir / ".rulebook-ai").exists()


def test_remove_pack_updates_selection(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)
    assert run_cli(["packs", "remove", "light-spec"], project_dir).returncode == 0

    selection = json.loads((project_dir / ".rulebook-ai" / "selection.json").read_text())
    assert selection["packs"] == []
    assert not (project_dir / ".rulebook-ai" / "packs" / "light-spec").exists()


def test_remove_pack_does_not_touch_context(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)
    run_cli(["project", "sync", "--cursor"], project_dir)
    assert (project_dir / "memory" / "docs" / "architecture_template.md").is_file()
    assert (project_dir / "tools" / "web_scraper.py").is_file()

    run_cli(["packs", "remove", "light-spec"], project_dir)
    assert (project_dir / "memory" / "docs" / "architecture_template.md").is_file()
    assert (project_dir / "tools" / "web_scraper.py").is_file()


def test_remove_nonexistent_pack_fails(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    result = run_cli(["packs", "remove", "ghost-pack"], project_dir)
    assert result.returncode != 0
    assert "not installed" in result.stdout
