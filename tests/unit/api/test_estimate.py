from io import BytesIO

from unittest.mock import AsyncMock

import app.api.routes as routes


def test_estimate_returns_request_id_from_header(client, monkeypatch):
    expected_request_id = "test-request-123"

    cred_decision_score = {
        "score": 0.86,
        "level": "high",
        "factors": {
            "model_confidence": "medium",
            "threshold_separation": "high",
        },
    }

    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "majority_country",
        "majority_country": "FR",
    }

    mock_estimate = AsyncMock(
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
                "estimated_age_exposed": False,
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
            "model_info": {
                "face_detector": "YuNet",
                "age_estimator": "age-gender-prediction-ONNX",
                "age_model_path": "models/age_estimation/age-gender-prediction-ONNX.onnx",
                "face_detection_model_path": "models/face_detection/face_detection_yunet_2023mar.onnx",
            },
        }
    )

    monkeypatch.setattr(routes.age_estimation_service, "estimate", mock_estimate)

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
    assert payload["privacy"]["estimated_age_exposed"] is False
    assert payload["proof"]["type"] == "zk-ready"

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload

    mock_estimate.assert_awaited_once()
