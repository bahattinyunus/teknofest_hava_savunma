import time

class OnleyiciBatarya:
    def __init__(self, muhimmat=10):
        self.muhimmat = muhimmat
        print(f"[ONLEYICI] Batarya Çevrimiçi. Hazır Füzeler: {self.muhimmat}")

    def angaje_ol(self, hedef):
        """Belirli bir hedefe angaje olur."""
        if self.muhimmat <= 0:
            print("[ONLEYICI] UYARI: MÜHİMMAT TÜKENDİ!")
            return False
        
        print(f"[ONLEYICI] HEDEF {hedef['id']} ÜZERİNE KİLİTLENİLİYOR...")
        time.sleep(1) # Simülasyon gecikmesi
        print(f"[ONLEYICI] FÜZE ATEŞLENDİ! (Hedef Mesafesi: {hedef['mesafe']:.2f}km)")
        self.muhimmat -= 1
        return True

    def vurus_ihtimalini_hesapla(self, hedef):
        """Mesafe ve hıza dayalı vuruş ihtimalini hesaplar."""
        # Basit mantık: yakın daha iyi, ancak çok yakın kötü
        if hedef['mesafe'] < 5:
            return 0.95
        elif hedef['mesafe'] < 50:
            return 0.80
        else:
            return 0.50
