from io import BytesIO

from unittest.mock import AsyncMock

import app.api.routes as routes


def test_estimate_returns_request_id_from_header(client, monkeypatch):
    expected_request_id = "test-request-123"

    cred_decision_score = {
        "score": 0.86,
        "level": "high",
        "factors": {
            "age_confidence": 0.8,
            "threshold_distance": 7.0,
        },
    }

    mock_estimate = AsyncMock(
        return_value={
            "request_id": expected_request_id,
            "correlation_id": expected_request_id,
            "estimated_age": 25.0,
            "confidence": 0.8,
            "is_adult": True,
            "decision": "adult",
            "threshold": 18,
            "age_margin": 2,
            "confidence_threshold": 0.7,
            "country": "FR",
            "face_detected": True,
            "face_count": 1,
            "spoof_check_required": True,
            "spoof_check": {
                "status": "required",
                "passed": None,
                "provider": None,
            },
            "cred_decision_score": cred_decision_score,
            "cred_score": cred_decision_score,
            "privacy": {
                "image_stored": False,
                "biometric_template_stored": False,
                "processing": "ephemeral",
                "zk_ready": True,
            },
            "proof": {
                "type": "zk-ready",
                "status": "not_generated",
                "claim": "age_over_threshold",
                "threshold": 18,
            },
            "rejection_reason": None,
            "request_policy": {
                "threshold_source": "country",
                "country": "FR",
                "threshold": 18,
                "age_margin": 2,
                "confidence_threshold": 0.7,
            },
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
        "/estimate?country=FR",
        headers={"X-Request-ID": expected_request_id},
        files={
            "file": ("test-face.jpg", BytesIO(b"fake-image"), "image/jpeg"),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["request_id"] == expected_request_id
    assert payload["correlation_id"] == expected_request_id
    assert payload["decision"] == "adult"
    assert payload["cred_decision_score"]["level"] == "high"
    assert payload["cred_score"]["level"] == "high"
    assert payload["privacy"]["image_stored"] is False
    assert payload["proof"]["type"] == "zk-ready"

    mock_estimate.assert_awaited_once()