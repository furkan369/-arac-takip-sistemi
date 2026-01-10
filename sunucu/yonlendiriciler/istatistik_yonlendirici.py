"""
İstatistik Yönlendirici
Grafik ve analiz endpoint'leri
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.servisler import istatistik_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.bagimliliklar.sahiplik import arac_sahipligini_dogrula
from sunucu.modeller.kullanici import Kullanicilar

router = APIRouter(prefix="/istatistikler", tags=["istatistikler"])


@router.get("/aylik-harcama", summary="Aylık Harcama Trendi")
def aylik_harcama_getir(
    arac_id: Optional[int] = Query(None, description="Araç ID (boş bırakılırsa tüm araçlar)"),
    ay_sayisi: int = Query(6, ge=1, le=24, description="Geriye dönük ay sayısı"),
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Son N ayın aylık toplam harcamalarını döndürür.
    Grafik için kullanılır.
    """
    # Eğer arac_id varsa, kullanıcının o araca yetkisi var mı kontrol et
    # Admin ise bypass edilir
    if arac_id:
        arac_sahipligini_dogrula(arac_id, db, kullanici)
        
    return istatistik_servisi.aylik_harcama_trendi(db, kullanici.id, arac_id, ay_sayisi, kullanici.rol)


@router.get("/kategori-dagilim", summary="Kategori Bazlı Harcama Dağılımı")
def kategori_dagilim_getir(
    arac_id: Optional[int] = Query(None, description="Araç ID"),
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Harcama kategorilerinin toplam tutarı ve yüzdelik dağırımı.
    Pasta grafik için kullanılır.
    """
    if arac_id:
        arac_sahipligini_dogrula(arac_id, db, kullanici)
        
    return istatistik_servisi.kategori_dagilimi(db, kullanici.id, arac_id, kullanici.rol)


@router.get("/yakit-tuketim", summary="Yakıt Tüketim Analizi")
def yakit_tuketim_getir(
    arac_id: int = Query(..., description="Araç ID"),
    ay_sayisi: int = Query(12, ge=1, le=24, description="Geriye dönük ay sayısı"),
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Aylık yakıt tüketimi, toplam tutar ve ortalama fiyat.
    Çizgi/sütun grafik için kullanılır.
    """
    # Araç sahipliğini doğrula
    arac_sahipligini_dogrula(arac_id, db, kullanici)
    
    return istatistik_servisi.yakit_tuketim_analizi(db, arac_id, ay_sayisi)


@router.get("/arac-karsilastirma", summary="Araçlar Arası Maliyet Karşılaştırması")
def arac_karsilastirma_getir(
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Tüm araçların toplam maliyetlerini karşılaştırır.
    Sütun grafik için kullanılır.
    """
    return istatistik_servisi.arac_karsilastirma(db, kullanici.id, kullanici.rol)


@router.get("/bakim-takip/{arac_id}", summary="Bakım Takip Göstergesi")
def bakim_takip_getir(
    arac_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """
    Bakıma kalan kilometre ve oran bilgisi.
    Kadran (gauge) grafik için kullanılır.
    """
    arac_sahipligini_dogrula(arac_id, db, kullanici)
    return istatistik_servisi.bakim_takip_gostergesi(db, arac_id)
