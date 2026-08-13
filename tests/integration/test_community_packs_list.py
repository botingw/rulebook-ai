import json
from pathlib import Path

def _write_cache(data: dict, cache_path: Path) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data, indent=2))


def test_packs_list_shows_builtin_and_community(tmp_path, run_cli):
    cache_path = tmp_path / "cache.json"
    index = {
        "packs": [
            {
                "name": "good-pack",
                "username": "user",
                "repo": "good-pack",
                "description": "desc",
            }
        ]
    }
    _write_cache(index, cache_path)
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(
        ["packs", "list"],
        project_dir,
        env={"RULEBOOK_AI_INDEX_CACHE_PATH": str(cache_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "light-spec" in result.stdout
    assert "good-pack" in result.stdout
    assert "(community)" in result.stdout
    assert "desc" in result.stdout


def test_packs_list_does_not_hit_network(tmp_path, run_cli):
    cache_path = tmp_path / "cache.json"
    _write_cache({"packs": []}, cache_path)
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    env = {
        "RULEBOOK_AI_INDEX_URL": "http://example.invalid",
        "RULEBOOK_AI_INDEX_CACHE_PATH": str(cache_path),
    }
    result = run_cli(["packs", "list"], project_dir, env=env)
    assert result.returncode == 0, result.stderr
