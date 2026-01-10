"""
Harcama Servisi
Harcama kayıtları ile ilgili iş mantığı fonksiyonlarını içerir.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.arac import Araclar
from sunucu.semalar.harcama_sema import HarcamaOlustur, HarcamaGuncelle, KategoriHarcama, HarcamaOzet
from typing import List
from decimal import Decimal


def harcama_olustur(db: Session, harcama_bilgileri: HarcamaOlustur) -> Harcamalar:
    """
    Yeni bir harcama kaydı oluşturur.
    
    Args:
        db: Veritabanı session'ı
        harcama_bilgileri: Oluşturulacak harcama bilgileri
        
    Returns:
        Harcamalar: Oluşturulan harcama nesnesi
        
    Raises:
        HTTPException: Araç bulunamazsa
    """
    # Araç kontrolü
    arac = db.query(Araclar).filter(
        and_(
            Araclar.id == harcama_bilgileri.arac_id,
            Araclar.silinmis_mi == False
        )
    ).first()
    
    if not arac:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {harcama_bilgileri.arac_id} ile araç bulunamadı"
        )
    
    # Yeni harcama kaydı oluştur
    yeni_harcama = Harcamalar(**harcama_bilgileri.model_dump())
    db.add(yeni_harcama)
    db.commit()
    db.refresh(yeni_harcama)
    
    return yeni_harcama


def harcama_getir(db: Session, harcama_id: int) -> Harcamalar:
    """
    ID ile harcama kaydı getirir.
    
    Args:
        db: Veritabanı session'ı
        harcama_id: Harcama ID
        
    Returns:
        Harcamalar: Bulunan harcama nesnesi
        
    Raises:
        HTTPException: Harcama kaydı bulunamazsa
    """
    harcama = db.query(Harcamalar).filter(
        and_(
            Harcamalar.id == harcama_id,
            Harcamalar.silinmis_mi == False
        )
    ).first()
    
    if not harcama:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {harcama_id} ile harcama kaydı bulunamadı"
        )
    
    return harcama


def arac_harcamalari_getir(
    db: Session,
    arac_id: int,
    kategori: str = None,
    atlama: int = 0,
    limit: int = 100
) -> List[Harcamalar]:
    """
    Belirli bir aracın harcama kayıtlarını getirir.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        kategori: Opsiyonel kategori filtresi
        atlama: Kaç kayıt atlanacak
        limit: Maksimum kaç kayıt getirilecek
        
    Returns:
        List[Harcamalar]: Harcama kayıtları listesi
    """
    sorgu = db.query(Harcamalar).filter(
        and_(
            Harcamalar.arac_id == arac_id,
            Harcamalar.silinmis_mi == False
        )
    )
    
    if kategori:
        sorgu = sorgu.filter(Harcamalar.kategori == kategori)
    
    return sorgu.order_by(Harcamalar.tarih.desc()).offset(atlama).limit(limit).all()


def harcama_guncelle(db: Session, harcama_id: int, harcama_bilgileri: HarcamaGuncelle) -> Harcamalar:
    """
    Harcama kaydını günceller.
    
    Args:
        db: Veritabanı session'ı
        harcama_id: Güncellenecek harcama ID
        harcama_bilgileri: Yeni harcama bilgileri
        
    Returns:
        Harcamalar: Güncellenmiş harcama nesnesi
    """
    harcama = harcama_getir(db, harcama_id)
    
    # Güncellenecek verileri al
    guncelleme_verisi = harcama_bilgileri.model_dump(exclude_unset=True)
    
    # Güncelle
    for alan, deger in guncelleme_verisi.items():
        setattr(harcama, alan, deger)
    
    db.commit()
    db.refresh(harcama)
    
    return harcama


def harcama_sil(db: Session, harcama_id: int) -> dict:
    """
    Harcama kaydını soft delete yapar.
    
    Args:
        db: Veritabanı session'ı
        harcama_id: Silinecek harcama ID
        
    Returns:
        dict: Başarı mesajı
    """
    harcama = harcama_getir(db, harcama_id)
    
    harcama.silinmis_mi = True
    db.commit()
    
    return {"mesaj": "Harcama kaydı başarıyla silindi"}


def toplam_harcama_hesapla(db: Session, arac_id: int) -> Decimal:
    """
    Aracın toplam harcamasını hesaplar.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        Decimal: Toplam harcama
    """
    toplam = db.query(func.sum(Harcamalar.tutar)).filter(
        and_(
            Harcamalar.arac_id == arac_id,
            Harcamalar.silinmis_mi == False
        )
    ).scalar()
    
    return Decimal(str(toplam)) if toplam else Decimal("0")


def kategori_bazli_harcama(db: Session, arac_id: int) -> HarcamaOzet:
    """
    Kategori bazında harcama analizi yapar.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        HarcamaOzet: Kategori bazlı harcama özeti
    """
    # Kategori bazlı gruplama
    sonuclar = db.query(
        Harcamalar.kategori,
        func.sum(Harcamalar.tutar).label('toplam_tutar'),
        func.count(Harcamalar.id).label('islem_sayisi'),
        func.avg(Harcamalar.tutar).label('ortalama_tutar')
    ).filter(
        and_(
            Harcamalar.arac_id == arac_id,
            Harcamalar.silinmis_mi == False
        )
    ).group_by(Harcamalar.kategori).all()
    
    # Kategori listesi oluştur
    kategori_listesi = [
        KategoriHarcama(
            kategori=sonuc.kategori,
            toplam_tutar=Decimal(str(sonuc.toplam_tutar)),
            islem_sayisi=sonuc.islem_sayisi,
            ortalama_tutar=Decimal(str(sonuc.ortalama_tutar))
        )
        for sonuc in sonuclar
    ]
    
    # Genel toplam
    toplam_tutar = sum(k.toplam_tutar for k in kategori_listesi)
    toplam_islem = sum(k.islem_sayisi for k in kategori_listesi)
    
    return HarcamaOzet(
        toplam_tutar=toplam_tutar,
        islem_sayisi=toplam_islem,
        kategori_dagilimi=kategori_listesi
    )
