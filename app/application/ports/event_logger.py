from typing import Protocol


class EventLoggerPort(Protocol):
    def info(self, event: dict) -> None: ...


class NullEventLogger:
    def info(self, event: dict) -> None:
        return None
