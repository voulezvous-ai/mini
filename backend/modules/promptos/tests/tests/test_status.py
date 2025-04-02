import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_status():
    # Note que para testar o endpoint /status, é necessário fornecer o header de API key.
    response = client.get("/status", headers={"x-api-key": "your_api_key"})
    assert response.status_code == 200
    assert "status" in response.json()