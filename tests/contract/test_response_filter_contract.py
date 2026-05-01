from app.api.response_filter import filter_age_decision_response


def test_age_decision_response_filter_ignores_internal_fields():
    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "default",
        "majority_country": None,
    }

    response = filter_age_decision_response(
        {
            "request_id": "req-1",
            "correlation_id": "corr-1",
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
            "cred_decision_score": {
                "score": 0.8,
                "level": "high",
                "factors": {
                    "model_confidence": "medium",
                    "threshold_separation": "high",
                },
            },
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
                "age_model_path": "/internal/model.onnx",
                "face_detection_model_path": "/internal/face.onnx",
            },
            "estimated_age": 25,
            "confidence": 0.99,
            "raw_scores": {"age": 25},
            "internal_thresholds": {"margin": 2},
        }
    )

    dumped = response.model_dump()

    assert "estimated_age" not in dumped
    assert "confidence" not in dumped
    assert "raw_scores" not in dumped
    assert "internal_thresholds" not in dumped
