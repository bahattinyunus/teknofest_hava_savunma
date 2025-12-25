import time
import sys
import yaml
import os
from typing import Dict, Any

from radar import RadarSistemi, Hedef
from interceptor import OnleyiciBatarya, MuhimmatYokHatasi
from telemetry import TelemetriSistemi
import utils

def efektli_yaz(metin: str, gecikme: float = 0.01):
    """Metni daktilo efektiyle ekrana basar."""
    for karakter in metin:
        sys.stdout.write(karakter)
        sys.stdout.flush()
        time.sleep(gecikme)
    print()

def ayarları_yukle(yol: str = "config/ayarlar.yaml") -> Dict[str, Any]:
    try:
        with open(yol, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

def main():
    ayarlar = ayarları_yukle()
    telemetri = TelemetriSistemi(log_dosyasi="logs/gokkalkan_gorev.log")
    
    radar = RadarSistemi(
        menzil_km=ayarlar.get('radar', {}).get('menzil_km', 200),
        tespit_olasiligi=ayarlar.get('radar', {}).get('tespit_olasiligi', 0.4)
    )
    
    batarya = OnleyiciBatarya(
        muhimmat=ayarlar.get('batarya', {}).get('muhimmat', 15),
        hassasiyet_ayarlari=ayarlar.get('batarya', {}).get('vurus_hassasiyeti')
    )

    os.system('cls' if os.name == 'nt' else 'clear')
    efektli_yaz(">>> GÖKKALKAN YZ SİSTEMLERİ BAŞLATILIYOR...", 0.03)
    time.sleep(0.5)
    efektli_yaz(">>> RADAR KATMANI: AKTİF", 0.02)
    efektli_yaz(">>> SİLAH KONTROL ARABİRİMİ: ÇEVRİMİÇİ", 0.02)
    efektli_yaz(">>> YEREL GÜVENLİK PROTOKOLLERİ YÜKLENDİ.", 0.02)
    time.sleep(0.5)
    
    print("\n" + "█"*60)
    print("      SKYSHIELD AI - BEYİN VE KOMUTA MERKEZİ V2.5")
    print("      OPERATÖR: BAHATTİN YUNUS ÇETİN | LOKASYON: TRABZON")
    print("█"*60 + "\n")

    try:
        while True:
            radar.guncelle()
            yeni_temas = radar.tara()
            
            if yeni_temas:
                tti = utils.carpisma_suresi_hesapla(yeni_temas)
                cpa = utils.en_yakin_nokta_hesapla(yeni_temas)
                total_hiz = yeni_temas.toplam_hiz

                print(f"\n[!] TEMAS TESPİT EDİLDİ: {yeni_temas.id}")
                print(f"    ├─ Mesafe: {yeni_temas.mesafe:.2f} km")
                print(f"    ├─ İrtifa: {yeni_temas.z:.2f} km")
                print(f"    ├─ Hız: {total_hiz:.1f} km/h")
                if tti:
                    print(f"    ├─ Çarpışma Süresi (TTI): {tti:.1f} sn")
                print(f"    └─ En Yakın Geçiş (CPA): {cpa:.2f} km")

                # Karar verme süreci
                kritik_cpa = ayarlar.get('tehdit_limitleri', {}).get('kritik_mesafe', 50.0)
                if cpa < kritik_cpa:
                    efektli_yaz(f"    [!] KRİTİK TEHDİT ANALİZİ: {yeni_temas.id} angajman sahasında!", 0.01)
                    
                    try:
                        time.sleep(1) # Karar alma süresi
                        if batarya.angaje_ol(yeni_temas):
                            print(f"    [+] BAŞARILI: {yeni_temas.id} bölgeden temizlendi.")
                        else:
                            print(f"    [-] ISKALAMA: {yeni_temas.id} takibi devam ediyor.")
                    except MuhimmatYokHatasi as e:
                        print(f"    [X] KRİTİK HATA: {e}")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n>>> SISTEM KAPATILIYOR. Gök vatan size emanet.")
        sys.exit(0)

if __name__ == "__main__":
    main()
