"""
Harcama Şemaları
Harcama modeli için request ve response şemalarını içerir.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# Base şema
class HarcamaBase(BaseModel):
    """Harcama için temel şema"""
    arac_id: int = Field(..., gt=0, description="Araç ID")
    kategori: str = Field(..., min_length=1, max_length=50, description="Harcama kategorisi")
    tarih: date = Field(..., description="Harcama tarihi")
    tutar: Decimal = Field(..., gt=0, description="Harcama miktarı")
    aciklama: Optional[str] = Field(None, description="Harcama detayları")
    fis_no: Optional[str] = Field(None, max_length=50, description="Fiş/Fatura numarası")


# Harcama oluşturma şeması
class HarcamaOlustur(HarcamaBase):
    """Yeni harcama oluştururken kullanılan şema"""
    pass


# Harcama güncelleme şeması
class HarcamaGuncelle(BaseModel):
    """Harcama güncellerken kullanılan şema"""
    kategori: Optional[str] = Field(None, min_length=1, max_length=50)
    tarih: Optional[date] = None
    tutar: Optional[Decimal] = Field(None, gt=0)
    aciklama: Optional[str] = None
    fis_no: Optional[str] = Field(None, max_length=50)


# Harcama yanıt şeması
class HarcamaYanit(HarcamaBase):
    """API yanıtlarında döndürülen harcama şeması"""
    id: int
    silinmis_mi: bool
    olusturulma_tarihi: datetime
    guncellenme_tarihi: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Kategori bazlı harcama analizi
class KategoriHarcama(BaseModel):
    """Kategori bazlı harcama istatistiği"""
    kategori: str
    toplam_tutar: Decimal
    islem_sayisi: int
    ortalama_tutar: Decimal


# Toplam harcama özeti
class HarcamaOzet(BaseModel):
    """Genel harcama özeti"""
    toplam_tutar: Decimal
    islem_sayisi: int
    kategori_dagilimi: list[KategoriHarcama]
