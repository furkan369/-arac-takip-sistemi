"""
Araç Servisi
Araç ile ilgili iş mantığı fonksiyonlarını içerir.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional

from sunucu.modeller.arac import Araclar
# İlişkili modeller
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.yakit_takibi import Yakit_Takibi as YakitTakibi
from sunucu.semalar.arac_sema import AracOlustur, AracGuncelle

def arac_olustur(db: Session, arac_bilgileri: AracOlustur, kullanici_id: int) -> Araclar:
    """
    Yeni bir araç kaydı oluşturur.
    """
    # Plaka kontrolü - Aynı kullanıcının silinmemiş kayıtları arasında
    mevcut_arac = db.query(Araclar).filter(
        and_(
            Araclar.plaka == arac_bilgileri.plaka,
            Araclar.kullanici_id == kullanici_id,
            Araclar.silinmis_mi == False
        )
    ).first()
    
    if mevcut_arac:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{arac_bilgileri.plaka}' plakası zaten kayıtlı"
        )
    
    # Yeni araç oluştur (kullanici_id ile)
    yeni_arac = Araclar(**arac_bilgileri.model_dump(), kullanici_id=kullanici_id)
    db.add(yeni_arac)
    db.commit()
    db.refresh(yeni_arac)
    
    return yeni_arac

def arac_getir(db: Session, arac_id: int) -> Araclar:
    """
    ID ile araç getirir.
    """
    arac = db.query(Araclar).filter(
        and_(
            Araclar.id == arac_id,
            Araclar.silinmis_mi == False
        )
    ).first()
    
    if not arac:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {arac_id} ile araç bulunamadı"
        )
    
    return arac


def tum_araclari_getir(
    db: Session,
    kullanici_id: int,
    atlama: int = 0, 
    limit: int = 100,
    sadece_aktifler: bool = True,
    kullanici_rol: str = "kullanici"
) -> List[Araclar]:
    """
    Kullanıcının tüm araçlarını listeler.
    Admin ise tüm araçları listeler.
    """
    sorgu = db.query(Araclar).filter(Araclar.silinmis_mi == False)
    
    # Admin değilse filtrele
    if kullanici_rol != 'admin':
        sorgu = sorgu.filter(Araclar.kullanici_id == kullanici_id)
    
    if sadece_aktifler:
        sorgu = sorgu.filter(Araclar.aktif_mi == True)
    
    return sorgu.offset(atlama).limit(limit).all()

def arac_guncelle(db: Session, arac_id: int, arac_bilgileri: AracGuncelle) -> Araclar:
    """
    Araç bilgilerini günceller.
    """
    # Aracı bul
    arac = arac_getir(db, arac_id)
    
    # Güncellenecek verileri al (sadece dolu olanlar)
    guncelleme_verisi = arac_bilgileri.model_dump(exclude_unset=True)
    
    # Plaka değişikliği varsa, çakışma kontrolü yap
    if "plaka" in guncelleme_verisi and guncelleme_verisi["plaka"] != arac.plaka:
        mevcut_plaka = db.query(Araclar).filter(
            and_(
                Araclar.plaka == guncelleme_verisi["plaka"],
                Araclar.id != arac_id,
                Araclar.silinmis_mi == False
            )
        ).first()
        
        if mevcut_plaka:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{guncelleme_verisi['plaka']}' plakası zaten kayıtlı"
            )
    
    # Güncelle
    for alan, deger in guncelleme_verisi.items():
        setattr(arac, alan, deger)
    
    db.commit()
    db.refresh(arac)
    
    return arac

def arac_kilometre_guncelle(db: Session, arac_id: int, yeni_km: int) -> Araclar:
    """
    Sadece araç kilometresini günceller.
    """
    arac = arac_getir(db, arac_id)
    
    # Kilometre geriye gidemez kontrolü
    if arac.km and yeni_km < arac.km:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Yeni kilometre ({yeni_km}) mevcut kilometreden ({arac.km}) küçük olamaz"
        )
    
    arac.km = yeni_km
    db.commit()
    db.refresh(arac)
    
    return arac

def arac_sil(db: Session, arac_id: int) -> dict:
    """
    Aracı soft delete yapar (silinmis_mi=True).
    """
    arac = arac_getir(db, arac_id)
    
    arac.silinmis_mi = True
    arac.aktif_mi = False
    db.commit()
    
    return {"mesaj": f"'{arac.plaka}' plakalı araç başarıyla silindi"}


def arac_sayisi_getir(db: Session, kullanici_id: int, sadece_aktifler: bool = True, kullanici_rol: str = "kullanici") -> int:
    """
    Kullanıcının toplam araç sayısını döndürür.
    Admin ise tüm araçları sayar.
    """
    sorgu = db.query(Araclar).filter(Araclar.silinmis_mi == False)
    
    if kullanici_rol != 'admin':
        sorgu = sorgu.filter(Araclar.kullanici_id == kullanici_id)
    
    if sadece_aktifler:
        sorgu = sorgu.filter(Araclar.aktif_mi == True)
    
    return sorgu.count()

def arac_detay_getir(db: Session, arac_id: int):
    """
    Aracı ve ilişkili tüm kayıtları getirir.
    """
    arac = arac_getir(db, arac_id)
    
    # İlişkili verileri manuel çek
    bakimlar = db.query(Bakimlar).filter(Bakimlar.arac_id == arac_id).order_by(Bakimlar.tarih.desc()).all()
    harcamalar = db.query(Harcamalar).filter(Harcamalar.arac_id == arac_id).order_by(Harcamalar.tarih.desc()).all()
    yakitlar = db.query(YakitTakibi).filter(YakitTakibi.arac_id == arac_id).order_by(YakitTakibi.tarih.desc()).all()
    
    # Araca dinamik olarak bu listeleri ekle
    # SQLAlchemy objesine attribute eklemek kalıcı olmaz ama bu scope'da iş görür
    # Pydantic v2 from_attributes bu dinamik property'leri de okuyacaktır
    arac.bakimlar = bakimlar
    arac.harcamalar = harcamalar
    arac.yakitlar = yakitlar
    
    return arac
