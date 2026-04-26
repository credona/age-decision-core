from app.config import settings


class CountryRules:
    """
    Provides age threshold rules by country (ISO 3166-1 alpha-2).

    Behavior:
    - Normalize input (uppercase, strip)
    - Return None if no rule exists
    - Allow extension via settings if needed
    """

    DEFAULT_MAPPING = {
        "FR": 18,
        "US": 21,
        "JP": 18,
        "DE": 18,
        "ES": 18,
        "IT": 18,
        "UK": 18,
        "CA": 18,
        "AU": 18,
        "KR": 19,  # South Korea
    }

    def __init__(self):
        # Future extension point (env override)
        self.mapping = self._build_mapping()

    def _build_mapping(self) -> dict:
        """
        Build final mapping.

        In v1.1 this simply returns DEFAULT_MAPPING,
        but this method allows future override from environment or config.
        """
        return self.DEFAULT_MAPPING

    def get_threshold(self, country_code: str | None) -> int | None:
        """
        Return the configured age threshold for a country code.

        Returns:
            int: threshold if found
            None: if country is unknown or not provided
        """
        if not country_code:
            return None

        normalized = self._normalize(country_code)

        return self.mapping.get(normalized)

    def _normalize(self, country_code: str) -> str:
        """
        Normalize country code input.
        """
        return country_code.strip().upper()