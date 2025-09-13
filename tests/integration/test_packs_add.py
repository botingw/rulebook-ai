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

def test_add_pack_with_source_conflict_fails(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    # 1. Add the built-in 'light-spec' pack first
    result1 = run_cli(["packs", "add", "light-spec"], project_dir)
    assert result1.returncode == 0, result1.stderr

    # Verify it's the built-in pack (no pack.json)
    assert not (project_dir / ".rulebook-ai" / "packs" / "light-spec" / "pack.json").exists()

    # 2. Create a local pack with the same name
    local_pack_dir = tmp_path / "sample_pack"
    local_pack_dir.mkdir()
    (local_pack_dir / "manifest.yaml").write_text(
        "name: light-spec\nversion: 9.9.9\nsummary: A conflicting local pack\n"
    )
    (local_pack_dir / "README.md").write_text("readme")
    rules_dir = local_pack_dir / "rules" / "01-rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "01-rule.md").write_text("local rule")

    # 3. Attempt to add the conflicting local pack
    result2 = run_cli(["packs", "add", f"local:{local_pack_dir}"], project_dir)

    # 4. Assert that the command fails
    assert result2.returncode != 0
    assert "already installed from a different source" in result2.stderr

    # 5. Assert that the original built-in pack is untouched
    selection = json.loads(
        (project_dir / ".rulebook-ai" / "selection.json").read_text()
    )
    assert len(selection["packs"]) == 1
    assert selection["packs"][0].get("version") != "9.9.9"  # Make sure it's not the new one
    assert not (
        project_dir / ".rulebook-ai" / "packs" / "light-spec" / "pack.json"
    ).exists()