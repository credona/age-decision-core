from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_estimate_propagates_request_id_and_correlation_id(monkeypatch):
    async def fake_estimate(**kwargs):
        cred_decision_score = {
            "score": 0.0,
            "level": "none",
            "factors": {
                "age_confidence": None,
                "threshold_distance": None,
            },
        }

        return {
            "request_id": kwargs["request_id"],
            "correlation_id": kwargs["correlation_id"],
            "estimated_age": None,
            "confidence": None,
            "is_adult": None,
            "decision": "unknown",
            "threshold": 18,
            "age_margin": 2,
            "confidence_threshold": 0.7,
            "country": None,
            "face_detected": False,
            "face_count": 0,
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
            "rejection_reason": "no_face",
            "request_policy": {
                "threshold_source": "default",
                "country": None,
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
    assert payload["cred_decision_score"]["level"] == "none"
    assert payload["cred_score"]["level"] == "none"