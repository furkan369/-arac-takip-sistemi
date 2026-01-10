"""
Yakıt Takip Şemaları
Yakıt takip modeli için request ve response şemalarını içerir.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# Base şema
class YakitBase(BaseModel):
    """Yakıt kaydı için temel şema"""
    arac_id: int = Field(..., gt=0, description="Araç ID")
    tarih: date = Field(..., description="Yakıt alma tarihi")
    km: int = Field(..., ge=0, description="Yakıt alma sırasındaki kilometre")
    litre: Decimal = Field(..., gt=0, description="Alınan yakıt miktarı")
    fiyat: Decimal = Field(..., gt=0, description="Litre başına fiyat")
    toplam_tutar: Decimal = Field(..., gt=0, description="Toplam maliyet")
    yakit_turu: str = Field(..., min_length=1, max_length=20, description="Yakıt türü")
    istasyon: Optional[str] = Field(None, max_length=100, description="Yakıt istasyonu")
    tam_depo: Optional[bool] = Field(False, description="Depo dolu mu?")
    notlar: Optional[str] = Field(None, description="Ekstra notlar")


# Yakıt kaydı oluşturma şeması
class YakitOlustur(YakitBase):
    """Yeni yakıt kaydı oluştururken kullanılan şema"""
    pass


# Yakıt kaydı güncelleme şeması
class YakitGuncelle(BaseModel):
    """Yakıt kaydı güncellerken kullanılan şema"""
    tarih: Optional[date] = None
    km: Optional[int] = Field(None, ge=0)
    litre: Optional[Decimal] = Field(None, gt=0)
    fiyat: Optional[Decimal] = Field(None, gt=0)
    toplam_tutar: Optional[Decimal] = Field(None, gt=0)
    yakit_turu: Optional[str] = Field(None, min_length=1, max_length=20)
    istasyon: Optional[str] = Field(None, max_length=100)
    tam_depo: Optional[bool] = None
    notlar: Optional[str] = None


# Yakıt kaydı yanıt şeması
class YakitYanit(YakitBase):
    """API yanıtlarında döndürülen yakıt kaydı şeması"""
    id: int
    ortalama_tuketim: Optional[Decimal]
    silinmis_mi: bool
    olusturulma_tarihi: datetime
    guncellenme_tarihi: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Yakıt tüketim analizi
class TuketimAnalizi(BaseModel):
    """Yakıt tüketim analizi sonucu"""
    ortalama_tuketim: Decimal = Field(..., description="Ortalama tüketim (L/100km)")
    toplam_yakit: Decimal = Field(..., description="Toplam alınan yakıt (L)")
    toplam_harcama: Decimal = Field(..., description="Toplam yakıt harcaması")
    toplam_mesafe: int = Field(..., description="Gidilen toplam mesafe (km)")
    kayit_sayisi: int = Field(..., description="Yakıt kaydı sayısı")


# İstasyon bazlı analiz
class IstasyonAnalizi(BaseModel):
    """İstasyon bazlı performans analizi"""
    istasyon: str
    ortalama_fiyat: Decimal
    toplam_litre: Decimal
    islem_sayisi: int
