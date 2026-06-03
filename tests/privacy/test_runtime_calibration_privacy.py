from app.api.response_filter import filter_decision_response

FORBIDDEN_CALIBRATION_FIELDS = (
    "calibration_parameters",
    "decision_offset",
    "signal_quality_offset",
    "signal_quality_floor",
    "signal_quality_ceiling",
    "private_payload",
    "thresholds",
    "weights",
    "margins",
    "calibration_internals",
)


def test_response_filter_strips_runtime_calibration_private_fields() -> None:
    threshold = {
        "type": "minimum_age",
        "value": 18,
        "source": "default",
        "majority_country": None,
    }

    payload = {
        "request_id": "req-test",
        "correlation_id": "corr-test",
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
            "score": 0.91,
            "level": "high",
            "factors": {
                "signal_quality": "high",
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
            "claim": "age-threshold-decision",
            "threshold": threshold,
        },
        "rejection_reason": None,
        "engine_info": {
            "input_analyzer": "opencv",
            "inference_engine": "onnx",
        },
        "private_payload": {
            "calibration_parameters": {
                "decision_offset": 1.5,
                "signal_quality_offset": 0.05,
                "weights": {"private": 0.4},
                "margins": {"private": 2},
            }
        },
        "calibration_parameters": {
            "decision_offset": 1.5,
            "signal_quality_offset": 0.05,
        },
        "calibration_internals": {
            "thresholds": [18],
            "weights": [0.4],
            "margins": [2],
        },
    }

    filtered = filter_decision_response(payload)
    serialized = filtered.model_dump_json()

    for forbidden in FORBIDDEN_CALIBRATION_FIELDS:
        assert forbidden not in serialized
