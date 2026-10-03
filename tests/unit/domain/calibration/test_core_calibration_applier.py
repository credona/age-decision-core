from app.domain.calibration import (
    CalibrationPolicyMetadata,
    CoreCalibrationApplier,
    RuntimeCalibrationPolicy,
)


def make_policy(private_payload: dict) -> RuntimeCalibrationPolicy:
    return RuntimeCalibrationPolicy(
        metadata=CalibrationPolicyMetadata(
            policy_id="core-policy-test",
            service="core",
            contract_version="2.6",
            policy_version="1.0.0",
            benchmark_attestation_id="attestation-test",
            model_identifier="credona.age.age-gender-onnx.v1",
            payload_hash="sha256:test",
            signature="signature-test",
        ),
        private_payload=private_payload,
    )


def test_core_calibration_applier_is_neutral_without_policy() -> None:
    applier = CoreCalibrationApplier()

    result = applier.apply(
        internal_estimate=25.0,
        signal_quality_score=0.8,
    )

    assert result.internal_estimate == 25.0
    assert result.signal_quality_score == 0.8


def test_core_calibration_applier_applies_private_offsets() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "decision_offset": 1.5,
                "signal_quality_offset": 0.05,
            }
        }
    )
    applier = CoreCalibrationApplier(policy)

    result = applier.apply(
        internal_estimate=25.0,
        signal_quality_score=0.8,
    )

    assert result.internal_estimate == 26.5
    assert result.signal_quality_score == 0.85


def test_core_calibration_applier_clamps_age_and_signal_quality() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "decision_offset": 200.0,
                "signal_quality_offset": 2.0,
            }
        }
    )
    applier = CoreCalibrationApplier(policy)

    result = applier.apply(
        internal_estimate=25.0,
        signal_quality_score=0.8,
    )

    assert result.internal_estimate == 120.0
    assert result.signal_quality_score == 1.0


def test_core_calibration_applier_applies_signal_quality_floor_and_ceiling() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "signal_quality_floor": 0.6,
                "signal_quality_ceiling": 0.9,
            }
        }
    )
    applier = CoreCalibrationApplier(policy)

    low = applier.apply(internal_estimate=25.0, signal_quality_score=0.2)
    high = applier.apply(internal_estimate=25.0, signal_quality_score=0.95)

    assert low.signal_quality_score == 0.6
    assert high.signal_quality_score == 0.9


def test_core_calibration_applier_does_not_expose_policy_payload() -> None:
    policy = make_policy(
        {
            "calibration_parameters": {
                "decision_offset": 1.5,
                "private_weight": 0.4,
                "private_margin": 2.0,
            }
        }
    )
    applier = CoreCalibrationApplier(policy)

    result = applier.apply(
        internal_estimate=25.0,
        signal_quality_score=0.8,
    )

    assert not hasattr(result, "private_payload")
    assert not hasattr(result, "calibration_parameters")
    assert not hasattr(result, "private_weight")
    assert not hasattr(result, "private_margin")
