import json
from pathlib import Path


def test_health_returns_ok(client):
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": project["service_name"],
        "version": project["version"],
        "contract_version": project["contract_version"],
    }
