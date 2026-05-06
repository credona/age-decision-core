from benchmarks.common.report import assert_report_is_privacy_safe, build_benchmark_report


def test_benchmark_report_is_privacy_safe():
    report = build_benchmark_report(
        benchmark_target="model",
        durations_ms=[10.0, 12.0, 14.0],
        decisions=["match", "no_match", "uncertain"],
        command="python -m benchmarks.model.run_model_benchmark",
        sample_count=3,
    )

    assert_report_is_privacy_safe(report)

    serialized = str(report).lower()

    assert "confidence" not in serialized
    assert "'raw_score':" not in serialized
    assert "'raw_scores':" not in serialized
    assert "'threshold':" not in serialized
    assert "'thresholds':" not in serialized
    assert "'internal_thresholds':" not in serialized
    assert "score_components" not in serialized
    assert "model_path" not in serialized
    assert "'base64':" not in serialized
    assert "payload" not in serialized
    assert "'downstream_raw_response':" not in serialized
    assert "'raw_response':" not in serialized


def test_benchmark_privacy_flags_are_false():
    report = build_benchmark_report(
        benchmark_target="service",
        durations_ms=[10.0],
        decisions=["match"],
        command="python -m benchmarks.service.run_service_benchmark",
        sample_count=1,
    )

    assert report["privacy"] == {
        "contains_raw_image": False,
        "contains_base64": False,
        "contains_downstream_raw_response": False,
        "contains_internal_thresholds": False,
        "contains_estimated_age": False,
        "contains_raw_scores": False,
    }
