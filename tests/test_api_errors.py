from fastapi.testclient import TestClient

from shodak.api.app import app
from shodak.api.errors import LlmProviderUnavailableError

client=TestClient(app)


def test_custom_api_handler():
    @app.get("/test-error")
    def test_error():
        raise LlmProviderUnavailableError()
    response=client.get("/test-error")
    assert response.json()=={
        "error": "llm_provider_unavailable",
        "message": (
            "No Configured LLM provider is currently available."
        )
    }