from io import BytesIO
from unittest.mock import AsyncMock

import app.api.routes as routes


def test_estimate_returns_request_id_from_header(client, monkeypatch):
    expected_request_id = "test-request-123"

    cred_decision_score = {
        "score": 0.86,
        "level": "high",
        "factors": {
            "signal_quality": "medium",
            "threshold_separation": "high",
        },
    }

    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "majority_country",
        "majority_country": "FR",
    }

    mock_run = AsyncMock(
        return_value={
            "request_id": expected_request_id,
            "correlation_id": expected_request_id,
            "decision": "match",
            "threshold": threshold,
            "face_detected": True,
            "face_count": 1,
            "spoof_check_required": True,
            "spoof_check": {
                "status": "required",
                "passed": None,
                "provider": None,
            },
            "cred_decision_score": cred_decision_score,
            "privacy": {
                "image_stored": False,
                "biometric_template_stored": False,
                "internal_estimate_exposed": False,
                "processing": "ephemeral",
                "zk_ready": True,
            },
            "proof": {
                "type": "zk-ready",
                "status": "not_generated",
                "claim": "age_over_threshold",
                "threshold": threshold,
            },
            "rejection_reason": None,
            "engine_info": {
                "input_analyzer": "YuNet",
                "inference_engine": "age-gender-prediction-ONNX",
            },
        }
    )

    monkeypatch.setattr(routes.decision_pipeline, "run", mock_run)

    response = client.post(
        "/estimate?majority_country=FR",
        headers={"X-Request-ID": expected_request_id},
        files={
            "file": ("test-face.jpg", BytesIO(b"fake-image"), "image/jpeg"),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["request_id"] == expected_request_id
    assert payload["correlation_id"] == expected_request_id
    assert payload["decision"] == "match"
    assert payload["threshold"]["value"] == 18
    assert payload["threshold"]["majority_country"] == "FR"
    assert payload["cred_decision_score"]["level"] == "high"
    assert payload["privacy"]["image_stored"] is False
    assert payload["privacy"]["internal_estimate_exposed"] is False
    assert payload["proof"]["type"] == "zk-ready"

    assert "internal_estimate" not in payload
    assert "signal_quality_score" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload

    mock_run.assert_awaited_once()
