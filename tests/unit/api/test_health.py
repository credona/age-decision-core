def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "age-decision-core",
        "version": "2.1.1",
        "contract_version": "2.0",
    }
