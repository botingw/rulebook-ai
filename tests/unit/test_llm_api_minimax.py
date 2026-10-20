"""Tests for MiniMax support in the LLM helper."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest import TestCase

import httpx
import pytest
from anthropic import DefaultHttpxClient as AnthropicHttpClient
from openai import DefaultHttpxClient as OpenAIHttpClient

HELPER_PATHS = [
    "tools/llm_api.py",
    "rule_sets/tool_starters/llm_api.py",
    "src/rulebook_ai/packs/light-spec/tool_starters/llm_api.py",
    "src/rulebook_ai/packs/medium-spec/tool_starters/llm_api.py",
    "src/rulebook_ai/packs/heavy-spec/tool_starters/llm_api.py",
    "vscode-extension/manage_rules/python/tool_starters/llm_api.py",
    "vscode-extension/manage_rules/python/rule_sets/tool_starters/llm_api.py",
]


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


def test_minimax_anthropic_defaults_to_flash(llm_api: ModuleType) -> None:
    captured: dict[str, Any] = {}

    def create(**kwargs: Any) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(
            content=[
                SimpleNamespace(type="thinking", thinking="reasoning"),
                SimpleNamespace(type="text", text="ok"),
            ]
        )

    client = SimpleNamespace(messages=SimpleNamespace(create=create))

    result = llm_api.query_llm(
        "hello",
        client=client,
        provider="minimax_anthropic",
    )

    assert result == "ok"
    assert captured["model"] == "MiniMax-M3.1-Flash"


def sdk_http_module(provider: str) -> ModuleType:
    """Match the HTTP backend of both older and current SDK releases."""
    client_type = OpenAIHttpClient if provider == "minimax" else AnthropicHttpClient
    return importlib.import_module("httpx" if issubclass(client_type, httpx.Client) else "httpx2")


def mock_response(provider: str, model: str, backend: ModuleType) -> Any:
    """Return realistic SDK responses, including Flash's thinking block."""
    if provider == "minimax":
        return backend.Response(
            200,
            json={
                "id": "test",
                "object": "chat.completion",
                "created": 0,
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "ok"},
                    }
                ],
            },
        )
    content = [{"type": "text", "text": "ok"}]
    if model == "MiniMax-M3.1-Flash":
        content.insert(0, {"type": "thinking", "thinking": "reasoning", "signature": "test"})
    return backend.Response(
        200,
        json={
            "id": "test",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": content,
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 1, "output_tokens": 2},
        },
    )


@pytest.mark.parametrize("helper_path", HELPER_PATHS)
@pytest.mark.parametrize("provider", ["minimax", "minimax_anthropic"])
@pytest.mark.parametrize("region", ["global_en", "cn_zh"])
@pytest.mark.parametrize("entrypoint", ["api", "cli"])
@pytest.mark.parametrize(
    ("model", "image", "expected_model"),
    [
        (None, False, "MiniMax-M3.1-Flash"),
        ("MiniMax-M3.1-Flash", False, "MiniMax-M3.1-Flash"),
        ("MiniMax-M3", False, "MiniMax-M3"),
        ("MiniMax-M2.7", False, "MiniMax-M2.7"),
        ("saved-custom-model", False, "saved-custom-model"),
        (None, True, "MiniMax-M3"),
        ("MiniMax-M3.1-Flash", True, "MiniMax-M3.1-Flash"),
    ],
)
def test_minimax_serialized_requests(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    helper_path: str,
    provider: str,
    region: str,
    entrypoint: str,
    model: str | None,
    image: bool,
    expected_model: str,
) -> None:
    """Exercise each shipped helper through the SDK's HTTP serialization."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.local").write_text("# Test environment\n")
    monkeypatch.setenv("MINIMAX_API_KEY", "test-key")
    monkeypatch.setenv("MINIMAX_REGION", region)
    spec = importlib.util.spec_from_file_location(
        "llm_api_transport", Path(__file__).parents[2] / helper_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    requests: list[httpx.Request] = []
    backend = sdk_http_module(provider)

    def respond(request: httpx.Request) -> Any:
        requests.append(request)
        return mock_response(provider, expected_model, backend)

    client_name = "OpenAI" if provider == "minimax" else "Anthropic"
    sdk_client = getattr(module, client_name)
    with backend.Client(transport=backend.MockTransport(respond)) as http_client:

        def create_client(**kwargs: Any) -> Any:
            return sdk_client(http_client=http_client, max_retries=0, **kwargs)

        monkeypatch.setattr(module, client_name, create_client)
        image_path = tmp_path / "input.png"
        if image:
            image_path.write_bytes(b"image")
        if entrypoint == "cli":
            args = ["llm_api.py", "--provider", provider, "--prompt", "hello"]
            if model is not None:
                args.extend(["--model", model])
            if image:
                args.extend(["--image", str(image_path)])
            monkeypatch.setattr(sys, "argv", args)
            module.main()
            TestCase().assertEqual(capsys.readouterr().out.strip(), "ok")
        else:
            TestCase().assertEqual(
                module.query_llm(
                    "hello",
                    provider=provider,
                    model=model,
                    image_path=str(image_path) if image else None,
                ),
                "ok",
            )

    TestCase().assertEqual(len(requests), 1)
    host = "api.minimax.io" if region == "global_en" else "api.minimaxi.com"
    path = "/v1/chat/completions" if provider == "minimax" else "/anthropic/v1/messages"
    TestCase().assertEqual(str(requests[0].url), f"https://{host}{path}")
    payload = json.loads(requests[0].content)
    content = [{"type": "text", "text": "hello"}]
    if image:
        if provider == "minimax":
            content.append(
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,aW1hZ2U="}}
            )
        else:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": "aW1hZ2U=",
                    },
                }
            )
    expected = {"model": expected_model, "messages": [{"role": "user", "content": content}]}
    if provider == "minimax":
        expected["temperature"] = 0.7
    else:
        expected["max_tokens"] = 4096 if expected_model == "MiniMax-M3.1-Flash" else 1000
    # Omitted thinking/effort uses Flash's adaptive/max defaults, preserving other models.
    TestCase().assertEqual(payload, expected)


def test_llm_helpers_stay_synchronized() -> None:
    """Pack sync must ship the same helper as the standalone and editor copies."""
    root = Path(__file__).parents[2]
    TestCase().assertEqual(len({(root / path).read_bytes() for path in HELPER_PATHS}), 1)
