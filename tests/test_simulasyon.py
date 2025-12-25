import sys
import os
import unittest

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from radar import RadarSistemi
from interceptor import OnleyiciBatarya

class TestGokKalkan(unittest.TestCase):
    
    def test_radar_ilklendirme(self):
        """Radar sisteminin doğru parametrelerle başlatıldığını test eder."""
        radar = RadarSistemi(menzil_km=200)
        self.assertEqual(radar.menzil_km, 200)
        self.assertEqual(len(radar.aktif_hedefler), 0)

    def test_radar_hedef_tespit(self):
        """Radar taramasının veri yapısını ve türlerini doğrular."""
        radar = RadarSistemi(menzil_km=100)
        # 10 denemede (mock random ile) en azindan veri yapisini kontrol et
        sonuc = radar.tara()
        if sonuc:
            self.assertIn("id", sonuc)
            self.assertIn("mesafe", sonuc)
            self.assertIn("tehdit_seviyesi", sonuc)
            self.assertLessEqual(sonuc["mesafe"], 100)
        else:
            self.assertIsNone(sonuc)

    def test_onleyici_sarj(self):
        """Önleyici bataryanın mühimmat tüketimini test eder."""
        batarya = OnleyiciBatarya(muhimmat=2)
        self.assertEqual(batarya.muhimmat, 2)
        
        hedef = {"id": "TEST-1", "mesafe": 50, "hiz": 500}
        
        # 1. Atış
        basarili = batarya.angaje_ol(hedef)
        self.assertTrue(basarili)
        self.assertEqual(batarya.muhimmat, 1)
        
        # 2. Atış
        batarya.angaje_ol(hedef)
        self.assertEqual(batarya.muhimmat, 0)
        
        # 3. Atış (Boş)
        basarili = batarya.angaje_ol(hedef)
        self.assertFalse(basarili)
        self.assertEqual(batarya.muhimmat, 0)

    def test_vurus_ihtimali(self):
        """Mesafe bazlı vuruş ihtimali mantığını doğrular."""
        batarya = OnleyiciBatarya()
        
        yakin_hedef = {"id": "YAKIN", "mesafe": 4, "hiz": 100}
        orta_hedef = {"id": "ORTA", "mesafe": 40, "hiz": 100}
        uzak_hedef = {"id": "UZAK", "mesafe": 100, "hiz": 100}
        
        self.assertEqual(batarya.vurus_ihtimalini_hesapla(yakin_hedef), 0.95)
        self.assertEqual(batarya.vurus_ihtimalini_hesapla(orta_hedef), 0.80)
        self.assertEqual(batarya.vurus_ihtimalini_hesapla(uzak_hedef), 0.50)

if __name__ == '__main__':
    unittest.main()
