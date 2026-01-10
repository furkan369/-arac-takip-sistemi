"""
Bakım Şemaları
Bakım modeli için request ve response şemalarını içerir.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# Base şema
class BakimBase(BaseModel):
    """Bakım için temel şema"""
    arac_id: int = Field(..., gt=0, description="Araç ID")
    bakim_turu: str = Field(..., min_length=1, max_length=100, description="Bakım türü")
    tarih: date = Field(..., description="Bakım tarihi")
    km: int = Field(..., ge=0, description="Bakım sırasındaki kilometre")
    tutar: Optional[Decimal] = Field(0, ge=0, description="Bakım maliyeti")
    servis_yeri: Optional[str] = Field(None, max_length=100, description="Bakımın yapıldığı yer")
    aciklama: Optional[str] = Field(None, description="Bakım detayları")
    sonraki_bakim_km: Optional[int] = Field(None, ge=0, description="Sonraki bakım kilometresi")
    sonraki_bakim_tarih: Optional[date] = Field(None, description="Sonraki bakım tarihi")


# Bakım oluşturma şeması
class BakimOlustur(BakimBase):
    """Yeni bakım kaydı oluştururken kullanılan şema"""
    pass


# Bakım güncelleme şeması
class BakimGuncelle(BaseModel):
    """Bakım kaydı güncellerken kullanılan şema"""
    bakim_turu: Optional[str] = Field(None, min_length=1, max_length=100)
    tarih: Optional[date] = None
    km: Optional[int] = Field(None, ge=0)
    tutar: Optional[Decimal] = Field(None, ge=0)
    servis_yeri: Optional[str] = Field(None, max_length=100)
    aciklama: Optional[str] = None
    sonraki_bakim_km: Optional[int] = Field(None, ge=0)
    sonraki_bakim_tarih: Optional[date] = None


# Bakım yanıt şeması
class BakimYanit(BakimBase):
    """API yanıtlarında döndürülen bakım şeması"""
    id: int
    silinmis_mi: bool
    olusturulma_tarihi: datetime
    guncellenme_tarihi: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Bakım özet şeması
class BakimOzet(BaseModel):
    """Bakım listesi için basitleştirilmiş şema"""
    id: int
    arac_id: int
    bakim_turu: str
    tarih: date
    km: int
    tutar: Optional[Decimal]
    
    model_config = ConfigDict(from_attributes=True)
