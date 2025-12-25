import time

class InterceptorBattery:
    def __init__(self, ammo=10):
        self.ammo = ammo
        print(f"[INTERCEPTOR] Battery Online. Missiles ready: {self.ammo}")

    def engage(self, target):
        """Engages a specific target."""
        if self.ammo <= 0:
            print("[INTERCEPTOR] WARNING: DEPLETED AMMUNITION!")
            return False
        
        print(f"[INTERCEPTOR] LOCKING ON TARGET {target['id']}...")
        time.sleep(1) # Simulation delay
        print(f"[INTERCEPTOR] FIRING MISSILE! (Target Dist: {target['distance']:.2f}km)")
        self.ammo -= 1
        return True

    def calculate_hit_probability(self, target):
        """Calculates hit probability based on distance and speed."""
        # Simple dummy logic: closer is better, but too close is bad
        if target['distance'] < 5:
            return 0.95
        elif target['distance'] < 50:
            return 0.80
        else:
            return 0.50
