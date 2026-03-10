import pytest
from shaper_engine import TrafficShaper

def test_critical_app_priority():
    shaper = TrafficShaper()
    metrics = [300, 10, 16, 100] # Very poor network conditions
    
    voip_limit = shaper.get_shaping_decision(metrics, "VOIP")
    bulk_limit = shaper.get_shaping_decision(metrics, "BULK_DATA")
    
    assert voip_limit > bulk_limit, "VOIP should always have a higher limit than Bulk Data"

def test_minimum_guarantee():
    shaper = TrafficShaper()
    metrics = [500, 20, 12, 1000] # Extreme congestion
    voip_limit = shaper.get_shaping_decision(metrics, "VOIP")
    assert voip_limit >= 100, "Critical apps must have a minimum guaranteed bandwidth"