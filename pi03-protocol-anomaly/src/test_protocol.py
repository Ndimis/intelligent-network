import pytest
from protocol_engine import ProtocolAnomalyDetector

@pytest.fixture
def detector():
    return ProtocolAnomalyDetector()

def test_legitimate_traffic(detector):
    """Standard web-like traffic should be accepted."""
    stream = [60, 800, 1400, 60, 500]
    result = detector.analyze_stream(stream)
    # Use == for value comparison
    assert result == False 

def test_exfiltration_anomaly(detector):
    """Heavy, uniform large packets should trigger an anomaly."""
    stream = [1500, 1500, 1500, 1500, 1500, 1500]
    result = detector.analyze_stream(stream)
    # Use == for value comparison
    assert result == True

def test_insufficient_data(detector):
    """Ensure the model doesn't alert on too few packets."""
    stream = [1500, 1500] 
    result = detector.analyze_stream(stream)
    assert result == False