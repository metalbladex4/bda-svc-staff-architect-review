"""Pipeline interfaces tests."""

from unittest.mock import patch

import pytest
from PIL import Image

from bda_svc.pipeline.interfaces import VLMBackend

# ----------------------------------------------------------------------
# Network host variable tests
# ----------------------------------------------------------------------


def test_uses_default_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """VLMBackend defaults to localhost when OPENAI_BASE_URL is unset."""
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)

    vlm = VLMBackend(model="test-model")

    assert vlm.client.base_url == "http://localhost:8000/v1/"


def test_uses_env_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """VLMBackend uses OPENAI_BASE_URL when environment variable is set."""
    monkeypatch.setenv("OPENAI_BASE_URL", "http://localhost:11434/v1")

    vlm = VLMBackend(model="test-model")

    assert vlm.client.base_url == "http://localhost:11434/v1/"


# ----------------------------------------------------------------------
# Client initialization tests
# ----------------------------------------------------------------------


def test_client_initialized_with_env_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """VLMBackend passes OPENAI_BASE_URL to OpenAI on init."""
    monkeypatch.setenv("OPENAI_BASE_URL", "http://localhost:12345/v1")

    with patch("bda_svc.pipeline.interfaces.OpenAI") as mock_client:
        VLMBackend(model="test-model")
        mock_client.assert_called_with(
            base_url="http://localhost:12345/v1",
            api_key="no-auth",
        )


def test_client_initialized_with_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """VLMBackend passes OPENAI_API_KEY directly to OpenAI."""
    monkeypatch.setenv("OPENAI_API_KEY", "secret-key")

    with patch("bda_svc.pipeline.interfaces.OpenAI") as mock_client:
        VLMBackend(model="test-model")
        mock_client.assert_called_with(
            base_url="http://localhost:8000/v1",
            api_key="secret-key",
        )


# ----------------------------------------------------------------------
# Generate method tests
# ----------------------------------------------------------------------


def test_system_prompt_is_sent_as_first_message() -> None:
    """VLMBackend includes the system prompt as the first message."""
    with patch("bda_svc.pipeline.interfaces.OpenAI") as mock_client:
        image = Image.new("RGB", (100, 100))
        vlm = VLMBackend(model="test-model")
        vlm.generate(image, prompt="What is this?", system_prompt="You are helpful.")
        messages = mock_client.return_value.chat.completions.create.call_args.kwargs[
            "messages"
        ]
        assert messages[0] == {"role": "system", "content": "You are helpful."}


def test_no_system_prompt_omits_system_message() -> None:
    """VLMBackend sends no system message when system_prompt absent."""
    with patch("bda_svc.pipeline.interfaces.OpenAI") as mock_client:
        image = Image.new("RGB", (100, 100))
        vlm = VLMBackend(model="test-model")
        vlm.generate(image, prompt="What is this?", temperature=0.0)
        messages = mock_client.return_value.chat.completions.create.call_args.kwargs[
            "messages"
        ]
        assert all(m["role"] != "system" for m in messages)
