"""Tests for MiniMax support in the LLM helper."""

import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest


@pytest.fixture
def llm_api(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> ModuleType:
    """Load the standalone LLM helper without reading project env files."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.local").write_text("# Test environment\n")
    module_path = Path(__file__).parents[2] / "tools" / "llm_api.py"
    spec = importlib.util.spec_from_file_location("llm_api_tool", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("provider", "region", "client_name", "expected_url"),
    [
        ("minimax", "global_en", "OpenAI", "https://api.minimax.io/v1"),
        ("minimax", "cn_zh", "OpenAI", "https://api.minimaxi.com/v1"),
        (
            "minimax_anthropic",
            "global_en",
            "Anthropic",
            "https://api.minimax.io/anthropic",
        ),
        (
            "minimax_anthropic",
            "cn_zh",
            "Anthropic",
            "https://api.minimaxi.com/anthropic",
        ),
    ],
)
def test_create_minimax_client_uses_region(
    monkeypatch: pytest.MonkeyPatch,
    llm_api: ModuleType,
    provider: str,
    region: str,
    client_name: str,
    expected_url: str,
) -> None:
    captured: dict[str, Any] = {}

    def fake_client(**kwargs: Any) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setenv("MINIMAX_API_KEY", "test-key")
    monkeypatch.setenv("MINIMAX_REGION", region)
    monkeypatch.setattr(llm_api, client_name, fake_client)

    llm_api.create_llm_client(provider)

    assert captured == {"api_key": "test-key", "base_url": expected_url}


def test_create_minimax_client_rejects_unknown_region(
    monkeypatch: pytest.MonkeyPatch, llm_api: ModuleType
) -> None:
    monkeypatch.setenv("MINIMAX_API_KEY", "test-key")
    monkeypatch.setenv("MINIMAX_REGION", "unknown")

    with pytest.raises(ValueError, match="MINIMAX_REGION"):
        llm_api.create_llm_client("minimax")


def test_minimax_openai_passes_m2_7_model(llm_api: ModuleType) -> None:
    captured: dict[str, Any] = {}

    def create(**kwargs: Any) -> SimpleNamespace:
        captured.update(kwargs)
        message = SimpleNamespace(content="ok")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))

    result = llm_api.query_llm(
        "hello",
        client=client,
        model="MiniMax-M2.7",
        provider="minimax",
    )

    assert result == "ok"
    assert captured["model"] == "MiniMax-M2.7"


def test_minimax_openai_supports_m3_images(tmp_path: Path, llm_api: ModuleType) -> None:
    image_path = tmp_path / "input.png"
    image_path.write_bytes(b"image")
    captured: dict[str, Any] = {}

    def create(**kwargs: Any) -> SimpleNamespace:
        captured.update(kwargs)
        message = SimpleNamespace(content="ok")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))

    result = llm_api.query_llm(
        "describe this",
        client=client,
        model="MiniMax-M3",
        provider="minimax",
        image_path=str(image_path),
    )

    assert result == "ok"
    assert captured["model"] == "MiniMax-M3"
    assert captured["messages"][0]["content"][1]["type"] == "image_url"


def test_minimax_anthropic_defaults_to_m3(llm_api: ModuleType) -> None:
    captured: dict[str, Any] = {}

    def create(**kwargs: Any) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(text="ok")])

    client = SimpleNamespace(messages=SimpleNamespace(create=create))

    result = llm_api.query_llm(
        "hello",
        client=client,
        provider="minimax_anthropic",
    )

    assert result == "ok"
    assert captured["model"] == "MiniMax-M3"
