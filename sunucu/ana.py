"""
FastAPI Uygulama Giris Noktasi
Ana uygulama ve temel endpoint'leri icerir.
"""
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sunucu.veritabani import veritabani_baglantisi_al, engine, Base
from sunucu.ayarlar import ayarlar

# FastAPI uygulama instance'i
uygulama = FastAPI(
    title="Akilli Arac Bakim ve Masraf Takip Sistemi",
    description="Arac bakim, harcama ve yakit takibi icin API",
    version="1.0.0",
    debug=ayarlar.HATA_AYIKLAMA_MODU
)

# CORS Ayarları - Geçici Olarak Tüm Originlere Açık
uygulama.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",  # Geçici: Tüm originlere izin (debugging için)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @uygulama.middleware("http")  <-- Manuel middleware devre dışı bırakıldı
# async def log_requests(request: Request, call_next):
#     ... (kodun geri kalanı)


@uygulama.on_event("startup")
async def baslangic():
    """
    Uygulama baslatildiginda calisir.
    Veritabani baglantisini kontrol eder.
    """
    print("🚀 Uygulama baslatiliyor...")
    print(f"📊 Hata ayiklama modu: {ayarlar.HATA_AYIKLAMA_MODU}")
    print(f"🗄️  Veritabani: {ayarlar.VERITABANI_ADI}")


@uygulama.on_event("shutdown")
async def kapanis():
    """Uygulama kapatildiginda calisir."""
    print("👋 Uygulama kapatiliyor...")


@uygulama.get("/")
async def ana_sayfa():
    """
    Ana sayfa endpoint'i
    
    Returns:
        dict: Hosgeldin mesaji ve API bilgileri
    """
    return {
        "mesaj": "Akilli Arac Bakim ve Masraf Takip Sistemi API",
        "versiyon": "1.0.0",
        "dokumantasyon": "/docs",
        "alternatif_dokumantasyon": "/redoc"
    }


@uygulama.get("/health")
async def saglik_kontrol(db: Session = Depends(veritabani_baglantisi_al)):
    """
    Sistem saglik kontrolu endpoint'i
    Veritabani baglantisini test eder.
    
    Args:
        db: Veritabani session'i (dependency injection)
    
    Returns:
        dict: Sistem durumu bilgileri
    """
    try:
        # Veritabani baglantisini test et
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        veritabani_durumu = "Bagli"
    except Exception as e:
        veritabani_durumu = f"Baglanti hatasi: {str(e)}"
    
    return {
        "durum": "Calisiyor",
        "veritabani": veritabani_durumu,
        "versiyon": "1.0.0"
    }


# Router'ları import et
from sunucu.yonlendiriciler import (
    arac_yonlendirici,
    bakim_yonlendirici,
    harcama_yonlendirici,
    yakit_yonlendirici,
    istatistik_yonlendirici,
    istatistik_yonlendirici,
    auth_yonlendirici,
    kullanici_yonlendirici
)

# Router'ları uygulamaya dahil et
uygulama.include_router(
    arac_yonlendirici.router,
    prefix="/api/v1/araclar",
    tags=["Araçlar"]
)

uygulama.include_router(
    bakim_yonlendirici.router,
    prefix="/api/v1/bakimlar",
    tags=["Bakımlar"]
)

uygulama.include_router(
    harcama_yonlendirici.router,
    prefix="/api/v1/harcamalar",
    tags=["Harcamalar"]
)

uygulama.include_router(
    yakit_yonlendirici.router,
    prefix="/api/v1/yakit",
    tags=["Yakıt Takibi"]
)

uygulama.include_router(
    istatistik_yonlendirici.router,
    prefix="/api/v1",
    tags=["İstatistikler"]
)

# Auth Router (Public - kimlik doğrulama gerektirmez)
uygulama.include_router(
    auth_yonlendirici.router,
    prefix="/api/v1",
    tags=["Kimlik Doğrulama"]
)

# Admin Kullanıcı Yönetimi Router
uygulama.include_router(
    kullanici_yonlendirici.router,
    prefix="/api/v1",
)
