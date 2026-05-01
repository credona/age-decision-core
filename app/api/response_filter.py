from app.schemas.estimate import AgeDecisionResponse


def filter_age_decision_response(payload: dict) -> AgeDecisionResponse:
    """
    Public API contract barrier.

    Any internal field not declared in AgeDecisionResponse is ignored here.
    This prevents domain, application or infrastructure internals from leaking
    through the public API response.
    """
    return AgeDecisionResponse(**payload)
