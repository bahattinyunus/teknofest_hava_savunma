import random
import time
import math

class RadarSystem:
    def __init__(self, range_km=100.0):
        self.range_km = range_km
        self.active_targets = []
        print(f"[RADAR] System Initialized. Range: {self.range_km}km")

    def scan(self):
        """Simulates a radar scan sweep."""
        print("[RADAR] Scanning airspace...")
        # Simulate finding a target with 30% probability
        if random.random() < 0.3:
            target = {
                "id": f"TGT-{random.randint(1000, 9999)}",
                "azimuth": random.randint(0, 360),
                "distance": random.uniform(10.0, self.range_km),
                "speed": random.uniform(200.0, 2000.0), # km/h
                "threat_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
            }
            self.active_targets.append(target)
            return target
        return None

    def track_targets(self):
        """Updates positions of tracked targets."""
        for target in self.active_targets:
            # Simulate target moving closer
            approach_speed_kmps = target['speed'] / 3600.0
            target['distance'] -= approach_speed_kmps
            if target['distance'] < 0:
                target['distance'] = 0
        
        # Remove targets that have been neutralized or landed (logic handled elsewhere usually)
        return self.active_targets
