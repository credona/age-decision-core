class CredScoreCalculator:
    """
    Computes a normalized credibility score for an age threshold decision.

    The score does not expose raw estimated age, raw confidence, or threshold
    distance. It only exposes categorical factors to preserve the privacy-first
    public contract.
    """

    def compute(
        self,
        decision: str,
        confidence: float | None,
        estimated_age: float | None,
        threshold: int,
        margin: int,
    ) -> dict:
        if decision == "uncertain" or confidence is None or estimated_age is None:
            return {
                "score": 0.0,
                "level": "none",
                "factors": {
                    "model_confidence": self._confidence_level(confidence),
                    "threshold_separation": "none",
                },
            }

        distance = abs(estimated_age - threshold)

        if margin <= 0:
            distance_factor = 1.0
        else:
            distance_factor = min(distance / (margin * 3), 1.0)

        score = round((confidence * 0.7) + (distance_factor * 0.3), 4)

        return {
            "score": score,
            "level": self._score_level(score),
            "factors": {
                "model_confidence": self._confidence_level(confidence),
                "threshold_separation": self._separation_level(distance_factor),
            },
        }

    def _score_level(self, score: float) -> str:
        if score >= 0.85:
            return "high"

        if score >= 0.65:
            return "medium"

        if score > 0:
            return "low"

        return "none"

    def _confidence_level(self, confidence: float | None) -> str:
        if confidence is None:
            return "none"

        if confidence >= 0.85:
            return "high"

        if confidence >= 0.65:
            return "medium"

        if confidence > 0:
            return "low"

        return "none"

    def _separation_level(self, distance_factor: float) -> str:
        if distance_factor >= 0.85:
            return "high"

        if distance_factor >= 0.5:
            return "medium"

        if distance_factor > 0:
            return "low"

        return "none"
