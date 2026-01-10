"""
Araç Yönlendirici
Araç ile ilgili API endpoint'lerini içerir.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.semalar.arac_sema import AracOlustur, AracGuncelle, AracYanit, AracOzet, KilometreGuncelle, AracDetayliYanit
from sunucu.servisler import arac_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.bagimliliklar.sahiplik import arac_sahipligini_dogrula
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.arac import Araclar


# Router oluştur
router = APIRouter()


@router.post("", response_model=AracYanit, status_code=201, summary="Yeni Araç Ekle")
def arac_olustur(
    arac: AracOlustur,
    db: Session = Depends(veritabani_baglantisi_al),
    # kullanici: Kullanicilar = Depends(mevcut_kullanici_al)  # GEÇİCİ DEVRE DIŞI
):
    """
    Yeni bir araç kaydı oluşturur.
    
    - **plaka**: Araç plakası (zorunlu, benzersiz)
    - **marka**: Araç markası (zorunlu)
    - **model**: Araç modeli (zorunlu)
    - **yil**: Model yılı (opsiyonel)
    - **renk**: Araç rengi (opsiyonel)
    - **km**: Güncel kilometre (opsiyonel, varsayılan: 0)
    - **sase_no**: Şase numarası (opsiyonel)
    - **motor_no**: Motor numarası (opsiyonel)
    - **notlar**: Ekstra notlar (opsiyonel)
    """
    # GEÇİCİ: Sabit kullanıcı ID (admin = 1)
    return arac_servisi.arac_olustur(db, arac, kullanici_id=1)


@router.get("/{arac_id}", response_model=AracYanit, summary="Araç Detaylarını Getir")
def arac_detayi_getir(
    arac: Araclar = Depends(arac_sahipligini_dogrula)
):
    """
    Belirtilen ID'ye sahip aracın detaylarını getirir.
    Sadece araç sahibi erişebilir.
    
    - **arac_id**: Araç ID numarası
    """
    return arac


@router.get("", response_model=List[AracOzet], summary="Tüm Araçları Listele")
def araclari_listele(
    atlama: int = Query(0, ge=0, description="Kaç kayıt atlanacak"),
    limit: int = Query(100, ge=1, le=500, description="Maksimum kayıt sayısı"),
    sadece_aktifler: bool = Query(True, description="Sadece aktif araçları göster"),
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Kullanıcının tüm araçlarını listeler.
    Admin ise tüm sistemdeki araçları listeler.
    
    - **atlama**: Pagination için atlanacak kayıt sayısı
    - **limit**: Döndürülecek maksimum kayıt sayısı
    - **sadece_aktifler**: True ise sadece aktif araçları getirir
    """
    return arac_servisi.tum_araclari_getir(db, kullanici.id, atlama, limit, sadece_aktifler, kullanici.rol)


@router.put("/{arac_id}", response_model=AracYanit, summary="Araç Bilgilerini Güncelle")
def arac_guncelle(
    arac_guncelleme: AracGuncelle,
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Mevcut bir aracın bilgilerini günceller.
    Sadece araç sahibi güncelleyebilir.
    
    - **arac_id**: Güncellenecek araç ID
    - Tüm alanlar opsiyoneldir, sadece gönderilen alanlar güncellenir
    """
    return arac_servisi.arac_guncelle(db, sahiplik_arac.id, arac_guncelleme)


@router.patch("/{arac_id}/kilometre", response_model=AracYanit, summary="Kilometre Güncelle")
def kilometre_guncelle(
    km_bilgisi: KilometreGuncelle,
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın kilometre bilgisini günceller.
    Sadece araç sahibi güncelleyebilir.
    
    - **arac_id**: Araç ID
    - **km**: Yeni kilometre değeri (mevcut değerden büyük olmalı)
    """
    return arac_servisi.arac_kilometre_guncelle(db, sahiplik_arac.id, km_bilgisi.km)


@router.delete("/{arac_id}", summary="Araç Sil")
def arac_sil(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Belirtilen aracı sistemden siler (soft delete).
    Sadece araç sahibi silebilir.
    
    - **arac_id**: Silinecek araç ID
    
    Not: Araç fiziksel olarak silinmez, 'silinmis_mi' bayrağı True yapılır.
    """
    return arac_servisi.arac_sil(db, sahiplik_arac.id)


@router.get("/istatistik/sayim", summary="Araç Sayısını Getir")
def arac_sayisi(
    sadece_aktifler: bool = Query(True, description="Sadece aktif araçları say"),
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Kullanıcının toplam araç sayısını döndürür.
    Admin ise toplam sistem araç sayısını döndürür.
    
    - **sadece_aktifler**: True ise sadece aktif araçları sayar
    """
    sayi = arac_servisi.arac_sayisi_getir(db, kullanici.id, sadece_aktifler, kullanici.rol)
    return {"toplam_arac": sayi, "sadece_aktifler": sadece_aktifler}


@router.get('/{arac_id}/detay', response_model=AracDetayliYanit)
def arac_detay_getir_endpoint(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """Araç detaylarını getirir. Sadece araç sahibi erişebilir."""
    return arac_servisi.arac_detay_getir(db, sahiplik_arac.id)
