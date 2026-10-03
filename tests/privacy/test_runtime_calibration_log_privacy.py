from app.domain.privacy.safe_logging import sanitize_log_payload

FORBIDDEN_CALIBRATION_LOG_FIELDS = (
    "policy_id",
    "policy_version",
    "benchmark_attestation_id",
    "model_identifier",
    "payload_hash",
    "signature",
    "private_payload",
    "calibration_parameters",
    "decision_offset",
    "signal_quality_offset",
)


def test_runtime_calibration_metadata_is_not_loggable() -> None:
    payload = {
        "event": "calibration_activated",
        "decision": "match",
        "policy_id": "core-policy-v1",
        "policy_version": "1.0.0",
        "benchmark_attestation_id": "benchmark-private",
        "model_identifier": "credona.age.age-gender-onnx.v1",
        "payload_hash": "sha256:secret",
        "signature": "secret-signature",
        "private_payload": {
            "calibration_parameters": {
                "decision_offset": 3.0,
                "signal_quality_offset": 0.1,
            }
        },
    }

    sanitized = sanitize_log_payload(payload)
    serialized = str(sanitized)

    assert sanitized == {
        "event": "calibration_activated",
        "decision": "match",
    }

    for field in FORBIDDEN_CALIBRATION_LOG_FIELDS:
        assert field not in serialized
