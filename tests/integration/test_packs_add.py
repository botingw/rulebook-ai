import json




def test_packs_add_is_config_only(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    result = run_cli(["packs", "add", "light-spec"], project_dir)
    assert result.returncode == 0, result.stderr

    rulebook_dir = project_dir / ".rulebook-ai"
    assert (rulebook_dir / "packs" / "light-spec").is_dir()

    selection = json.loads((rulebook_dir / "selection.json").read_text())
    assert selection["packs"][0]["name"] == "light-spec"

    # no memory/tools or rules until project sync
    assert not (project_dir / "memory").exists()
    assert not (project_dir / "tools").exists()
    assert not (project_dir / ".cursor").exists()
