"""
Bakım Yönlendirici
Bakım kayıtları ile ilgili API endpoint'lerini içerir.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.semalar.bakim_sema import BakimOlustur, BakimGuncelle, BakimYanit, BakimOzet
from sunucu.servisler import bakim_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.bagimliliklar.sahiplik import arac_sahipligini_dogrula, bakim_sahipligini_dogrula
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.arac import Araclar


# Router oluştur
router = APIRouter()


@router.post("/", response_model=BakimYanit, status_code=201, summary="Yeni Bakım Kaydı Ekle")
def bakim_olustur(
    bakim: BakimOlustur,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Yeni bir bakım kaydı oluşturur.
    Sadece yetkili olunan araçlar için kayıt eklenebilir.
    
    - **arac_id**: Araç ID (zorunlu)
    - **bakim_turu**: Bakım türü (zorunlu)
    - **tarih**: Bakım tarihi (zorunlu)
    - **km**: Bakım sırasındaki kilometre (zorunlu)
    - **tutar**: Bakım maliyeti (opsiyonel)
    - **servis_yeri**: Bakımın yapıldığı yer (opsiyonel)
    - **aciklama**: Bakım detayları (opsiyonel)
    """
    # Aracın sahibi mi kontrol et
    arac_sahipligini_dogrula(bakim.arac_id, db, kullanici)
    
    return bakim_servisi.bakim_olustur(db, bakim)


@router.get("/{bakim_id}", response_model=BakimYanit, summary="Bakım Detaylarını Getir")
def bakim_detayi_getir(
    bakim: Bakimlar = Depends(bakim_sahipligini_dogrula)
):
    """
    Belirtilen ID'ye sahip bakım detaylarını getirir.
    
    - **bakim_id**: Bakım kaydı ID
    """
    return bakim


@router.get("/arac/{arac_id}", response_model=List[BakimOzet], summary="Araç Bakımlarını Listele")
def arac_bakimlari(
    arac_id: int,
    atlama: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(veritabani_baglantisi_al),
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula)
):
    """
    Belirli bir aracın tüm bakım kayıtlarını listeler.
    Sadece yetkili olunan araçlar için.
    
    - **arac_id**: Araç ID
    - **atlama**: Pagination için atlanacak kayıt sayısı
    - **limit**: Maksimum kayıt sayısı
    """
    return bakim_servisi.arac_bakimlari_getir(db, sahiplik_arac.id, atlama, limit)


@router.put("/{bakim_id}", response_model=BakimYanit, summary="Bakım Kaydını Güncelle")
def bakim_guncelle(
    bakim_guncelleme: BakimGuncelle,
    sahiplik_bakim: Bakimlar = Depends(bakim_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Mevcut bir bakım kaydını günceller.
    
    - **bakim_id**: Güncellenecek bakım ID
    - Tüm alanlar opsiyoneldir
    """
    return bakim_servisi.bakim_guncelle(db, sahiplik_bakim.id, bakim_guncelleme)


@router.delete("/{bakim_id}", summary="Bakım Kaydını Sil")
def bakim_sil(
    sahiplik_bakim: Bakimlar = Depends(bakim_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Belirtilen bakım kaydını siler (soft delete).
    
    - **bakim_id**: Silinecek bakım ID
    """
    return bakim_servisi.bakim_sil(db, sahiplik_bakim.id)


@router.get("/arac/{arac_id}/son-bakim", response_model=BakimYanit, summary="Son Bakım Kaydını Getir")
def son_bakim(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın en son bakım kaydını getirir.
    
    - **arac_id**: Araç ID
    """
    sonuc = bakim_servisi.son_bakim_getir(db, sahiplik_arac.id)
    if not sonuc:
        return {"mesaj": "Henüz bakım kaydı bulunmuyor"}
    return sonuc


@router.get("/arac/{arac_id}/toplam-maliyet", summary="Toplam Bakım Maliyeti")
def toplam_maliyet(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın toplam bakım maliyetini hesaplar.
    
    - **arac_id**: Araç ID
    """
    toplam = bakim_servisi.toplam_bakim_maliyeti(db, sahiplik_arac.id)
    return {"arac_id": sahiplik_arac.id, "toplam_bakim_maliyeti": toplam}
