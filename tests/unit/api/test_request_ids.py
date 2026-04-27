from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_estimate_propagates_request_id_and_correlation_id(monkeypatch):
    async def fake_estimate(**kwargs):
        threshold = {
            "type": "minimum_age",
            "value": 18,
            "source": "default",
            "majority_country": None,
        }

        cred_decision_score = {
            "score": 0.0,
            "level": "none",
            "factors": {
                "model_confidence": "none",
                "threshold_separation": "none",
            },
        }

        return {
            "request_id": kwargs["request_id"],
            "correlation_id": kwargs["correlation_id"],
            "decision": "uncertain",
            "threshold": threshold,
            "face_detected": False,
            "face_count": 0,
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
            "rejection_reason": "no_face",
            "model_info": {
                "face_detector": "YuNet",
                "age_estimator": "age-gender-prediction-ONNX",
                "age_model_path": "models/age_estimation/age-gender-prediction-ONNX.onnx",
                "face_detection_model_path": "models/face_detection/face_detection_yunet_2023mar.onnx",
            },
        }

    monkeypatch.setattr("app.api.routes.age_estimation_service.estimate", fake_estimate)

    response = client.post(
        "/estimate",
        headers={
            "X-Request-ID": "test-request-001",
            "X-Correlation-ID": "test-correlation-001",
        },
        files={
            "file": ("test.jpg", BytesIO(b"fake-image"), "image/jpeg"),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["request_id"] == "test-request-001"
    assert payload["correlation_id"] == "test-correlation-001"
    assert payload["decision"] == "uncertain"
    assert payload["cred_decision_score"]["level"] == "none"

    assert "estimated_age" not in payload
    assert "confidence" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
