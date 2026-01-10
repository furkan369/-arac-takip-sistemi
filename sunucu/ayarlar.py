"""
Uygulama Konfigurasyon Ayarlari
Bu dosya ortam degiskenlerinden okunan ayarlari yonetir.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Ayarlar(BaseSettings):
    """Uygulama ayarlari sinifi"""
    
    # Veritabani Ayarlari
    VERITABANI_SUNUCU: str = "localhost"
    VERITABANI_PORT: int = 3306
    VERITABANI_ADI: str = "arac_takip"
    VERITABANI_KULLANICI: str = "root"
    VERITABANI_SIFRE: str = ""
    
    # Uygulama Ayarlari
    HATA_AYIKLAMA_MODU: bool = True
    GUNLUK_SEVIYESI: str = "INFO"
    
    # Güvenlik Ayarları (JWT Authentication)
    SECRET_KEY: str = "DEGISTIR_BUNU_PRODUCTION_DA_OPENSSL_RAND_HEX_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global ayarlar instance'i
ayarlar = Ayarlar()
