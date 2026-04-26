def test_model_status_returns_sections(client):
    response = client.get("/model/status")

    assert response.status_code == 200

    data = response.json()

    assert "face_detection" in data
    assert "age_estimation" in data