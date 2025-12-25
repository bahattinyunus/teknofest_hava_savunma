import logging
import os
import json
from datetime import datetime
from typing import Any, Dict

class TelemetriSistemi:
    def __init__(self, log_dosyasi: str = "logs/sistem.log"):
        os.makedirs(os.path.dirname(log_dosyasi), exist_ok=True)
        
        # Standart Python logger yapılandırması
        self.logger = logging.getLogger("GokKalkan")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_dosyasi, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        print(f"[SİSTEM] Telemetri Aktif: {log_dosyasi}")

    def olay_kaydet(self, seviye: str, mesaj: str, veri: Dict[str, Any] = None):
        """Bir olayı hem log dosyasına hem de yapılandırılmış olarak kaydeder."""
        log_mesajı = mesaj
        if veri:
            log_mesajı += f" | VERİ: {json.dumps(veri, ensure_ascii=False)}"
            
        if seviye.upper() == "INFO":
            self.logger.info(log_mesajı)
        elif seviye.upper() == "WARNING":
            self.logger.warning(log_mesajı)
        elif seviye.upper() == "ERROR":
            self.logger.error(log_mesajı)
        elif seviye.upper() == "CRITICAL":
            self.logger.critical(log_mesajı)
