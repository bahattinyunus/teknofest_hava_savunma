import math
from typing import Optional
from radar import Hedef

def carpisma_suresi_hesapla(hedef: Hedef) -> Optional[float]:
    """
    Hedefin mevcut hiz vektoru ile radara (0,0,0) ne kadar surede ulasacagini hesaplar (TTI).
    Eger hedef uzaklasiyorsa None doner.
    """
    # Nokta urunu (P . V) / |V|^2 
    # Pozisyon vektoru P = (x, y, z)
    # Hiz vektoru V = (vx, vy, vz)
    
    pay = (hedef.x * hedef.vx) + (hedef.y * hedef.vy) + (hedef.z * hedef.vz)
    hiz_kare = (hedef.vx**2 + hedef.vy**2 + hedef.vz**2)
    
    if hiz_kare == 0: return None
    
    # pay < 0 ise hedef yaklasiyordur
    if pay >= 0: return None
    
    tti = -pay / hiz_kare
    return tti

def en_yakin_nokta_hesapla(hedef: Hedef) -> float:
    """
    Hedefin rotasi uzerindeki en yakin gecis mesafesini (CPA) hesaplar.
    """
    # CPA mesafesi: |P x V| / |V|
    # Cross product P x V
    cx = (hedef.y * hedef.vz) - (hedef.z * hedef.vy)
    cy = (hedef.z * hedef.vx) - (hedef.x * hedef.vz)
    cz = (hedef.x * hedef.vy) - (hedef.y * hedef.vx)
    
    cp_mag = math.sqrt(cx**2 + cy**2 + cz**2)
    hiz_mag = math.sqrt(hedef.vx**2 + hedef.vy**2 + hedef.vz**2)
    
    if hiz_mag == 0: return hedef.mesafe
    
    return cp_mag / hiz_mag
