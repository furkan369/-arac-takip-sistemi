"""
Bakım Servisi
Bakım kayıtları ile ilgili iş mantığı fonksiyonlarını içerir.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.arac import Araclar
from sunucu.semalar.bakim_sema import BakimOlustur, BakimGuncelle
from typing import List
from datetime import date


def bakim_olustur(db: Session, bakim_bilgileri: BakimOlustur) -> Bakimlar:
    """
    Yeni bir bakım kaydı oluşturur.
    
    Args:
        db: Veritabanı session'ı
        bakim_bilgileri: Oluşturulacak bakım bilgileri
        
    Returns:
        Bakimlar: Oluşturulan bakım nesnesi
        
    Raises:
        HTTPException: Araç bulunamazsa
    """
    # Araç kontrolü
    arac = db.query(Araclar).filter(
        and_(
            Araclar.id == bakim_bilgileri.arac_id,
            Araclar.silinmis_mi == False
        )
    ).first()
    
    if not arac:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {bakim_bilgileri.arac_id} ile araç bulunamadı"
        )
    
    # Yeni bakım kaydı oluştur
    yeni_bakim = Bakimlar(**bakim_bilgileri.model_dump())
    db.add(yeni_bakim)
    db.commit()
    db.refresh(yeni_bakim)
    
    return yeni_bakim


def bakim_getir(db: Session, bakim_id: int) -> Bakimlar:
    """
    ID ile bakım kaydı getirir.
    
    Args:
        db: Veritabanı session'ı
        bakim_id: Bakım ID
        
    Returns:
        Bakimlar: Bulunan bakım nesnesi
        
    Raises:
        HTTPException: Bakım kaydı bulunamazsa
    """
    bakim = db.query(Bakimlar).filter(
        and_(
            Bakimlar.id == bakim_id,
            Bakimlar.silinmis_mi == False
        )
    ).first()
    
    if not bakim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {bakim_id} ile bakım kaydı bulunamadı"
        )
    
    return bakim


def arac_bakimlari_getir(
    db: Session,
    arac_id: int,
    atlama: int = 0,
    limit: int = 100
) -> List[Bakimlar]:
    """
    Belirli bir aracın tüm bakım kayıtlarını getirir.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        atlama: Kaç kay kayıt atlanacak
        limit: Maksimum kaç kayıt getirilecek
        
    Returns:
        List[Bakimlar]: Bakım kayıtları listesi
    """
    return db.query(Bakimlar).filter(
        and_(
            Bakimlar.arac_id == arac_id,
            Bakimlar.silinmis_mi == False
        )
    ).order_by(Bakimlar.tarih.desc()).offset(atlama).limit(limit).all()


def bakim_guncelle(db: Session, bakim_id: int, bakim_bilgileri: BakimGuncelle) -> Bakimlar:
    """
    Bakım kaydını günceller.
    
    Args:
        db: Veritabanı session'ı
        bakim_id: Güncellenecek bakım ID
        bakim_bilgileri: Yeni bakım bilgileri
        
    Returns:
        Bakimlar: Güncellenmiş bakım nesnesi
    """
    bakim = bakim_getir(db, bakim_id)
    
    # Güncellenecek verileri al
    guncelleme_verisi = bakim_bilgileri.model_dump(exclude_unset=True)
    
    # Güncelle
    for alan, deger in guncelleme_verisi.items():
        setattr(bakim, alan, deger)
    
    db.commit()
    db.refresh(bakim)
    
    return bakim


def bakim_sil(db: Session, bakim_id: int) -> dict:
    """
    Bakım kaydını soft delete yapar.
    
    Args:
        db: Veritabanı session'ı
        bakim_id: Silinecek bakım ID
        
    Returns:
        dict: Başarı mesajı
    """
    bakim = bakim_getir(db, bakim_id)
    
    bakim.silinmis_mi = True
    db.commit()
    
    return {"mesaj": f"Bakım kaydı başarıyla silindi"}


def son_bakim_getir(db: Session, arac_id: int) -> Bakimlar | None:
    """
    Aracın en son bakım kaydını getirir.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        Bakimlar | None: Son bakım kaydı veya None
    """
    return db.query(Bakimlar).filter(
        and_(
            Bakimlar.arac_id == arac_id,
            Bakimlar.silinmis_mi == False
        )
    ).order_by(Bakimlar.tarih.desc()).first()


def toplam_bakim_maliyeti(db: Session, arac_id: int) -> float:
    """
    Aracın toplam bakım maliyetini hesaplar.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        float: Toplam bakım maliyeti
    """
    toplam = db.query(func.sum(Bakimlar.tutar)).filter(
        and_(
            Bakimlar.arac_id == arac_id,
            Bakimlar.silinmis_mi == False
        )
    ).scalar()
    
    return float(toplam) if toplam else 0.0
