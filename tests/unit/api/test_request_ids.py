from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_estimate_propagates_request_id_and_correlation_id(monkeypatch):
    async def fake_run(**kwargs):
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
                "signal_quality": "none",
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
            "rejection_reason": "no_face",
            "engine_info": {
                "input_analyzer": "YuNet",
                "inference_engine": "age-gender-prediction-ONNX",
            },
        }

    monkeypatch.setattr("app.api.routes.decision_pipeline.run", fake_run)

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

    assert "internal_estimate" not in payload
    assert "signal_quality_score" not in payload
    assert "is_adult" not in payload
    assert "cred_score" not in payload
