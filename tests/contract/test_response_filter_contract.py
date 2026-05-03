from app.api.response_filter import filter_decision_response


def test_age_decision_response_filter_ignores_internal_fields():
    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "default",
        "majority_country": None,
    }

    response = filter_decision_response(
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
                    "signal_quality": "medium",
                    "threshold_separation": "high",
                },
            },
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
            "internal_estimate": 25,
            "signal_quality_score": 0.99,
            "raw_scores": {"age": 25},
            "internal_thresholds": {"margin": 2},
        }
    )

    dumped = response.model_dump()

    assert "internal_estimate" not in dumped
    assert "signal_quality_score" not in dumped
    assert "raw_scores" not in dumped
    assert "internal_thresholds" not in dumped
