import random
import time
import math

class RadarSistemi:
    def __init__(self, menzil_km=100.0):
        self.menzil_km = menzil_km
        self.aktif_hedefler = []
        print(f"[RADAR] Sistem Başlatıldı. Menzil: {self.menzil_km}km")

    def tara(self):
        """Radar tarama döngüsünü simüle eder."""
        print("[RADAR] Hava sahası taranıyor...")
        # %30 ihtimalle hedef bulma simülasyonu
        if random.random() < 0.3:
            hedef = {
                "id": f"HDF-{random.randint(1000, 9999)}",
                "azimut": random.randint(0, 360),
                "mesafe": random.uniform(10.0, self.menzil_km),
                "hiz": random.uniform(200.0, 2000.0), # km/s
                "tehdit_seviyesi": random.choice(["DUSUK", "ORTA", "YUKSEK", "KRITIK"])
            }
            self.aktif_hedefler.append(hedef)
            return hedef
        return None

    def hedefleri_takip_et(self):
        """Takip edilen hedeflerin konumlarını günceller."""
        for hedef in self.aktif_hedefler:
            # Hedefin yaklaşmasını simüle et
            yaklasma_hizi_kmps = hedef['hiz'] / 3600.0
            hedef['mesafe'] -= yaklasma_hizi_kmps
            if hedef['mesafe'] < 0:
                hedef['mesafe'] = 0
        
        # Etkisiz hale getirilen veya inen hedefleri temizle (mantık genellikle başka yerde işlenir)
        return self.aktif_hedefler
