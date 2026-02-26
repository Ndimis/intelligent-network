import math
import logging
import sys
from collections import Counter

# Windows Unicode Fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("DNS-Guard")

class DNSTunnelDetector:
    def __init__(self, entropy_threshold=4.0, length_limit=20):
        self.entropy_threshold = entropy_threshold
        self.length_limit = length_limit

    def calculate_entropy(self, text):
        """Calculates Shannon Entropy (Randomness)."""
        if not text: return 0.0
        probs = [f / len(text) for f in Counter(text).values()]
        return round(-sum(p * math.log2(p) for p in probs), 4)


    def evaluate(self, domain):
        subdomain = domain.split('.')[0]
        entropy = self.calculate_entropy(subdomain)
        length = len(subdomain)
        
        # 1. Pure Math Threat: Very high randomness (Standard Base64)
        is_high_entropy = entropy > 3.9 
        
        # 2. Stealth Threat: Moderate randomness + Moderate length
        # This will catch 'a1b2c3d4e5f6' (Len 12, Ent 3.5)
        is_stealth_hex = length >= 12 and entropy > 3.4
        
        # 3. Dictionary Evasion: Long string with many hyphens/chars
        # This will catch 'p-a-s-s-w-o-r-d-l-e-a-k' (Len 19, Ent 2.6)
        is_long_leak = length >= 18 and entropy > 2.5

        if is_high_entropy or is_stealth_hex or is_long_leak:
            logger.warning(f"🚨 THREAT DETECTED: {domain} | Entropy: {entropy} | Len: {length}")
            return True
        else:
            logger.info(f"✅ Safe: {domain} | Entropy: {entropy} | Len: {length}")
            return False

if __name__ == "__main__":
    detector = DNSTunnelDetector()
    
    # Comprehensive Test Suite
    test_cases = [
        "google.com",                       # Normal
        "aws.amazon.com",                   # Normal
        "SGVsbG8tU2VjcmV0LU1lc3NhZ2U=.io",  # Detected: High Entropy + Long
        "a1b2c3d4e5f6.C2-server.ru",        # Detected: Unusual Length + Moderate Entropy
        "admin.com",                        # Safe: Short/Linguistic
        "x1y2.ws",                          # Safe: Too short to be meaningful exfil
        "p-a-s-s-w-o-r-d-l-e-a-k.net"       # Detected: High Diversity/Length even with low entropy words
    ]

    print("\n--- DNS TRAFFIC ANALYSIS ---")
    for domain in test_cases:
        detector.evaluate(domain)