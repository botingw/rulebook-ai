import json
from pathlib import Path

CACHE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "rulebook_ai"
    / "community"
    / "index_cache"
    / "packs.json"
)

def _write_cache(data: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2))


def test_packs_list_shows_builtin_and_community(tmp_path, run_cli):
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
    _write_cache(index)
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    result = run_cli(["packs", "list"], project_dir)
    assert result.returncode == 0, result.stderr
    assert "light-spec" in result.stdout
    assert "good-pack" in result.stdout
    assert "(community)" in result.stdout
    assert "desc" in result.stdout


def test_packs_list_does_not_hit_network(tmp_path, run_cli):
    _write_cache({"packs": []})
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    env = {"RULEBOOK_AI_INDEX_URL": "http://example.invalid"}
    result = run_cli(["packs", "list"], project_dir, env=env)
    assert result.returncode == 0, result.stderr
