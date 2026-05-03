def test_health_contract_is_stable_and_privacy_first(client):
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {
        "status",
        "service",
        "version",
        "contract_version",
    }

    assert payload["status"] == "ok"

    assert "internal_estimate" not in payload
    assert "signal_quality_score" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload


def test_model_status_contract_is_stable_and_privacy_first(client):
    response = client.get("/engine/status")

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {"input_analysis", "inference"}

    assert "internal_estimate" not in payload
    assert "signal_quality_score" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
