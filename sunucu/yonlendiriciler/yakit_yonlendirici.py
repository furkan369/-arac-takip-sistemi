"""
Yakıt Yönlendirici
Yakıt takip kayıtları ile ilgili API endpoint'lerini içerir.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.semalar.yakit_sema import YakitOlustur, YakitGuncelle, YakitYanit, TuketimAnalizi, IstasyonAnalizi
from sunucu.servisler import yakit_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.bagimliliklar.sahiplik import arac_sahipligini_dogrula, yakit_sahipligini_dogrula
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.yakit_takibi import Yakit_Takibi as YakitKayitlari
from sunucu.modeller.arac import Araclar


# Router oluştur
router = APIRouter()


@router.post("/", response_model=YakitYanit, status_code=201, summary="Yeni Yakıt Kaydı Ekle")
def yakit_kaydi_olustur(
    yakit: YakitOlustur,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Yeni bir yakıt kaydı oluşturur.
    Sadece yetkili olunan araçlar için kayıt eklenebilir.
    
    - **arac_id**: Araç ID (zorunlu)
    - **tarih**: Yakıt alma tarihi (zorunlu)
    - **km**: Kilometredeki değer (zorunlu)
    - **litre**: Alınan yakıt miktarı (zorunlu)
    - **fiyat**: Litre başına fiyat (zorunlu)
    - **toplam_tutar**: Toplam maliyet (zorunlu)
    - **yakit_turu**: Yakıt türü (zorunlu)
    - **istasyon**: Yakıt istasyonu (opsiyonel)
    - **tam_depo**: Depo tamamen dolduruldu mu? (opsiyonel)
    """
    # Araç sahipliğini doğrula
    arac_sahipligini_dogrula(yakit.arac_id, db, kullanici)
    
    return yakit_servisi.yakit_kaydi_olustur(db, yakit)


@router.get("/{yakit_id}", response_model=YakitYanit, summary="Yakıt Kaydı Detaylarını Getir")
def yakit_detayi_getir(
    yakit: YakitKayitlari = Depends(yakit_sahipligini_dogrula)
):
    """
    Belirtilen ID'ye sahip yakıt kaydının detaylarını getirir.
    
    - **yakit_id**: Yakıt kaydı ID
    """
    return yakit


@router.get("/arac/{arac_id}", response_model=List[YakitYanit], summary="Araç Yakıt Kayıtlarını Listele")
def arac_yakit_kayitlari(
    arac_id: int,
    atlama: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(veritabani_baglantisi_al),
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula)
):
    """
    Belirli bir aracın tüm yakıt kayıtlarını listeler.
    Sadece yetkili olunan araçlar için.
    
    - **arac_id**: Araç ID
    - **atlama**: Pagination için atlanacak kayıt sayısı
    - **limit**: Maksimum kayıt sayısı
    """
    return yakit_servisi.arac_yakit_kayitlari_getir(db, sahiplik_arac.id, atlama, limit)


@router.put("/{yakit_id}", response_model=YakitYanit, summary="Yakıt Kaydını Güncelle")
def yakit_guncelle(
    yakit_guncelleme: YakitGuncelle,
    sahiplik_yakit: YakitKayitlari = Depends(yakit_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Mevcut bir yakıt kaydını günceller.
    
    - **yakit_id**: Güncellenecek yakıt kaydı ID
    - Tüm alanlar opsiyoneldir
    """
    return yakit_servisi.yakit_kaydi_guncelle(db, sahiplik_yakit.id, yakit_guncelleme)


@router.delete("/{yakit_id}", summary="Yakıt Kaydını Sil")
def yakit_sil(
    sahiplik_yakit: YakitKayitlari = Depends(yakit_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Belirtilen yakıt kaydını siler (soft delete).
    
    - **yakit_id**: Silinecek yakıt kaydı ID
    """
    return yakit_servisi.yakit_kaydi_sil(db, sahiplik_yakit.id)


@router.get("/arac/{arac_id}/tuketim-analizi", response_model=TuketimAnalizi, summary="Yakıt Tüketim Analizi")
def tuketim_analizi(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Aracın yakıt tüketim analizini yapar.
    
    - **arac_id**: Araç ID
    
    Returns: Ortalama tüketim, toplam yakıt, toplam harcama vb.
    """
    return yakit_servisi.ortalama_tuketim_hesapla(db, sahiplik_arac.id)


@router.get("/arac/{arac_id}/istasyon-analizi", response_model=List[IstasyonAnalizi], summary="İstasyon Bazlı Analiz")
def istasyon_analiz(
    sahiplik_arac: Araclar = Depends(arac_sahipligini_dogrula),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    İstasyon bazlı yakıt fiyat ve tüketim analizini yapar.
    
    - **arac_id**: Araç ID
    
    Returns: Her istasyonun ortalama fiyat ve toplam litre bilgisi
    """
    return yakit_servisi.istasyon_analizi(db, sahiplik_arac.id)
