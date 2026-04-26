from io import BytesIO

from unittest.mock import AsyncMock

from app.api.routes import age_estimation_service


def test_estimate_response_contains_cred_decision_score_and_legacy_cred_score(client):
    score = {
        "score": 0.86,
        "level": "high",
        "factors": {
            "age_confidence": 0.8,
            "threshold_distance": 7.0,
        },
    }

    age_estimation_service.estimate = AsyncMock(
        return_value={
            "request_id": "test-request-001",
            "correlation_id": "test-request-001",
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
            "cred_decision_score": score,
            "cred_score": score,
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

    response = client.post(
        "/estimate",
        headers={"X-Request-ID": "test-request-001"},
        files={
            "file": ("test-face.jpg", BytesIO(b"fake-image"), "image/jpeg"),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["cred_decision_score"] == score
    assert payload["cred_score"] == score