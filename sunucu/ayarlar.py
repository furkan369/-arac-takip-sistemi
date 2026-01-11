"""
Uygulama Konfigurasyon Ayarlari
Bu dosya ortam degiskenlerinden okunan ayarlari yonetir.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Ayarlar(BaseSettings):
    """Uygulama ayarlari sinifi"""
    
    # Veritabani Ayarlari
    VERITABANI_TIP: str = "mysql"  # "mysql" veya "postgresql"
    VERITABANI_SUNUCU: str = "localhost"
    VERITABANI_PORT: int = 5432
    VERITABANI_ADI: str = "arac_takip"
    VERITABANI_KULLANICI: str = "root"
    VERITABANI_SIFRE: str = ""
    
    # Uygulama Ayarlari
    HATA_AYIKLAMA_MODU: bool = True
    GUNLUK_SEVIYESI: str = "INFO"
    
    # Güvenlik Ayarları (JWT Authentication)
    SECRET_KEY: str = None  # ZORUNLU: .env dosyasından okunmalı
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY:
            import os
            self.SECRET_KEY = os.getenv("SECRET_KEY")
            if not self.SECRET_KEY:
                raise ValueError("SECRET_KEY environment variable zorunludur! Lütfen .env dosyasında tanımlayın.")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global ayarlar instance'i
ayarlar = Ayarlar()
