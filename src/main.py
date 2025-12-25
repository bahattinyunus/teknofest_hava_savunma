import time
import sys
import yaml
import os
from typing import Dict, Any

from radar import RadarSistemi, Hedef
from interceptor import OnleyiciBatarya, MuhimmatYokHatasi
from telemetry import TelemetriSistemi

def ayarları_yukle(yol: str = "config/ayarlar.yaml") -> Dict[str, Any]:
    """YAML dosyasından sistem ayarlarını yükler."""
    try:
        with open(yol, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[UYARI] {yol} bulunamadı, varsayılan ayarlar kullanılacak.")
        return {}

def main():
    # 1. Altyapı Hazırlığı
    ayarlar = ayarları_yukle()
    telemetri = TelemetriSistemi(log_dosyasi="logs/gokkalkan_gorev.log")
    
    # 2. Sistem Bileşenlerini Başlat
    radar_ayar = ayarlar.get('radar', {})
    batarya_ayar = ayarlar.get('batarya', {})
    limit_ayar = ayarlar.get('tehdit_limitleri', {})

    radar = RadarSistemi(
        menzil_km=radar_ayar.get('menzil_km', 200),
        tespit_olasiligi=radar_ayar.get('tespit_olasiligi', 0.4)
    )
    
    batarya = OnleyiciBatarya(
        muhimmat=batarya_ayar.get('muhimmat', 15),
        hassasiyet_ayarlari=batarya_ayar.get('vurus_hassasiyeti')
    )

    print("\n" + "="*60)
    print("      GÖKKALKAN YZ - HAVA SAVUNMA KOMUTA MERKEZİ V2.0")
    print("      Durum: OPERASYONEL | Mod: OTONOM")
    print("="*60 + "\n")

    telemetri.olay_kaydet("INFO", "Sistem tam kapasite ile başlatıldı.")

    try:
        while True:
            # A.Radar Taraması
            radar.guncelle()
            yeni_temas = radar.tara()
            
            if yeni_temas:
                # Veri Kaydı
                veri = {
                    "id": yeni_temas.id,
                    "mesafe": round(yeni_temas.mesafe, 2),
                    "irtifa": round(yeni_temas.z, 2),
                    "hiz": round(yeni_temas.toplam_hiz, 1)
                }
                telemetri.olay_kaydet("WARNING", f"Yeni temas tespit edildi: {yeni_temas.id}", veri)
                
                print(f"[RADAR] TEMAS! {yeni_temas.id} | Mesafe: {veri['mesafe']}km | İrtifa: {veri['irtifa']}km | Hız: {veri['hiz']}km/s")

                # B.Tehdit Analizi
                kritik_hiz = limit_ayar.get('kritik_hiz', 1000.0)
                if veri['hiz'] > kritik_hiz or veri['mesafe'] < limit_ayar.get('kritik_mesafe', 50.0):
                    print(f"[ANALİZ] TEHDİT KRİTİK! {yeni_temas.id} için angajman başlatılıyor...")
                    
                    # C.Angajman
                    try:
                        basarili = batarya.angaje_ol(yeni_temas)
                        if basarili:
                            telemetri.olay_kaydet("INFO", f"Hedef imha edildi: {yeni_temas.id}", {"muhimmat_kalan": batarya.muhimmat})
                            print(f"[SİSTEM] HEDEF {yeni_temas.id} İMHA EDİLDİ. (Kalan Mühimmat: {batarya.muhimmat})")
                        else:
                            telemetri.olay_kaydet("ERROR", f"Angajman başarısız: {yeni_temas.id}")
                            print(f"[SİSTEM] !!! DİKKAT: {yeni_temas.id} İÇİN ISKALAMA GERÇEKLEŞTİ!")
                    
                    except MuhimmatYokHatasi as e:
                        telemetri.olay_kaydet("CRITICAL", str(e))
                        print(f"[HATA] {e}")

            time.sleep(2)

    except KeyboardInterrupt:
        telemetri.olay_kaydet("INFO", "Sistem kullanıcı tarafından kapatıldı.")
        print("\n[Veda] GökKalkan YZ Güvenli Modda Kapatılıyor. İyi nöbetler!")
        sys.exit(0)

if __name__ == "__main__":
    main()
