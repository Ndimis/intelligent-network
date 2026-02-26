import pytest
from entropy_engine import DNSTunnelDetector

@pytest.fixture
def detector():
    return DNSTunnelDetector()

def test_safe_domains(detector):
    """Standard domains should always pass."""
    assert detector.evaluate("microsoft.com") is False
    assert detector.evaluate("github.com") is False

def test_base64_exfiltration(detector):
    """Classic Base64 encoded data should be caught by entropy."""
    query = "Zm9vYmFyYmF6MTIzNDU2Nzg5MA==.attacker.com"
    assert detector.evaluate(query) is True

def test_long_dictionary_evasion(detector):
    """Catch evasion attempts using long strings of dictionary words."""
    query = "confidential-internal-password-database-leak-v2.net"
    # Even if entropy is lower, the length + diversity should trigger it
    assert detector.evaluate(query) is True

def test_short_string_limitation(detector):
    """Verify that we don't flag tiny random strings (False Positive Prevention)."""
    assert detector.evaluate("a1b2.com") is False