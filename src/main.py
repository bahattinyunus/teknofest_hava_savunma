import time
import sys
from radar import RadarSystem
from interceptor import InterceptorBattery

def main():
    print("="*50)
    print("SKYSHIELD AI - AIR DEFENSE COMMAND CENTER")
    print("System Startup Sequence Initiated...")
    print("="*50)
    time.sleep(1)

    radar = RadarSystem(range_km=150)
    battery = InterceptorBattery(ammo=20)

    print("\n[SYSTEM] Monitoring Hostile Activity. Press Ctrl+C to abort.\n")

    try:
        while True:
            # 1. Scan Phase
            target = radar.scan()
            
            if target:
                print(f"\n>>> ALERT: Contact Detected! ID: {target['id']} | Azimuth: {target['azimuth']} | Threat: {target['threat_level']}")
                
                # 2. Assessment Phase
                if target['threat_level'] in ["HIGH", "CRITICAL"]:
                    print(f"[SYSTEM] ENGAGEMENT AUTHORITY GRANTED for {target['id']}")
                    if battery.engage(target):
                        hit_prob = battery.calculate_hit_probability(target)
                        print(f"[INTERCEPTOR] Impact Probability: {hit_prob*100:.1f}%")
                        print(f"[SYSTEM] TARGET {target['id']} NEUTRALIZED.")
                else:
                    print(f"[SYSTEM] Monitoring target {target['id']} (Non-Lethal).")
            
            time.sleep(2) # Scan interval

    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down defense grid...")
        sys.exit(0)

if __name__ == "__main__":
    main()
