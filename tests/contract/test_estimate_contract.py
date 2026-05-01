from io import BytesIO
from unittest.mock import AsyncMock

from app.api.routes import age_estimation_service


def test_estimate_response_contains_privacy_first_cred_decision_score(client):
    score = {
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

    age_estimation_service.estimate = AsyncMock(
        return_value={
            "request_id": "test-request-001",
            "correlation_id": "test-request-001",
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
            "cred_decision_score": score,
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
                "face_detection_model_path": (
                    "models/face_detection/face_detection_yunet_2023mar.onnx"
                ),
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
    assert payload["decision"] == "match"
    assert payload["threshold"] == threshold
    assert payload["privacy"]["estimated_age_exposed"] is False

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
