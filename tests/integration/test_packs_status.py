import os
def test_packs_status_lists_library_and_profiles(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)
    run_cli(["profiles", "create", "frontend"], project_dir)
    run_cli(["profiles", "add", "light-spec", "--to", "frontend"], project_dir)

    result = run_cli(["packs", "status"], project_dir)
    assert result.returncode == 0, result.stderr
    assert "light-spec" in result.stdout
    assert "frontend" in result.stdout
