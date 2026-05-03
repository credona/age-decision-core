def test_model_status_returns_sections(client):
    response = client.get("/engine/status")

    assert response.status_code == 200

    data = response.json()

    assert "input_analysis" in data
    assert "inference" in data


def test_model_status_exposes_model_identifier_not_model_path(client):
    response = client.get("/engine/status")

    assert response.status_code == 200

    inference = response.json()["inference"]

    assert "model_id" in inference
    assert "model_version" in inference
    assert "scoring_policy_id" in inference
    assert "path" not in inference
    assert "model_path" not in inference
