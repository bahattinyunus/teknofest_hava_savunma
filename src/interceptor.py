import time
from typing import Dict, Any
from radar import Hedef

class SavunmaHatasi(Exception):
    """GökKalkan savunma sistemi için genel hata sınıfı."""
    pass

class MuhimmatYokHatasi(SavunmaHatasi):
    """Mühimmat tükendiğinde fırlatılan hata."""
    pass

class OnleyiciBatarya:
    def __init__(self, muhimmat: int = 10, hassasiyet_ayarlari: Dict[str, float] = None):
        self.muhimmat = muhimmat
        # Varsayılan hassasiyet ayarları
        self.hassasiyet = hassasiyet_ayarlari or {
            "yakin": 0.95,
            "orta": 0.80,
            "uzak": 0.50
        }

    def angaje_ol(self, hedef: Hedef) -> bool:
        """Belirli bir hedefe angaje olur. Mühimmat yoksa hata fırlatır."""
        if self.muhimmat <= 0:
            raise MuhimmatYokHatasi("KRİTİK: Mühimmat kalmadı, angajman başarısız!")
        
        # Mühimmat azalt
        self.muhimmat -= 1
        
        # Angajman simülasyonu
        # Mesafe ve hızın vuruş başarısına etkisi
        vurus_skoru = self.vurus_ihtimalini_hesapla(hedef)
        
        # Basit bir başarı kontrolü (Gerçek projede daha karmaşık algoritmalar olur)
        import random
        return random.random() < vurus_skoru

    def vurus_ihtimalini_hesapla(self, hedef: Hedef) -> float:
        """Mesafe ve irtifaya dayalı vuruş ihtimalini hesaplar."""
        d = hedef.mesafe
        
        if d < 10:
            return self.hassasiyet["yakin"]
        elif d < 60:
            return self.hassasiyet["orta"]
        else:
            return self.hassasiyet["uzak"]
