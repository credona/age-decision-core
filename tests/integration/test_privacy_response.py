from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_estimate_does_not_leak_sensitive_data():
    image_path = Path("tests/integration/assets/adult_sample.jpg")

    with image_path.open("rb") as f:
        response = client.post(
            "/estimate",
            files={"file": ("adult.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200

    payload = response.json()

    # Privacy contract
    assert payload["privacy"]["image_stored"] is False
    assert payload["privacy"]["biometric_template_stored"] is False

    # No raw data leakage
    forbidden_keys = [
        "image_bytes",
        "base64",
        "file_path",
        "raw_image",
        "embedding",
    ]

    payload_str = str(payload)

    for key in forbidden_keys:
        assert key not in payload_str