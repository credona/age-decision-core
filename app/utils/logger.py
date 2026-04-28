import json
import logging
from datetime import UTC, datetime

from app.config import settings
from app.project import project_metadata


def get_logger(name: str = "age_decision") -> logging.Logger:
    """
    Configure and return a structured JSON logger.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(settings.log_level.upper())
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler)

    return logger


def log_event(logger: logging.Logger, event: dict) -> None:
    """
    Log a structured JSON event.

    No image content, base64 payload, file path, or biometric template
    should ever be logged.
    """
    payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "service": project_metadata.service_name,
        "version": project_metadata.version,
        "contract_version": project_metadata.contract_version,
        **event,
    }

    logger.info(json.dumps(payload, ensure_ascii=False, default=str))
