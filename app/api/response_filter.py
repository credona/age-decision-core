from app.schemas.decision import DecisionResponse


def filter_decision_response(payload: dict) -> DecisionResponse:
    """
    Public API contract barrier.

    Any internal field not declared in DecisionResponse is ignored here.
    This prevents domain, application or infrastructure internals from leaking
    through the public API response.
    """
    return DecisionResponse(**payload)
