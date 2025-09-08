import os
def test_packs_list_shows_manifest_info(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    result = run_cli(["packs", "list"], project_dir)
    assert result.returncode == 0, result.stderr
    assert "light-spec" in result.stdout
    assert "v0.1.0" in result.stdout
    assert "simplification" in result.stdout
