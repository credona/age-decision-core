from app.application.ports.event_logger import EventLoggerPort
from app.infrastructure.logging.safe_logger import get_logger, log_event


class SafeEventLogger(EventLoggerPort):
    def __init__(self, name: str = "age_decision") -> None:
        self.logger = get_logger(name)

    def info(self, event: dict) -> None:
        log_event(self.logger, event)
