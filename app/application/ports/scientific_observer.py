from typing import Protocol


class ScientificObserverPort(Protocol):
    """
    Private scientific observation port.

    Implementations may consume internal model signals for authorized,
    private benchmark execution. Observations must never be added to
    public API responses or production logs.
    """

    def observe_age_inference(
        self,
        *,
        internal_estimate: float,
        signal_quality_score: float,
    ) -> None: ...


class NullScientificObserver:
    """
    Default production-safe observer.

    Intentionally discards all private scientific observations.
    """

    def observe_age_inference(
        self,
        *,
        internal_estimate: float,
        signal_quality_score: float,
    ) -> None:
        return None
