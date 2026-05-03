import json
import logging

from app.infrastructure.logging.safe_logger import log_event


def test_log_event_outputs_valid_json(caplog):
    logger = logging.getLogger("test_logger")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = True

    event = {
        "event": "test_event",
        "request_id": "req-1",
        "correlation_id": "corr-1",
    }

    with caplog.at_level(logging.INFO, logger="test_logger"):
        log_event(logger, event)

    assert len(caplog.records) == 1

    parsed = json.loads(caplog.records[0].message)

    assert parsed["event"] == "test_event"
    assert parsed["request_id"] == "req-1"
    assert parsed["correlation_id"] == "corr-1"
    assert "timestamp" in parsed
    assert "service" in parsed
    assert "version" in parsed
