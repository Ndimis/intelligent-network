import numpy as np
import logging
from scipy.stats import ks_2samp

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ProtocolGuard")

class ProtocolAnomalyDetector:
    def __init__(self):
        # Baseline Profile: Normal HTTP traffic (Packet sizes in bytes)
        # Typically a mix of small headers and medium payloads
        self.http_baseline = [60, 1500, 400, 800, 60, 1200, 500, 60]

    def analyze_stream(self, packet_sizes):
        """
        Uses the Kolmogorov-Smirnov test to see if the current 
        stream matches the historical protocol profile.
        """
        if len(packet_sizes) < 5:
            return False # Not enough data for statistical significance
        
        # Calculate statistical "distance" between baseline and current stream
        statistic, p_value = ks_2samp(self.http_baseline, packet_sizes)
        
        # If p-value is low, the distributions are significantly different
        is_anomalous = p_value < 0.05
        
        if is_anomalous:
            logger.warning(f"🚨 PROTOCOL ANOMALY: Deviation detected! (p={round(p_value, 4)})")
            # Heuristic: Are packets too large? (Possible Tunneling)
            if np.mean(packet_sizes) > 1000:
                logger.warning("📝 Analysis: Suspiciously large packets. Possible Data Exfiltration.")
        else:
            logger.info("✅ Protocol behavior within normal parameters.")
            
        return is_anomalous

if __name__ == "__main__":
    detector = ProtocolAnomalyDetector()
    
    print("\n--- Testing Normal HTTP Stream ---")
    detector.analyze_stream([64, 1480, 500, 700, 60])
    
    print("\n--- Testing Anomalous Exfiltration (All Large Packets) ---")
    # All packets at maximum MTU (1500) suggests non-standard web traffic
    detector.analyze_stream([1500, 1500, 1500, 1500, 1500])