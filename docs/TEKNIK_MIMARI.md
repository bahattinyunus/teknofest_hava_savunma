# 📐 GökKalkan YZ - Teknik Mimari Dokümanı

## 1. Sisteme Genel Bakış

GökKalkan YZ, katmanlı bir hava savunma simülasyonudur. Sistem, tehditleri tespit etmekten (Sense), analiz etmeye (Decide) ve engellemeye (Act) kadar olan OODA (Observe-Orient-Decide-Act) döngüsünü otonom olarak gerçekleştirir.

## 2. Algoritmik Mantık

### 2.1. Algılama Modülü (Radar)
Rastgele olasılık dağılımı kullanılarak radar kesit alanı (RCS) simülasyonu yapılır.
- **Menzil Denklemi:** $R_{max} = \sqrt[4]{\frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 P_{min}}}$
  *(Not: Simülasyonda bu denklem basitleştirilmiş lineer mesafe kontrolü olarak uygulanmıştır.)*
- **Taramalar:** Sistem saniyede 0.5Hz frekans ile tarama yapar.

### 2.2. Tehdit Değerlendirme
Algılanan her cisim bir "Tehdit Matriksi"ne tabi tutulur:
- **KRITIK:** Mesafe < 50km VE Hız > 1000km/s (Balistik Füze Profili)
- **YUKSEK:** Mesafe < 80km (Taarruz Uçağı Profili)
- **ORTA/DUSUK:** Sivil uçak veya iha profili.

### 2.3. Engelleme (Interceptor)
Füze vuruş ihtimali ($P_k$), hedefin o anki konumu ve kaçınma manevrası kapasitesine ters orantılı olarak hesaplanır.

$$P_k = \begin{cases} 
0.95 & \text{if } d < 5km \\
0.80 & \text{if } 5km \le d < 50km \\
0.50 & \text{otherwise}
\end{cases}$$

## 3. Yazılım Mimarisi

```mermaid
graph TD
    A[Ana Döngü (Main)] -->|Veri İsteği| B(Radar Sistemi)
    B -->|Hedef Listesi| A
    A -->|Tehdit Analizi| C{Tehdit Seviyesi?}
    C -->|Kritik/Yüksek| D[Engelleme Bataryası]
    D -->|Ateşleme| E[Hedef İmha]
    C -->|Düşük| F[Loglama]
```

## 4. Gelecek Geliştirmeler
- **Sensor Fusion:** Optik ve Termal kamera verilerinin entegrasyonu.
- **Swarm Defense:** Sürü drone saldırılarına karşı karşı-sürü algoritmaları.
