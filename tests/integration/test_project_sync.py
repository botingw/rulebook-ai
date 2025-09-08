import json


def test_project_sync_with_pack_flag(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    assert run_cli(["packs", "add", "light-spec"], project_dir).returncode == 0
    assert run_cli(["packs", "add", "heavy-spec"], project_dir).returncode == 0

    result = run_cli(
        ["project", "sync", "--pack", "light-spec", "--cursor"], project_dir
    )
    assert result.returncode == 0, result.stderr

    arch_file = project_dir / "memory" / "docs" / "architecture_template.md"
    assert arch_file.is_file()

    manifest = json.loads(
        (project_dir / ".rulebook-ai" / "file_manifest.json").read_text()
    )
    assert manifest["memory/docs/architecture_template.md"] == "light-spec"

    status = json.loads(
        (project_dir / ".rulebook-ai" / "sync_status.json").read_text()
    )
    assert status["cursor"]["mode"] == "pack"
    assert status["cursor"]["pack_count"] == 1

    status_result = run_cli(["project", "status"], project_dir)
    assert "cursor" in status_result.stdout


def test_project_sync_all_packs(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec", "heavy-spec"], project_dir)

    result = run_cli(["project", "sync", "--cursor"], project_dir)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(
        (project_dir / ".rulebook-ai" / "file_manifest.json").read_text()
    )
    assert manifest["memory/docs/architecture_template.md"] == "light-spec"
    status = json.loads((project_dir / ".rulebook-ai" / "sync_status.json").read_text())
    assert status["cursor"]["pack_count"] == 2
    assert set(status["cursor"]["packs"]) == {"light-spec", "heavy-spec"}


def test_project_sync_with_profile(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec", "heavy-spec"], project_dir)
    run_cli(["profiles", "create", "frontend"], project_dir)
    run_cli(["profiles", "add", "light-spec", "--to", "frontend"], project_dir)

    result = run_cli(["project", "sync", "--profile", "frontend", "--cursor"], project_dir)
    assert result.returncode == 0, result.stderr

    manifest = json.loads(
        (project_dir / ".rulebook-ai" / "file_manifest.json").read_text()
    )
    assert manifest["memory/docs/architecture_template.md"] == "light-spec"
    status = json.loads((project_dir / ".rulebook-ai" / "sync_status.json").read_text())
    assert status["cursor"]["mode"] == "profile"
    assert status["cursor"]["pack_count"] == 1
    assert status["cursor"]["packs"] == ["light-spec"]


def test_project_status_reports_last_sync(tmp_path, run_cli):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    run_cli(["packs", "add", "light-spec"], project_dir)
    run_cli(["project", "sync", "--cursor"], project_dir)
    run_cli(["project", "sync", "--windsurf", "--pack", "light-spec"], project_dir)

    out = run_cli(["project", "status"], project_dir)
    assert "cursor" in out.stdout and "all" in out.stdout
    assert "windsurf" in out.stdout and "pack" in out.stdout
