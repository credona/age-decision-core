from app.application.ports.scientific_observer import NullScientificObserver


def test_null_scientific_observer_discards_private_signals() -> None:
    observer = NullScientificObserver()

    result = observer.observe_age_inference(
        internal_estimate=17.25,
        signal_quality_score=0.82,
    )

    assert result is None
