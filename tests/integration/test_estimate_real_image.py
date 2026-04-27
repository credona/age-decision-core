from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_estimate_with_real_image():
    image_path = Path("tests/integration/assets/adult_sample.jpg")

    with image_path.open("rb") as f:
        response = client.post(
            "/estimate",
            files={"file": ("adult.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200

    payload = response.json()

    assert "request_id" in payload
    assert "correlation_id" in payload
    assert payload["face_detected"] is True
    assert payload["cred_decision_score"]["score"] >= 0

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
