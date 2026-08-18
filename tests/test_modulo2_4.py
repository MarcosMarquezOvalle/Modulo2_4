import asyncio
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import modulo2_4
from modulo2_4 import fetch_url, fetch_url_async


@pytest.mark.asyncio
async def test_fetch_url_async_returns_status_code_on_success():
    class FakeClient:
        async def get(self, url, timeout):
            assert url == "https://example.com"
            assert timeout == 10.0
            return type("Response", (), {"status_code": 200})()

    result = await fetch_url_async(
        FakeClient(),
        "https://example.com",
        asyncio.Semaphore(1),
    )

    assert result == 200


@pytest.mark.asyncio
async def test_fetch_url_async_returns_none_on_http_error():
    class FakeClient:
        async def get(self, url, timeout):
            raise httpx.HTTPError("network error")

    result = await fetch_url_async(
        FakeClient(),
        "https://example.com",
        asyncio.Semaphore(1),
    )

    assert result is None


def test_fetch_url_returns_status_code_on_success(monkeypatch):
    class FakeResponse:
        status_code = 200

    def fake_get(url, timeout):
        assert url == "https://example.com"
        assert timeout == 5
        return FakeResponse()

    monkeypatch.setattr(modulo2_4.requests, "get", fake_get)

    assert fetch_url("https://example.com") == 200


def test_fetch_url_returns_none_on_request_exception(monkeypatch):
    def fake_get(url, timeout):
        raise modulo2_4.requests.exceptions.RequestException("request failed")

    monkeypatch.setattr(modulo2_4.requests, "get", fake_get)

    assert fetch_url("https://example.com") is None
