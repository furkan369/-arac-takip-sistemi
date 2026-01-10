"""
Yakıt Takip Servisi
Yakıt tüketim kayıtları ile ilgili iş mantığı fonksiyonlarını içerir.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from sunucu.modeller.yakit_takibi import Yakit_Takibi
from sunucu.modeller.arac import Araclar
from sunucu.semalar.yakit_sema import YakitOlustur, YakitGuncelle, TuketimAnalizi, IstasyonAnalizi
from typing import List
from decimal import Decimal


def yakit_kaydi_olustur(db: Session, yakit_bilgileri: YakitOlustur) -> Yakit_Takibi:
    """
    Yeni bir yakıt kaydı oluşturur ve ortalama tüketimi hesaplar.
    
    Args:
        db: Veritabanı session'ı
        yakit_bilgileri: Oluşturulacak yakıt bilgileri
        
    Returns:
        Yakit_Takibi: Oluşturulan yakıt kaydı nesnesi
        
    Raises:
        HTTPException: Araç bulunamazsa
    """
    # Araç kontrolü
    arac = db.query(Araclar).filter(
        and_(
            Araclar.id == yakit_bilgileri.arac_id,
            Araclar.silinmis_mi == False
        )
    ).first()
    
    if not arac:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {yakit_bilgileri.arac_id} ile araç bulunamadı"
        )
    
    # Yeni yakıt kaydı oluştur
    yeni_kayit = Yakit_Takibi(**yakit_bilgileri.model_dump())
    
    # Ortalama tüketim hesapla (tam depo ise)
    if yakit_bilgileri.tam_depo:
        # Bir önceki tam depo kaydını bul
        onceki_kayit = db.query(Yakit_Takibi).filter(
            and_(
                Yakit_Takibi.arac_id == yakit_bilgileri.arac_id,
                Yakit_Takibi.tam_depo == True,
                Yakit_Takibi.km < yakit_bilgileri.km,
                Yakit_Takibi.silinmis_mi == False
            )
        ).order_by(Yakit_Takibi.km.desc()).first()
        
        if onceki_kayit:
            # Gidilen mesafe
            mesafe = yakit_bilgileri.km - onceki_kayit.km
            if mesafe > 0:
                # Ortalama tüketim = (Alınan yakıt * 100) / Mesafe
                yeni_kayit.ortalama_tuketim = (yakit_bilgileri.litre * 100) / mesafe
    
    db.add(yeni_kayit)
    db.commit()
    db.refresh(yeni_kayit)
    
    return yeni_kayit


def yakit_kaydi_getir(db: Session, yakit_id: int) -> Yakit_Takibi:
    """
    ID ile yakıt kaydı getirir.
    
    Args:
        db: Veritabanı session'ı
        yakit_id: Yakıt kaydı ID
        
    Returns:
        Yakit_Takibi: Bulunan yakıt kaydı nesnesi
        
    Raises:
        HTTPException: Yakıt kaydı bulunamazsa
    """
    kayit = db.query(Yakit_Takibi).filter(
        and_(
            Yakit_Takibi.id == yakit_id,
            Yakit_Takibi.silinmis_mi == False
        )
    ).first()
    
    if not kayit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {yakit_id} ile yakıt kaydı bulunamadı"
        )
    
    return kayit


def arac_yakit_kayitlari_getir(
    db: Session,
    arac_id: int,
    atlama: int = 0,
    limit: int = 100
) -> List[Yakit_Takibi]:
    """
    Belirli bir aracın yakıt kayıtlarını getirir.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        atlama: Kaç kayıt atlanacak
        limit: Maksimum kaç kayıt getirilecek
        
    Returns:
        List[Yakit_Takibi]: Yakıt kayıtları listesi
    """
    return db.query(Yakit_Takibi).filter(
        and_(
            Yakit_Takibi.arac_id == arac_id,
            Yakit_Takibi.silinmis_mi == False
        )
    ).order_by(Yakit_Takibi.tarih.desc()).offset(atlama).limit(limit).all()


def yakit_kaydi_guncelle(db: Session, yakit_id: int, yakit_bilgileri: YakitGuncelle) -> Yakit_Takibi:
    """
    Yakıt kaydını günceller.
    
    Args:
        db: Veritabanı session'ı
        yakit_id: Güncellenecek yakıt kaydı ID
        yakit_bilgileri: Yeni yakıt bilgileri
        
    Returns:
        Yakit_Takibi: Güncellenmiş yakıt kaydı nesnesi
    """
    kayit = yakit_kaydi_getir(db, yakit_id)
    
    # Güncellenecek verileri al
    guncelleme_verisi = yakit_bilgileri.model_dump(exclude_unset=True)
    
    # Güncelle
    for alan, deger in guncelleme_verisi.items():
        setattr(kayit, alan, deger)
    
    db.commit()
    db.refresh(kayit)
    
    return kayit


def yakit_kaydi_sil(db: Session, yakit_id: int) -> dict:
    """
    Yakıt kaydını soft delete yapar.
    
    Args:
        db: Veritabanı session'ı
        yakit_id: Silinecek yakıt kaydı ID
        
    Returns:
        dict: Başarı mesajı
    """
    kayit = yakit_kaydi_getir(db, yakit_id)
    
    kayit.silinmis_mi = True
    db.commit()
    
    return {"mesaj": "Yakıt kaydı başarıyla silindi"}


def ortalama_tuketim_hesapla(db: Session, arac_id: int) -> TuketimAnalizi:
    """
    Aracın genel yakıt tüketim analizini yapar.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        TuketimAnalizi: Yakıt tüketim analizi sonucu
    """
    # Tüm kayıtları al
    kayitlar = db.query(Yakit_Takibi).filter(
        and_(
            Yakit_Takibi.arac_id == arac_id,
            Yakit_Takibi.silinmis_mi == False
        )
    ).order_by(Yakit_Takibi.km).all()
    
    if not kayitlar:
        return TuketimAnalizi(
            ortalama_tuketim=Decimal("0"),
            toplam_yakit=Decimal("0"),
            toplam_harcama=Decimal("0"),
            toplam_mesafe=0,
            kayit_sayisi=0
        )
    
    # Toplamları hesapla
    toplam_yakit = sum(k.litre for k in kayitlar)
    toplam_harcama = sum(k.toplam_tutar for k in kayitlar)
    kayit_sayisi = len(kayitlar)
    
    # İlk ve son kayıt arası mesafe
    ilk_kayit = kayitlar[0]
    son_kayit = kayitlar[-1]
    toplam_mesafe = son_kayit.km - ilk_kayit.km
    
    # Ortalama tüketim hesapla
    if toplam_mesafe > 0:
        ortalama_tuketim = (toplam_yakit * 100) / toplam_mesafe
    else:
        ortalama_tuketim = Decimal("0")
    
    return TuketimAnalizi(
        ortalama_tuketim=Decimal(str(round(ortalama_tuketim, 2))),
        toplam_yakit=Decimal(str(toplam_yakit)),
        toplam_harcama=Decimal(str(toplam_harcama)),
        toplam_mesafe=toplam_mesafe,
        kayit_sayisi=kayit_sayisi
    )


def istasyon_analizi(db: Session, arac_id: int) -> List[IstasyonAnalizi]:
    """
    İstasyon bazlı yakıt analizi yapar.
    
    Args:
        db: Veritabanı session'ı
        arac_id: Araç ID
        
    Returns:
        List[IstasyonAnalizi]: İstasyon bazlı analiz listesi
    """
    sonuclar = db.query(
        Yakit_Takibi.istasyon,
        func.avg(Yakit_Takibi.fiyat).label('ortalama_fiyat'),
        func.sum(Yakit_Takibi.litre).label('toplam_litre'),
        func.count(Yakit_Takibi.id).label('islem_sayisi')
    ).filter(
        and_(
            Yakit_Takibi.arac_id == arac_id,
            Yakit_Takibi.istasyon.isnot(None),
            Yakit_Takibi.silinmis_mi == False
        )
    ).group_by(Yakit_Takibi.istasyon).all()
    
    return [
        IstasyonAnalizi(
            istasyon=sonuc.istasyon,
            ortalama_fiyat=Decimal(str(sonuc.ortalama_fiyat)),
            toplam_litre=Decimal(str(sonuc.toplam_litre)),
            islem_sayisi=sonuc.islem_sayisi
        )
        for sonuc in sonuclar
    ]
