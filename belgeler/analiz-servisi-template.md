# Analiz Servisi - Analytics & Monitoring Service

## 🎯 Özellikler

- Kullanıcı davranış analizi
- Sistem performans metrikleri
- Konuşma analitikleri
- Gerçek zamanlı dashboard
- Raporlama sistemi
- A/B test desteği
- Anomali tespiti

## 📁 Dizin Yapısı
# Ana dizine git
mkdir -p servisler/analiz/app/modeller
mkdir -p servisler/analiz/app/schemas
mkdir -p servisler/analiz/app/api/v1
mkdir -p servisler/analiz/app/core
mkdir -p servisler/analiz/app/servisler
mkdir -p servisler/analiz/tests

# Dosyaları oluştur
touch servisler/analiz/app/__init__.py
touch servisler/analiz/app/analiz.py
touch servisler/analiz/app/ayar.py
touch servisler/analiz/app/veritabani.py
touch servisler/analiz/app/modeller/__init__.py
touch servisler/analiz/app/modeller/olay.py
touch servisler/analiz/app/modeller/metrik.py
touch servisler/analiz/app/modeller/rapor.py
touch servisler/analiz/app/schemas/__init__.py
touch servisler/analiz/app/schemas/analiz.py
touch servisler/analiz/app/schemas/metrik.py
touch servisler/analiz/app/api/__init__.py
touch servisler/analiz/app/api/v1/__init__.py
touch servisler/analiz/app/api/v1/olay.py
touch servisler/analiz/app/api/v1/metrik.py
touch servisler/analiz/app/api/v1/rapor.py
touch servisler/analiz/app/api/v1/dashboard.py
touch servisler/analiz/app/core/__init__.py
touch servisler/analiz/app/core/analiz_motoru.py
touch servisler/analiz/app/core/metrik_toplayici.py
touch servisler/analiz/app/core/anomali_tespit.py
touch servisler/analiz/app/servisler/__init__.py
touch servisler/analiz/app/servisler/olay_hizmeti.py
touch servisler/analiz/app/servisler/metrik_hizmeti.py
touch servisler/analiz/app/servisler/rapor_hizmeti.py
touch servisler/analiz/app/servisler/dashboard_hizmeti.py
touch servisler/analiz/tests/__init__.py
touch servisler/analiz/Dockerfile
touch servisler/analiz/pyproject.toml
touch servisler/analiz/README.md
```
servisler/analiz/
├── app/
│   ├── __init__.py
│   ├── analiz.py              # FastAPI app
│   ├── ayar.py              # Configuration
│   ├── veritabani.py        # Database connections
│   ├── modeller/
│   │   ├── __init__.py
│   │   ├── olay.py          # Event model
│   │   ├── metrik.py        # Metric model
│   │   └── rapor.py         # Report model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analiz.py        # Analytics schemas
│   │   └── metrik.py        # Metrics schemas
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── olay.py      # Event endpoints
│   │       ├── metrik.py    # Metrics endpoints
│   │       ├── rapor.py     # Report endpoints
│   │       └── dashboard.py # Dashboard endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── analiz_motoru.py # Analytics engine
│   │   ├── metrik_toplayici.py # Metrics collector
│   │   └── anomali_tespit.py # Anomaly detection
│   └── servisler/
│       ├── __init__.py
│       ├── olay_hizmeti.py
│       ├── metrik_hizmeti.py
│       ├── rapor_hizmeti.py
│       └── dashboard_hizmeti.py
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 🔧 Temel Dosyalar

### pyproject.toml
```toml
[tool.poetry]
name = "eyay-analiz-servisi"
version = "0.1.0"
description = "EyAy.OS Analiz ve İzleme Mikroservisi"
authors = ["Barut Şeref <barutseref@barutben.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sqlalchemy = "^2.0.0"
alembic = "^1.12.0"
psycopg2-binary = "^2.9.0"
redis = "^5.0.0"
pandas = "^2.1.0"
numpy = "^1.24.0"
plotly = "^5.17.0"
prometheus-client = "^0.19.0"
influxdb-client = "^1.38.0"
scikit-learn = "^1.3.0"
pydantic = "^2.4.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.25.0"
jupyter = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### app/cekirdek/analiz_motoru.py
```python
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import redis
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from sqlalchemy.orm import Session

from app.modeller.olay import Olay
from app.modeller.metrik import Metrik
from app.veritabani import get_db

logger = logging.getLogger(__name__)

class AnalizMotoru:
    """Ana analiz ve izleme motoru"""
    
    def __init__(self, ayarlar: Dict[str, Any]):
        self.ayarlar = ayarlar
        self.redis_client = None
        self.influxdb_client = None
        self.write_api = None
        self.anomali_modeli = IsolationForest(contamination=0.1)
        self.scaler = StandardScaler()
        self._baglanti_kur()
    
    def _baglanti_kur(self):
        """Veritabanı bağlantılarını kur"""
        try:
            # Redis bağlantısı
            self.redis_client = redis.Redis(
                host=self.ayarlar.get('redis_host', 'localhost'),
                port=self.ayarlar.get('redis_port', 6379),
                db=self.ayarlar.get('redis_db', 2),
                decode_responses=True
            )
            
            # InfluxDB bağlantısı (zaman serisi verileri için)
            if self.ayarlar.get('influxdb_enabled', False):
                self.influxdb_client = InfluxDBClient(
                    url=self.ayarlar.get('influxdb_url', 'http://localhost:8086'),
                    token=self.ayarlar.get('influxdb_token'),
                    org=self.ayarlar.get('influxdb_org', 'eyay')
                )
                self.write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
            
            logger.info("✅ Analiz motoru bağlantıları kuruldu")
            
        except Exception as e:
            logger.error(f"❌ Analiz motoru bağlantı hatası: {e}")
            raise
    
    async def olay_kaydet(
        self,
        kullanici_id: Optional[int],
        olay_tipi: str,
        olay_verisi: Dict[str, Any],
        kaynak: str = "sistem"
    ) -> Dict[str, Any]:
        """Analiz olayı kaydet"""
        try:
            olay = {
                "id": f"{olay_tipi}_{datetime.now().timestamp()}",
                "kullanici_id": kullanici_id,
                "olay_tipi": olay_tipi,
                "olay_verisi": olay_verisi,
                "kaynak": kaynak,
                "zaman": datetime.now().isoformat(),
                "ip_adresi": olay_verisi.get("ip_adresi"),
                "user_agent": olay_verisi.get("user_agent")
            }
            
            # PostgreSQL'e kaydet
            await self._olay_veritabani_kaydet(olay)
            
            # Redis'e hızlı erişim için kaydet
            await self._olay_redis_kaydet(olay)
            
            # InfluxDB'ye zaman serisi verisi olarak kaydet
            if self.influxdb_client:
                await self._olay_influxdb_kaydet(olay)
            
            # Gerçek zamanlı metrik güncelle
            await self._gercek_zamanli_metrik_guncelle(olay_tipi, kullanici_id)
            
            logger.debug(f"Olay kaydedildi: {olay_tipi}")
            
            return {
                "durum": "basarili",
                "olay_id": olay["id"]
            }
            
        except Exception as e:
            logger.error(f"Olay kaydetme hatası: {e}")
            return {"durum": "hata", "mesaj": str(e)}
    
    async def _olay_veritabani_kaydet(self, olay: Dict[str, Any]):
        """Olayı PostgreSQL'e kaydet"""
        try:
            db = next(get_db())
            
            db_olay = Olay(
                id=olay["id"],
                kullanici_id=olay["kullanici_id"],
                olay_tipi=olay["olay_tipi"],
                olay_verisi=json.dumps(olay["olay_verisi"]),
                kaynak=olay["kaynak"],
                olusturulma_tarihi=datetime.fromisoformat(olay["zaman"]),
                ip_adresi=olay.get("ip_adresi"),
                user_agent=olay.get("user_agent")
            )
            
            db.add(db_olay)
            db.commit()
            
        except Exception as e:
            logger.error(f"Olay veritabanı kaydetme hatası: {e}")
    
    async def _olay_redis_kaydet(self, olay: Dict[str, Any]):
        """Olayı Redis'e kaydet"""
        try:
            # Son olaylar listesi (son 1000 olay)
            self.redis_client.lpush("son_olaylar", json.dumps(olay))
            self.redis_client.ltrim("son_olaylar", 0, 999)
            
            # Olay tipine göre sayaç
            self.redis_client.incr(f"olay_sayaci:{olay['olay_tipi']}")
            
            # Kullanıcı bazlı sayaç
            if olay["kullanici_id"]:
                self.redis_client.incr(f"kullanici_olay:{olay['kullanici_id']}")
            
        except Exception as e:
            logger.error(f"Olay Redis kaydetme hatası: {e}")
    
    async def _olay_influxdb_kaydet(self, olay: Dict[str, Any]):
        """Olayı InfluxDB'ye kaydet"""
        try:
            point = Point("olay") \
                .tag("olay_tipi", olay["olay_tipi"]) \
                .tag("kaynak", olay["kaynak"]) \
                .field("kullanici_id", olay["kullanici_id"] or 0) \
                .field("olay_verisi", json.dumps(olay["olay_verisi"])) \
                .time(datetime.fromisoformat(olay["zaman"]))
            
            if olay["kullanici_id"]:
                point = point.tag("kullanici_id", str(olay["kullanici_id"]))
            
            self.write_api.write(
                bucket=self.ayarlar.get('influxdb_bucket', 'eyay'),
                record=point
            )
            
        except Exception as e:
            logger.error(f"InfluxDB kaydetme hatası: {e}")
    
    async def _gercek_zamanli_metrik_guncelle(
        self, 
        olay_tipi: str, 
        kullanici_id: Optional[int]
    ):
        """Gerçek zamanlı metrikleri güncelle"""
        try:
            # Dakikalık sayaçlar
            dakika_key = f"metrik:dakika:{datetime.now().strftime('%Y%m%d%H%M')}"
            self.redis_client.hincrby(dakika_key, olay_tipi, 1)
            self.redis_client.expire(dakika_key, 3600)  # 1 saat TTL
            
            # Saatlik sayaçlar
            saat_key = f"metrik:saat:{datetime.now().strftime('%Y%m%d%H')}"
            self.redis_client.hincrby(saat_key, olay_tipi, 1)
            self.redis_client.expire(saat_key, 86400)  # 1 gün TTL
            
            # Günlük sayaçlar
            gun_key = f"metrik:gun:{datetime.now().strftime('%Y%m%d')}"
            self.redis_client.hincrby(gun_key, olay_tipi, 1)
            self.redis_client.expire(gun_key, 2592000)  # 30 gün TTL
            
        except Exception as e:
            logger.error(f"Gerçek zamanlı metrik güncelleme hatası: {e}")
    
    async def kullanici_davranis_analizi(
        self,
        kullanici_id: int,
        baslangic_tarihi: datetime,
        bitis_tarihi: datetime
    ) -> Dict[str, Any]:
        """Kullanıcı davranış analizi"""
        try:
            db = next(get_db())
            
            # Kullanıcı olaylarını getir
            olaylar = db.query(Olay).filter(
                Olay.kullanici_id == kullanici_id,
                Olay.olusturulma_tarihi >= baslangic_tarihi,
                Olay.olusturulma_tarihi <= bitis_tarihi
            ).all()
            
            if not olaylar:
                return {
                    "kullanici_id": kullanici_id,
                    "toplam_olay": 0,
                    "analiz": "Yeterli veri yok"
                }
            
            # DataFrame'e çevir
            df = pd.DataFrame([{
                "olay_tipi": olay.olay_tipi,
                "zaman": olay.olusturulma_tarihi,
                "kaynak": olay.kaynak
            } for olay in olaylar])
            
            # Temel istatistikler
            olay_sayilari = df['olay_tipi'].value_counts().to_dict()
            kaynak_sayilari = df['kaynak'].value_counts().to_dict()
            
            # Zaman bazlı analiz
            df['saat'] = df['zaman'].dt.hour
            saatlik_dagilim = df['saat'].value_counts().sort_index().to_dict()
            
            # Aktivite yoğunluğu
            df['tarih'] = df['zaman'].dt.date
            gunluk_aktivite = df['tarih'].value_counts().sort_index()
            
            # En aktif gün ve saat
            en_aktif_gun = gunluk_aktivite.idxmax()
            en_aktif_saat = max(saatlik_dagilim, key=saatlik_dagilim.get)
            
            return {
                "kullanici_id": kullanici_id,
                "analiz_donemi": {
                    "baslangic": baslangic_tarihi.isoformat(),
                    "bitis": bitis_tarihi.isoformat()
                },
                "toplam_olay": len(olaylar),
                "olay_tipleri": olay_sayilari,
                "kaynak_dagilimi": kaynak_sayilari,
                "saatlik_dagilim": saatlik_dagilim,
                "en_aktif_gun": str(en_aktif_gun),
                "en_aktif_saat": en_aktif_saat,
                "ortalama_gunluk_aktivite": float(gunluk_aktivite.mean()),
                "aktivite_tutarliligi": float(gunluk_aktivite.std())
            }
            
        except Exception as e:
            logger.error(f"Kullanıcı davranış analizi hatası: {e}")
            return {"hata": str(e)}
    
    async def sistem_performans_metrikleri(
        self,
        son_dakika: int = 60
    ) -> Dict[str, Any]:
        """Sistem performans metriklerini getir"""
        try:
            metriker = {}
            
            # Son N dakikadaki olaylar
            for i in range(son_dakika):
                zaman = datetime.now() - timedelta(minutes=i)
                dakika_key = f"metrik:dakika:{zaman.strftime('%Y%m%d%H%M')}"
                
                dakika_verileri = self.redis_client.hgetall(dakika_key)
                if dakika_verileri:
                    metriker[zaman.strftime('%H:%M')] = {
                        k: int(v) for k, v in dakika_verileri.items()
                    }
            
            # Toplam sayılar
            toplam_metrikler = {}
            for dakika_data in metriker.values():
                for olay_tipi, sayi in dakika_data.items():
                    toplam_metrikler[olay_tipi] = toplam_metrikler.get(olay_tipi, 0) + sayi
            
            # Ortalama hesapla
            ortalama_metrikler = {
                k: v / son_dakika for k, v in toplam_metrikler.items()
            }
            
            return {
                "zaman_araligi": f"Son {son_dakika} dakika",
                "dakikalik_metrikler": metriker,
                "toplam_metrikler": toplam_metrikler,
                "ortalama_metrikler": ortalama_metrikler,
                "son_guncelleme": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Sistem performans metrikleri hatası: {e}")
            return {"hata": str(e)}
    
    async def anomali_tespiti(
        self,
        metrik_adi: str,
        son_gun: int = 7
    ) -> Dict[str, Any]:
        """Anomali tespiti yap"""
        try:
            # Son N günün verilerini al
            veriler = []
            for i in range(son_gun * 24):  # Saatlik veriler
                zaman = datetime.now() - timedelta(hours=i)
                saat_key = f"metrik:saat:{zaman.strftime('%Y%m%d%H')}"
                
                veri = self.redis_client.hget(saat_key, metrik_adi)
                veriler.append(int(veri) if veri else 0)
            
            if len(veriler) < 24:  # En az 24 saatlik veri gerekli
                return {
                    "metrik_adi": metrik_adi,
                    "durum": "Yeterli veri yok"
                }
            
            # Veriyi numpy array'e çevir
            X = np.array(veriler).reshape(-1, 1)
            
            # Standartlaştır
            X_scaled = self.scaler.fit_transform(X)
            
            # Anomali tespiti
            anomali_skorlari = self.anomali_modeli.fit_predict(X_scaled)
            anomali_indeksleri = np.where(anomali_skorlari == -1)[0]
            
            # Anomali zamanlarını hesapla
            anomali_zamanlari = []
            for indeks in anomali_indeksleri:
                zaman = datetime.now() - timedelta(hours=indeks)
                anomali_zamanlari.append({
                    "zaman": zaman.isoformat(),
                    "deger": veriler[indeks],
                    "skor": float(anomali_skorlari[indeks])
                })
            
            return {
                "metrik_adi": metrik_adi,
                "analiz_donemi": f"Son {son_gun} gün",
                "toplam_veri_noktasi": len(veriler),
                "anomali_sayisi": len(anomali_indeksleri),
                "anomali_orani": len(anomali_indeksleri) / len(veriler),
                "anomali_zamanlari": anomali_zamanlari,
                "ortalama_deger": float(np.mean(veriler)),
                "standart_sapma": float(np.std(veriler))
            }
            
        except Exception as e:
            logger.error(f"Anomali tespiti hatası: {e}")
            return {"hata": str(e)}
    
    async def dashboard_verileri(self) -> Dict[str, Any]:
        """Dashboard için özet veriler"""
        try:
            # Gerçek zamanlı sayaçlar
            mevcut_dakika = datetime.now().strftime('%Y%m%d%H%M')
            dakika_key = f"metrik:dakika:{mevcut_dakika}"
            dakika_verileri = self.redis_client.hgetall(dakika_key)
            
            # Son 24 saatin özeti
            saatlik_veriler = {}
            for i in range(24):
                zaman = datetime.now() - timedelta(hours=i)
                saat_key = f"metrik:saat:{zaman.strftime('%Y%m%d%H')}"
                saat_verileri = self.redis_client.hgetall(saat_key)
                
                if saat_verileri:
                    saatlik_veriler[zaman.strftime('%H:00')] = {
                        k: int(v) for k, v in saat_verileri.items()
                    }
            
            # Toplam kullanıcı sayısı
            toplam_kullanici = len(self.redis_client.keys("kullanici_olay:*"))
            
            # En popüler olay tipleri
            olay_sayaclari = {}
            for key in self.redis_client.keys("olay_sayaci:*"):
                olay_tipi = key.split(":")[-1]
                sayi = int(self.redis_client.get(key) or 0)
                olay_sayaclari[olay_tipi] = sayi
            
            # En popüler 5 olay tipi
            en_populer_olaylar = dict(
                sorted(olay_sayaclari.items(), key=lambda x: x[1], reverse=True)[:5]
            )
            
            return {
                "gercek_zamanli": {
                    "mevcut_dakika": dakika_verileri,
                    "zaman": datetime.now().isoformat()
                },
                "saatlik_trend": saatlik_veriler,
                "genel_istatistikler": {
                    "toplam_kullanici": toplam_kullanici,
                    "toplam_olay_tipi": len(olay_sayaclari),
                    "en_populer_olaylar": en_populer_olaylar
                },
                "son_guncelleme": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dashboard verileri hatası: {e}")
            return {"hata": str(e)}
    
    def durum_bilgisi(self) -> Dict[str, Any]:
        """Analiz motoru durum bilgisi"""
        try:
            redis_durum = self.redis_client.ping() if self.redis_client else False
            influxdb_durum = bool(self.influxdb_client)
            
            return {
                "redis_baglantisi": redis_durum,
                "influxdb_baglantisi": influxdb_durum,
                "anomali_modeli": bool(self.anomali_modeli),
                "aktif": redis_durum,
                "son_guncelleme": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Durum bilgisi hatası: {e}")
            return {"aktif": False, "hata": str(e)}
```

### app/api/v1/dashboard.py
```python
from typing import Any
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta

from app.cekirdek.analiz_motoru import AnalizMotoru
from app.ayar import ayarlar

router = APIRouter()

# Global analiz motoru instance
analiz_motoru = AnalizMotoru(ayarlar.ANALIZ_AYARLARI)

@router.get("/genel-bakis")
async def genel_bakis() -> Any:
    """Dashboard genel bakış"""
    try:
        veriler = await analiz_motoru.dashboard_verileri()
        return veriler
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performans-metrikleri")
async def performans_metrikleri(
    dakika: int = Query(60, ge=1, le=1440)
) -> Any:
    """Sistem performans metrikleri"""
    try:
        metrikler = await analiz_motoru.sistem_performans_metrikleri(dakika)
        return metrikler
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomali-raporu")
async def anomali_raporu(
    metrik: str = Query(..., description="Metrik adı"),
    gun: int = Query(7, ge=1, le=30)
) -> Any:
    """Anomali tespit raporu"""
    try:
        rapor = await analiz_motoru.anomali_tespiti(metrik, gun)
        return rapor
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kullanici-analizi/{kullanici_id}")
async def kullanici_analizi(
    kullanici_id: int,
    gun: int = Query(30, ge=1, le=365)
) -> Any:
    """Kullanıcı davranış analizi"""
    try:
        bitis = datetime.now()
        baslangic = bitis - timedelta(days=gun)
        
        analiz = await analiz_motoru.kullanici_davranis_analizi(
            kullanici_id, baslangic, bitis
        )
        
        return analiz
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### app/eyay.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import olay, metrik, rapor, dashboard
from app.ayar import ayarlar

app = FastAPI(
    title="EyAy.OS Analiz Servisi",
    description="Analiz ve izleme mikroservisi",
    version="0.1.0",
    docs_url="/docs" if ayarlar.DEBUG else None,
    redoc_url="/redoc" if ayarlar.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ayarlar.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları dahil et
app.include_router(
    olay.router, 
    prefix="/api/v1/olay", 
    tags=["olay"]
)
app.include_router(
    metrik.router, 
    prefix="/api/v1/metrik", 
    tags=["metrik"]
)
app.include_router(
    rapor.router, 
    prefix="/api/v1/rapor", 
    tags=["rapor"]
)
app.include_router(
    dashboard.router, 
    prefix="/api/v1/dashboard", 
    tags=["dashboard"]
)

@app.get("/saglik")
async def saglik_kontrolu():
    return {"durum": "saglikli", "servis": "analiz-servisi"}

@app.get("/")
async def ana_sayfa():
    return {
        "mesaj": "EyAy.OS Analiz Servisi", 
        "surum": "0.1.0",
        "dashboard": "/api/v1/dashboard/genel-bakis"
    }

@app.get("/yetenekler")
async def yetenekler():
    return {
        "olay_takibi": True,
        "performans_metrikleri": True,
        "anomali_tespiti": True,
        "kullanici_analizi": True,
        "gercek_zamanli_dashboard": True,
        "zaman_serisi_analizi": True
    }
```

## 🚀 Çalıştırma

```bash
# Bağımlılıkları yükle
cd hizmetler/analiz
poetry install

# Development server başlat
poetry run uvicorn app.eyay:app --reload --port 8005

# Dashboard görüntüle
curl http://localhost:8005/api/v1/dashboard/genel-bakis
```

## 📋 API Endpoints

### Dashboard
- `GET /api/v1/dashboard/genel-bakis` - Genel dashboard
- `GET /api/v1/dashboard/performans-metrikleri` - Performans metrikleri
- `GET /api/v1/dashboard/anomali-raporu` - Anomali raporu
- `GET /api/v1/dashboard/kullanici-analizi/{id}` - Kullanıcı analizi

### Olay Takibi
- `POST /api/v1/olay/kaydet` - Olay kaydet
- `GET /api/v1/olay/listele` - Olayları listele
- `GET /api/v1/olay/istatistik` - Olay istatistikleri

### Metrikler
- `GET /api/v1/metrik/gercek-zamanli` - Gerçek zamanlı metrikler
- `GET /api/v1/metrik/trend` - Trend analizi
- `GET /api/v1/metrik/karsilastirma` - Dönem karşılaştırması

## 📊 Analiz Özellikleri

- **Gerçek Zamanlı İzleme**: Dakika bazında metrik toplama
- **Anomali Tespiti**: Machine learning ile anormal davranış tespiti
- **Kullanıcı Analizi**: Bireysel kullanıcı davranış profilleri
- **Trend Analizi**: Zaman serisi analizi ve tahminleme
- **Dashboard**: Görsel raporlama ve grafikler
