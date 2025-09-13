import json


def test_project_clean_requires_confirmation(synced_project, run_cli):
    result = run_cli(["project", "clean"], synced_project, input_text="yes\n")
    assert result.returncode == 0
    assert not (synced_project / ".rulebook-ai").exists()
    assert not (synced_project / "memory").exists()
    assert not (synced_project / "tools").exists()


def test_project_clean_aborts_on_decline(synced_project, run_cli):
    result = run_cli(["project", "clean"], synced_project, input_text="no\n")
    assert result.returncode == 0
    assert (synced_project / ".rulebook-ai").exists()
    assert (synced_project / "memory").exists()


def test_project_clean_rules_preserves_context(synced_project, run_cli):
    result = run_cli(["project", "clean-rules"], synced_project)
    assert result.returncode == 0
    assert not (synced_project / ".rulebook-ai").exists()
    assert not (synced_project / ".cursor").exists()
    assert (synced_project / "memory").exists()
    assert (synced_project / "tools").exists()


def test_project_clean_context_removes_orphans(synced_project, run_cli):
    run_cli(["packs", "remove", "light-spec"], synced_project)
    assert (synced_project / "memory" / "docs" / "architecture_template.md").is_file()

    result = run_cli(
        ["project", "clean-context", "--action", "delete", "--force"],
        synced_project,
    )
    assert result.returncode == 0
    assert not (synced_project / "memory" / "docs" / "architecture_template.md").exists()
    manifest = json.loads((synced_project / ".rulebook-ai" / "file_manifest.json").read_text())
    assert "memory/docs/architecture_template.md" not in manifest
