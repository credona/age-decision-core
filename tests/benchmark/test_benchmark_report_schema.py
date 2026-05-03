import json
from pathlib import Path

from benchmarks.common.report import build_benchmark_report


def test_benchmark_schema_is_valid_json():
    schema = json.loads(Path("benchmarks/schemas/benchmark-report.schema.json").read_text())

    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert schema["properties"]["service"]["enum"] == ["core"]
    assert schema["properties"]["benchmark_target"]["enum"] == ["model", "service"]


def test_benchmark_report_contains_required_public_fields_only():
    report = build_benchmark_report(
        benchmark_target="model",
        durations_ms=[10.0, 20.0, 30.0],
        decisions=["match", "match", "uncertain"],
        command="python -m benchmarks.model.run_model_benchmark",
        sample_count=3,
    )

    assert set(report) == {
        "benchmark_id",
        "benchmark_version",
        "generated_at",
        "service",
        "service_version",
        "contract_version",
        "benchmark_target",
        "dataset",
        "machine",
        "runtime",
        "metrics",
        "privacy",
    }

    assert report["service"] == "core"
    assert report["benchmark_target"] == "model"
    assert report["privacy"] == {
        "contains_sensitive_data": False,
        "contains_raw_inputs": False,
        "contains_internal_scores": False,
        "contains_internal_thresholds": False,
    }


def test_benchmark_report_decision_distribution_is_aggregate_only():
    report = build_benchmark_report(
        benchmark_target="service",
        durations_ms=[10.0, 20.0, 30.0],
        decisions=["match", "no_match", "unknown"],
        command="python -m benchmarks.service.run_service_benchmark",
        sample_count=3,
    )

    assert report["metrics"]["decision_distribution"] == {
        "match": 1,
        "no_match": 1,
        "uncertain": 0,
    }
