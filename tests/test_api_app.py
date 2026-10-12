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
    response=client.get("/health")
    assert response.status_code==200
    data=response.json()
    assert data["status"]=="healthy"
    assert data["environment"]=="development"
