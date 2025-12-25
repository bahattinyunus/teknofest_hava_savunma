import time
import sys
from radar import RadarSistemi
from interceptor import OnleyiciBatarya

def main():
    print("="*50)
    print("GÖKKALKAN YZ - HAVA SAVUNMA KOMUTA MERKEZİ")
    print("Sistem Başlatma Dizisi Devrede...")
    print("="*50)
    time.sleep(1)

    radar = RadarSistemi(menzil_km=150)
    batarya = OnleyiciBatarya(muhimmat=20)

    print("\n[SİSTEM] Düşman Aktivitesi İzleniyor. İptal etmek için Ctrl+C'ye basın.\n")

    try:
        while True:
            # 1. Tarama Fazı
            hedef = radar.tara()
            
            if hedef:
                print(f"\n>>> ALARM: Temas Tespit Edildi! ID: {hedef['id']} | Azimut: {hedef['azimut']} | Tehdit: {hedef['tehdit_seviyesi']}")
                
                # 2. Değerlendirme Fazı
                if hedef['tehdit_seviyesi'] in ["YUKSEK", "KRITIK"]:
                    print(f"[SİSTEM] {hedef['id']} için ANGAJMAN YETKİSİ VERİLDİ")
                    if batarya.angaje_ol(hedef):
                        vurus_ihtimali = batarya.vurus_ihtimalini_hesapla(hedef)
                        print(f"[ONLEYICI] Vuruş İhtimali: %{vurus_ihtimali*100:.1f}")
                        print(f"[SİSTEM] HEDEF {hedef['id']} ETKİSİZ HALE GETİRİLDİ.")
                else:
                    print(f"[SİSTEM] Hedef {hedef['id']} izleniyor (Ölümcül Olmayan).")
            
            time.sleep(2) # Tarama aralığı

    except KeyboardInterrupt:
        print("\n[SİSTEM] Savunma ağı kapatılıyor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
