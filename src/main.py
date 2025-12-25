import time
import sys
import yaml
import os
from typing import Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from radar import RadarSistemi, Hedef
from interceptor import OnleyiciBatarya, MuhimmatYokHatasi
from telemetry import TelemetriSistemi
import utils

console = Console()

def ayarları_yukle(yol: str = "config/ayarlar.yaml") -> Dict[str, Any]:
    try:
        with open(yol, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

def create_status_table(target_data: list, battery_ammo: int) -> Table:
    table = Table(title="[bold blue]GÖKKALKAN YZ - CANLI TEMAS ÇİZELGESİ[/]", border_style="blue")
    
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Mesafe (km)", justify="right", style="magenta")
    table.add_column("İrtifa (km)", justify="right", style="green")
    table.add_column("Hız (km/h)", justify="right", style="yellow")
    table.add_column("TTI (sn)", justify="right", style="red")
    table.add_column("CPA (km)", justify="right", style="bold red")

    for t in target_data:
        table.add_row(
            t['id'],
            f"{t['mesafe']:.2f}",
            f"{t['irtifa']:.2f}",
            f"{t['hiz']:.1f}",
            f"{t['tti']:.1f}" if t['tti'] else "---",
            f"{t['cpa']:.2f}"
        )
    
    table.caption = f"[bold white]Mühimmat Durumu: {battery_ammo}[/]"
    return table

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

    # Başlangıç Ekranı
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]GÖKKALKAN YZ v2.5.0 - HAVA SAVUNMA KOMUTA MERKEZİ[/]\n"
        "[dim]Mimar: Bahattin Yunus Çetin | Sektör: Karadeniz/Trabzon[/]",
        border_style="bold blue"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Radar sistemleri senkronize ediliyor...", total=None)
        time.sleep(1)
        progress.add_task(description="Silah sistemleri kalibre ediliyor...", total=None)
        time.sleep(1)
        progress.add_task(description="Gök vatan veritabanı bağlandı.", total=None)
        time.sleep(0.5)

    telemetri.olay_kaydet("INFO", "Sistem tam kapasite ile başlatıldı.")
    
    active_ui_targets = []

    try:
        with Live(create_status_table([], batarya.muhimmat), refresh_per_second=1) as live:
            while True:
                radar.guncelle()
                yeni_temas = radar.tara()
                
                # Mevcut hedefleri UI için hazırla
                current_targets = []
                for h in radar.aktif_hedefler:
                    tti = utils.carpisma_suresi_hesapla(h)
                    cpa = utils.en_yakin_nokta_hesapla(h)
                    hiz = h.toplam_hiz
                    
                    data = {
                        "id": h.id,
                        "mesafe": h.mesafe,
                        "irtifa": h.z,
                        "hiz": hiz,
                        "tti": tti,
                        "cpa": cpa
                    }
                    current_targets.append(data)

                    # Otomatik Angajman Mantığı
                    kritik_cpa = ayarlar.get('tehdit_limitleri', {}).get('kritik_mesafe', 50.0)
                    if cpa < kritik_cpa and h.id not in [t.id for t in active_ui_targets]: # Sadece yeni kritikler için log at
                        telemetri.olay_kaydet("WARNING", f"KRİTİK TEHDİT: {h.id}", data)
                        
                        # Angajman görsel efekti (Konsolun üstüne yazar)
                        live.console.print(f"[bold red]>>> TEHDİT KİLİDİ: {h.id} <<<[/]")
                        try:
                            if batarya.angaje_ol(h):
                                live.console.print(f"[bold green][+] İMHA BAŞARILI: {h.id}[/]")
                                radar.aktif_hedefler.remove(h)
                            else:
                                live.console.print(f"[bold yellow][-] ISKALAMA: {h.id} takibi sürüyor![/]")
                        except MuhimmatYokHatasi as e:
                            live.console.print(f"[bold red][X] KRİTİK HATA: {e}[/]")

                live.update(create_status_table(current_targets, batarya.muhimmat))
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[bold red]SİSTEM KAPATILDI.[/] [white]Gök vatan size emanet.[/]")
        sys.exit(0)

if __name__ == "__main__":
    main()
