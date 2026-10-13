from unittest.mock import patch

from fastapi.testclient import TestClient

from shodak.api.app import app

client=TestClient(app)


def test_root_endpoint():
    response=client.get("/")
    assert response.status_code==200
    data=response.json()
    assert data["name"]=="Shodak"
    assert data["status"]=="running"


def test_health_endpoint():
    with (
        patch(
            "shodak.api.app.get_health_status",
            return_value="healthy"
        ),
        patch(
            "shodak.api.app.get_provider_status",
            return_value=[
                {
                    "provider":"groq",
                    "configured":True
                },
                {
                    "provider":"openai",
                    "configured":True
                }
            ]
        )
    ):
        response=client.get("/health")
    assert response.status_code==200
    data=response.json()
    assert data["status"]=="healthy"
    assert data["app_name"]=="Shodak"
    assert "environment" in data
    assert data["primary_provider"]=="groq"
    assert len(data["providers"])==2
    assert data["providers"][0]=={
        "provider":"groq",
        "configured":True
    }