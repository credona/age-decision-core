from io import BytesIO
from unittest.mock import AsyncMock

from app.api.routes import decision_pipeline


def test_estimate_response_contains_privacy_first_cred_decision_score(client):
    score = {
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

    decision_pipeline.run = AsyncMock(
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
    assert payload["privacy"]["internal_estimate_exposed"] is False

    assert "internal_estimate" not in payload
    assert "signal_quality_score" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
