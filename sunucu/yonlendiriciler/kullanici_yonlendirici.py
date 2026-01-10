"""
Kullanıcı Yönetimi Router (Admin)
Sadece admin yetkisi ile erişilebilen kullanıcı yönetimi işlemleri.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.semalar.kullanici_sema import KullaniciYanit, AdminKullaniciOlustur
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.servisler.auth_servisi import kullanici_kaydet, sifre_hashle

router = APIRouter(prefix="/kullanicilar", tags=["Kullanıcı Yönetimi (Admin)"])

def admin_dogrula(kullanici: Kullanicilar = Depends(mevcut_kullanici_al)):
    """Sadece 'admin' rolüne sahip kullanıcıların erişimine izin verir."""
    if kullanici.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlem için yönetici yetkisi gerekiyor"
        )
    return kullanici

@router.get("/", response_model=List[KullaniciYanit], summary="Tüm Kullanıcıları Listele")
def kullanicilari_getir(
    db: Session = Depends(veritabani_baglantisi_al),
    _: Kullanicilar = Depends(admin_dogrula)
):
    """
    Sisteme kayıtlı tüm kullanıcıları listeler.
    Sadece Admin erişebilir.
    """
    return db.query(Kullanicilar).all()

@router.post("/", response_model=KullaniciYanit, status_code=status.HTTP_201_CREATED, summary="Yeni Kullanıcı Ekle")
def kullanici_ekle(
    yeni_kullanici: AdminKullaniciOlustur,
    db: Session = Depends(veritabani_baglantisi_al),
    _: Kullanicilar = Depends(admin_dogrula)
):
    """
    Yönetici tarafından yeni kullanıcı oluşturur.
    Rol seçimi (admin/kullanici) yapılabilir.
    """
    # Email kontrolü
    mevcut = db.query(Kullanicilar).filter(Kullanicilar.email == yeni_kullanici.email).first()
    if mevcut:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu e-posta adresi zaten kayıtlı"
        )
    
    # Kullanıcı oluştur (manuel olarak model oluşturuyoruz çünkü servis rol parametresi almıyor olabilir)
    # Servis güncellenmemişse manuel ekleyelim, daha güvenli.
    
    db_kullanici = Kullanicilar(
        email=yeni_kullanici.email,
        ad_soyad=yeni_kullanici.ad_soyad,
        sifre_hash=sifre_hashle(yeni_kullanici.sifre),
        rol=yeni_kullanici.rol,
        aktif_mi=True
    )
    
    db.add(db_kullanici)
    db.commit()
    db.refresh(db_kullanici)
    
    return db_kullanici

@router.delete("/{kullanici_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Kullanıcıyı Sil")
def kullanici_sil(
    kullanici_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    mevcut_admin: Kullanicilar = Depends(admin_dogrula)
):
    """
    Belirtilen ID'ye sahip kullanıcıyı siler.
    Kendi hesabını silemez.
    """
    if kullanici_id == mevcut_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kendi hesabınızı silemezsiniz"
        )
        
    kullanici = db.query(Kullanicilar).filter(Kullanicilar.id == kullanici_id).first()
    if not kullanici:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı"
        )
        
    db.delete(kullanici)
    db.commit()
