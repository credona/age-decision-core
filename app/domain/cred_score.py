class CredScoreCalculator:
    """
    Computes a normalized credibility score for an age decision.

    The cred_score is not a proof of truth.
    It represents how reliable the probabilistic decision appears based on
    model confidence and distance from the configured age threshold.
    """

    def compute(
        self,
        decision: str,
        confidence: float | None,
        estimated_age: float | None,
        threshold: int,
        margin: int,
    ) -> dict:
        if decision == "unknown" or confidence is None or estimated_age is None:
            return {
                "score": 0.0,
                "level": "none",
                "factors": {
                    "age_confidence": confidence,
                    "threshold_distance": None,
                },
            }

        distance = abs(estimated_age - threshold)

        if margin <= 0:
            distance_factor = 1.0
        else:
            distance_factor = min(distance / (margin * 3), 1.0)

        score = round((confidence * 0.7) + (distance_factor * 0.3), 4)

        if score >= 0.85:
            level = "high"
        elif score >= 0.65:
            level = "medium"
        elif score > 0:
            level = "low"
        else:
            level = "none"

        return {
            "score": score,
            "level": level,
            "factors": {
                "age_confidence": confidence,
                "threshold_distance": round(distance, 4),
            },
        }