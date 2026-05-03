def test_model_status_returns_sections(client):
    response = client.get("/engine/status")

    assert response.status_code == 200

    data = response.json()

    assert "input_analysis" in data
    assert "inference" in data
