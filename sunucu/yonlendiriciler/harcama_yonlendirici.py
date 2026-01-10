"""
Harcama Yönlendirici
Harcama kayıtları ile ilgili API endpoint'lerini içerir.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.semalar.harcama_sema import HarcamaOlustur, HarcamaGuncelle, HarcamaYanit, HarcamaOzet
from sunucu.servisler import harcama_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.bagimliliklar.sahiplik import arac_sahipligini_dogrula, harcama_sahipligini_dogrula
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.arac import Araclar


# Router oluştur
router = APIRouter()


@router.post("/", response_model=HarcamaYanit, status_code=201, summary="Yeni Harcama Ekle")
def harcama_olustur(
    harcama: HarcamaOlustur,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Yeni bir harcama kaydı oluşturur.
    Sadece yetkili olunan araçlar için kayıt eklenebilir.
    
    - **arac_id**: Araç ID (zorunlu)
    - **kategori**: Harcama kategorisi (zorunlu)
    - **tarih**: Harcama tarihi (zorunlu)
    - **tutar**: Harcama miktarı (zorunlu)
    - **aciklama**: Harcama detayları (opsiyonel)
    - **fis_no**: Fiş/Fatura numarası (opsiyonel)
    """
    # Araç sahipliğini doğrula
    arac_sahipligini_dogrula(harcama.arac_id, db, kullanici)
    
    return harcama_servisi.harcama_olustur(db, harcama)


@router.get("/{harcama_id}", response_model=HarcamaYanit, summary="Harcama Detaylarını Getir")
def harcama_detayi_getir(
    harcama: Harcamalar = Depends(harcama_sahipligini_dogrula)
):
    """
    Belirtilen ID'ye sahip harcama detaylarını getirir.
    
    - **harcama_id**: Harcama kaydı ID
    """
    return harcama


@router.get("/arac/{arac_id}", response_model=List[HarcamaYanit], summary="Araç Harcamalarını Listele")
def arac_harcamalari(
    arac_id: int,
    kategori: Optional[str] = Query(None, description="Kategori filtresi"),
    atlama: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(veritabani_baglantisi_al),
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula)
):
    """
    Belirli bir aracın harcama kayıtlarını listeler.
    Sadece yetkili olunan araçlar için.
    
    - **arac_id**: Araç ID
    - **kategori**: Belirli bir kategoriye göre filtrele (opsiyonel)
    - **atlama**: Pagination için atlanacak kayıt sayısı
    - **limit**: Maksimum kayıt sayısı
    """
    return harcama_servisi.arac_harcamalari_getir(db, sahiplik_arac.id, kategori, atlama, limit)


@router.put("/{harcama_id}", response_model=HarcamaYanit, summary="Harcama Kaydını Güncelle")
def harcama_guncelle(
    harcama_guncelleme: HarcamaGuncelle,
    sahiplik_harcama: Harcamalar = Depends(harcama_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Mevcut bir harcama kaydını günceller.
    
    - **harcama_id**: Güncellenecek harcama ID
    - Tüm alanlar opsiyoneldir
    """
    return harcama_servisi.harcama_guncelle(db, sahiplik_harcama.id, harcama_guncelleme)


@router.delete("/{harcama_id}", summary="Harcama Kaydını Sil")
def harcama_sil(
    sahiplik_harcama: Harcamalar = Depends(harcama_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Belirtilen harcama kaydını siler (soft delete).
    
    - **harcama_id**: Silinecek harcama ID
    """
    return harcama_servisi.harcama_sil(db, sahiplik_harcama.id)


@router.get("/arac/{arac_id}/toplam", summary="Toplam Harcama")
def toplam_harcama(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın toplam harcamasını hesaplar.
    
    - **arac_id**: Araç ID
    """
    toplam = harcama_servisi.toplam_harcama_hesapla(db, sahiplik_arac.id)
    return {"arac_id": sahiplik_arac.id, "toplam_harcama": toplam}


@router.get("/arac/{arac_id}/kategori-analizi", response_model=HarcamaOzet, summary="Kategori Bazlı Analiz")
def kategori_analizi(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın harcamalarının kategori bazlı analizini yapar.
    
    - **arac_id**: Araç ID
    
    Returns: Kategori bazlı harcama dağılımı ve istatistikleri
    """
    return harcama_servisi.kategori_bazli_harcama(db, sahiplik_arac.id)
