from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.api.health import get_health_status

client = TestClient(app)


def test_health_is_degraded_without_provider():
    with (
        patch("shodak.api.app.get_health_status", return_value="degraded"),
        patch(
            "shodak.api.app.get_provider_status",
            return_value=[
                {"provider": "groq", "configured": False},
                {"provider": "openai", "configured": False},
            ],
        ),
    ):
        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert all(provider["configured"] is False for provider in data["providers"])


def test_health_status_is_healthy_when_provider_exisits():
    with (
        patch(
            "shodak.api.health.run_startup_checks",
            return_value=SimpleNamespace(healthy=True)
        ),
        patch(
            "shodak.api.health.get_provider_status",
            return_value=[{"provider": "groq", "configured": True}],
        )
    ):
        assert get_health_status() == "healthy"


def test_health_status_is_degraded_without_providers():
    with (
        patch(
            "shodak.api.health.run_startup_checks",
            return_value=SimpleNamespace(healthy=False)
        ),
        patch(
            "shodak.api.health.get_provider_status",
            return_value=[
                {"provider": "groq", "configured": False},
                {"provider": "openai", "configured": False},
            ],
        )
    ):
        assert get_health_status() == "degraded"
