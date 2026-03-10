import numpy as np
from sklearn.ensemble import RandomForestRegressor

class TrafficShaper:
    def __init__(self):
        # Model to predict the "Optimal Bandwidth Limit" for a flow
        # Features: [Current Latency, Packet Loss, Time of Day, Flow Duration]
        self.model = RandomForestRegressor(n_estimators=10)
        self._pretrain_dummy_data()

    def _pretrain_dummy_data(self):
        # Simulating training: Higher latency/loss -> Lower recommended bandwidth
        X = np.array([[20, 0, 10, 5], [150, 5, 14, 60], [300, 10, 16, 120]])
        y = np.array([1000, 50, 10]) # Recommended Mbps
        self.model.fit(X, y)

    def calculate_priority(self, app_type):
        priorities = {"VOIP": 1, "SSH": 1, "VIDEO": 2, "BULK_DATA": 3}
        return priorities.get(app_type, 3)

    def get_shaping_decision(self, metrics, app_type):
        """
        Predicts the allowed bandwidth (Mbps) for a specific application.
        """
        predicted_max = self.model.predict([metrics])[0]
        
        # Apply logic: Critical apps (Priority 1) get at least 80% of prediction
        # Bulk apps (Priority 3) can be throttled down to 10% if needed
        priority = self.calculate_priority(app_type)
        if priority == 1:
            return max(predicted_max, 100) # Minimum 100Mbps for critical
        return predicted_max * (0.5 if priority == 2 else 0.1)

if __name__ == "__main__":
    shaper = TrafficShaper()
    # Scenario: High latency (200ms) and 2% packet loss during peak hour
    current_metrics = [200, 2, 15, 30] 
    
    for app in ["VOIP", "VIDEO", "BULK_DATA"]:
        limit = shaper.get_shaping_decision(current_metrics, app)
        print(f"AI Decision for {app}: Limit to {limit:.2f} Mbps")