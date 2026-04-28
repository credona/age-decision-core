def test_version_returns_project_metadata(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "service_name": "age-decision-core",
        "app_name": "Age Decision Core",
        "version": "2.1.0",
        "contract_version": "2.0",
        "repository": "https://github.com/credona/age-decision-core",
        "image": "ghcr.io/credona/age-decision-core",
    }
