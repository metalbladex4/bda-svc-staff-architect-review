"""Pipeline interfaces tests."""

from unittest.mock import patch

import pytest

from bda_svc.pipeline.interfaces import OllamaVLM

# ----------------------------------------------------------------------
# Network host variable tests
# ----------------------------------------------------------------------


def test_uses_default_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """OllamaVLM defaults to localhost when OLLAMA_HOST is unset."""
    monkeypatch.delenv("OLLAMA_HOST", raising=False)

    vlm = OllamaVLM(model="test-model")

    assert vlm.client._client.base_url == "http://localhost:11434"


def test_uses_env_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """OllamaVLM uses OLLAMA_HOST when environment variable is set."""
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:12345")

    vlm = OllamaVLM(model="test-model")

    assert vlm.client._client.base_url == "http://localhost:12345"


# ----------------------------------------------------------------------
# Client initialization tests
# ----------------------------------------------------------------------


def test_client_initialized_with_env_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """OllamaVLM passes OLLAMA_HOST to Client on init."""
    # OllamaVLM creates a Client with the correct host based on environment variable
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:12345")

    with patch("bda_svc.pipeline.interfaces.Client") as mock_client:
        OllamaVLM(model="test-model")
        mock_client.assert_called_with(host="http://localhost:12345", headers=None)


def test_client_initialized_with_api_key_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OllamaVLM passes the API key as a bearer token header."""
    monkeypatch.setenv("OLLAMA_API_KEY", "secret-key")

    with patch("bda_svc.pipeline.interfaces.Client") as mock_client:
        OllamaVLM(model="test-model")
        mock_client.assert_called_with(
            host="http://localhost:11434",
            headers={"Authorization": "Bearer secret-key"},
        )
