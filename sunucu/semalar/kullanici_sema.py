"""
Kullanıcı Şemaları (Pydantic)
API request/response validation için
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class KullaniciOlustur(BaseModel):
    """Kullanıcı kayıt şeması"""
    email: EmailStr
    ad_soyad: str
    sifre: str  # Düz metin, hash'lenecek
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "kullanici@example.com",
                "ad_soyad": "Ahmet Yılmaz",
                "sifre": "GuvenlıSıfre123!"
            }
        }



class AdminKullaniciOlustur(KullaniciOlustur):
    """Admin tarafından kullanıcı oluşturma"""
    rol: str = "kullanici"


class KullaniciYanit(BaseModel):
    """Kullanıcı yanıt şeması (şifre olmadan)"""
    id: int
    email: str
    ad_soyad: str
    rol: str
    aktif_mi: bool
    olusturulma_tarihi: datetime
    
    class Config:
        from_attributes = True


class TokenYanit(BaseModel):
    """JWT token yanıt şeması"""
    access_token: str
    token_type: str = "bearer"
    rol: str


class GirisGirdi(BaseModel):
    """Giriş request şeması"""
    email: EmailStr
    sifre: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "kullanici@example.com",
                "sifre": "GuvenlıSıfre123!"
            }
        }

class KullaniciGuncelle(BaseModel):
    """Kullanıcı bilgi güncelleme şeması"""
    ad_soyad: str
    email: Optional[EmailStr] = None


class SifreDegistir(BaseModel):
    """Şifre değiştirme şeması"""
    eski_sifre: str
    yeni_sifre: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "eski_sifre": "EskiSifre123",
                "yeni_sifre": "YeniGuvenliSifre!"
            }
        }
