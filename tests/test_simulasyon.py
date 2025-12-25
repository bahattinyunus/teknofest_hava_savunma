import sys
import os
import unittest
import math

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from radar import RadarSistemi, Hedef
from interceptor import OnleyiciBatarya, MuhimmatYokHatasi

class TestGokKalkanV2(unittest.TestCase):
    
    def test_hedef_matematigi(self):
        """Hedef sınıfının mesafe ve hız hesaplamalarını doğrular."""
        # 3-4-5 üçgeni + irtifa
        h = Hedef("TEST", x=3, y=4, z=0, vx=0, vy=0, vz=0)
        self.assertEqual(h.mesafe, 5.0)
        
        # Hız hesaplama (1 km/s = 3600 km/h)
        h.vx = 1.0
        self.assertEqual(h.toplam_hiz, 3600.0)

    def test_radar_3b_tespit(self):
        """Radarın 3B uzayda hedef üretme mantığını test eder."""
        radar = RadarSistemi(menzil_km=100)
        # 20 denemede olasılıkla bir hedef yakalamaya çalış
        tespit = None
        for _ in range(20):
            tespit = radar.tara()
            if tespit: break
            
        if tespit:
            self.assertIsInstance(tespit, Hedef)
            self.assertLessEqual(tespit.mesafe, 100 * 1.1)
            self.assertTrue(0 <= tespit.z <= 15) # İrtifa kontrolü

    def test_gelismis_onleyici_ve_istisna(self):
        """Mühimmat tükenme hatasını (Exception) test eder."""
        batarya = OnleyiciBatarya(muhimmat=1)
        hedef = Hedef("H1", 10, 10, 5, 0, 0, 0)
        
        # İlk atış
        batarya.angaje_ol(hedef)
        self.assertEqual(batarya.muhimmat, 0)
        
        # İkinci atışta hata fırlatmalı
        with self.assertRaises(MuhimmatYokHatasi):
            batarya.angaje_ol(hedef)

    def test_vurus_ihtimali_katmanlari(self):
        """Yeni vuruş hassasiyeti katmanlarını doğrular."""
        ayarlar = {"yakin": 0.99, "orta": 0.50, "uzak": 0.10}
        batarya = OnleyiciBatarya(hassasiyet_ayarlari=ayarlar)
        
        h_yakin = Hedef("Y", 2, 2, 1, 0, 0, 0) # mesafe ~3
        h_orta = Hedef("O", 30, 30, 2, 0, 0, 0) # mesafe ~42
        
        self.assertEqual(batarya.vurus_ihtimalini_hesapla(h_yakin), 0.99)
        self.assertEqual(batarya.vurus_ihtimalini_hesapla(h_orta), 0.50)

    def test_ballistic_utils(self):
        """TTI ve CPA matematiksel fonksiyonlarını doğrular."""
        import utils
        # Merkeze (0,0,0) dogru tam 1 km/s hizla gelen hedef
        # Mesafe 10km, Hiz 1km/s -> TTI 10sn olmali
        h = Hedef("B1", 10, 0, 0, -1, 0, 0)
        self.assertEqual(utils.carpisma_suresi_hesapla(h), 10.0)
        # CPA degeri 0 olmali (ustune geliyor)
        self.assertEqual(utils.en_yakin_nokta_hesapla(h), 0.0)
        
        # Yanindan gecen hedef
        # P = (10, 10, 0), V = (-1, 0, 0) -> CPA 10 olmali
        h_side = Hedef("B2", 10, 10, 0, -1, 0, 0)
        self.assertEqual(utils.en_yakin_nokta_hesapla(h_side), 10.0)

if __name__ == '__main__':
    unittest.main()
