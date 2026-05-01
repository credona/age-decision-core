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

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload


def test_model_status_contract_is_stable_and_privacy_first(client):
    response = client.get("/model/status")

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {"face_detection", "age_estimation"}

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
