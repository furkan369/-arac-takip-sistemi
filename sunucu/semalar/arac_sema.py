from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# --- YARDIMCI MODELLER (Circular Import Önlemek İçin Buraya Taşıdık) ---

class BakimBasit(BaseModel):
    id: int
    bakim_turu: str
    tarih: Optional[datetime] = None
    km: int
    tutar: Optional[float] = 0.0
    aciklama: Optional[str] = None
    
    class Config:
        from_attributes = True

class HarcamaBasit(BaseModel):
    id: int
    kategori: str
    tarih: Optional[datetime] = None
    tutar: float
    aciklama: Optional[str] = None
    
    class Config:
        from_attributes = True

class YakitBasit(BaseModel):
    id: int
    tarih: Optional[datetime] = None
    km: int
    litre: float
    fiyat: float
    tam_depo: bool
    yakit_turu: str
    istasyon: Optional[str] = None
    
    class Config:
        from_attributes = True

class AracTemel(BaseModel):
    plaka: str = Field(..., min_length=7, max_length=20)
    marka: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=2, max_length=50)
    yil: int = Field(..., ge=1900)
    renk: Optional[str] = None
    km: Optional[int] = Field(0, ge=0)
    sase_no: Optional[str] = None
    motor_no: Optional[str] = None
    notlar: Optional[str] = None
    yakit_turu: Optional[str] = "Benzin"
    aktif_mi: bool = True

    @validator('plaka')
    def plaka_buyuk_harf(cls, v):
        return v.upper().replace(" ", "")

class AracOlustur(AracTemel):
    pass

class AracGuncelle(BaseModel):
    plaka: Optional[str] = Field(None, min_length=7, max_length=20)
    marka: Optional[str] = Field(None, min_length=2, max_length=50)
    model: Optional[str] = Field(None, min_length=2, max_length=50)
    yil: Optional[int] = Field(None, ge=1900)
    renk: Optional[str] = None
    km: Optional[int] = Field(None, ge=0)
    aktif_mi: Optional[bool] = None
    notlar: Optional[str] = None
    yakit_turu: Optional[str] = None

    @validator('plaka')
    def plaka_buyuk_harf(cls, v):
        if v:
            return v.upper().replace(" ", "")
        return v

class AracYanit(AracTemel):
    id: int
    olusturulma_tarihi: Optional[datetime] = None

    class Config:
        from_attributes = True

class KilometreGuncelle(BaseModel):
    yeni_km: int = Field(..., ge=0)

class AracOzet(BaseModel):
    id: int
    plaka: str
    marka: str
    model: str
    
    class Config:
        from_attributes = True

# DÜZELTME: Pydantic modellerini kullanıyoruz.
# from_attributes=True sayesinde SQLAlchemy objeleri bu modellere otomatik map edilecek.
class AracDetayliYanit(AracYanit):
    bakimlar: List[BakimBasit] = []
    harcamalar: List[HarcamaBasit] = []
    yakitlar: List[YakitBasit] = []
