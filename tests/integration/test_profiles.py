import json


def test_profile_creation_and_sync(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)

    assert run_cli(["profiles", "create", "frontend"], project_dir).returncode == 0
    assert (
        run_cli(["profiles", "add", "light-spec", "--to", "frontend"], project_dir).returncode
        == 0
    )

    list_out = run_cli(["profiles", "list"], project_dir)
    assert "frontend" in list_out.stdout

    result = run_cli(["project", "sync", "--profile", "frontend", "--cursor"], project_dir)
    assert result.returncode == 0

    status = json.loads(
        (project_dir / ".rulebook-ai" / "sync_status.json").read_text()
    )
    assert status["cursor"]["mode"] == "profile"
    assert status["cursor"]["profile"] == "frontend"


def test_profiles_add_and_remove_packs(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)
    run_cli(["profiles", "create", "frontend"], project_dir)
    run_cli(["profiles", "add", "light-spec", "--to", "frontend"], project_dir)

    result = run_cli(["profiles", "remove", "light-spec", "--from", "frontend"], project_dir)
    assert result.returncode == 0, result.stderr

    list_out = run_cli(["profiles", "list"], project_dir)
    assert "light-spec" not in list_out.stdout


def test_profiles_delete(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["profiles", "create", "frontend"], project_dir)
    result = run_cli(["profiles", "delete", "frontend"], project_dir)
    assert result.returncode == 0

    selection = json.loads((project_dir / ".rulebook-ai" / "selection.json").read_text())
    assert selection["profiles"] == {}

