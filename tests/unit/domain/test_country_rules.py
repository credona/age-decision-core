from app.policies.country_rules import CountryRules


def test_country_threshold_known():
    rules = CountryRules()

    assert rules.get_threshold("fr") == 18
    assert rules.get_threshold("US") == 21


def test_country_threshold_unknown():
    rules = CountryRules()

    assert rules.get_threshold("XX") is None


def test_country_threshold_none():
    rules = CountryRules()

    assert rules.get_threshold(None) is None
