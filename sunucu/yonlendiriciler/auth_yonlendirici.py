"""
Authentication Router
Kullanıcı kaydı ve giriş endpoint'leri
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.semalar.kullanici_sema import (
    KullaniciOlustur, 
    KullaniciYanit, 
    TokenYanit, 
    GirisGirdi,
    KullaniciGuncelle,
    SifreDegistir
)
from sunucu.servisler import auth_servisi
from sunucu.bagimliliklar.auth import mevcut_kullanici_al
from sunucu.modeller.kullanici import Kullanicilar

router = APIRouter(prefix="/auth", tags=["Kimlik Doğrulama"])


@router.post("/kayit", response_model=KullaniciYanit, status_code=status.HTTP_201_CREATED, summary="Kullanıcı Kaydı")
def kayit_ol(
    kullanici: KullaniciOlustur, 
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Yeni kullanıcı kaydı oluşturur.
    
    - **email**: Benzersiz email adresi
    - **ad_soyad**: Kullanıcının adı soyadı
    - **sifre**: Güvenli şifre (en az 8 karakter önerilir)
    """
    # Email kontrolü
    mevcut = db.query(Kullanicilar).filter(Kullanicilar.email == kullanici.email).first()
    if mevcut:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu e-posta adresi zaten kayıtlı"
        )
    
    # Şifre uzunluk kontrolü
    if len(kullanici.sifre) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Şifre en az 6 karakter olmalıdır"
        )
    
    # Kullanıcı oluştur
    return auth_servisi.kullanici_kaydet(
        db, 
        kullanici.email, 
        kullanici.ad_soyad, 
        kullanici.sifre
    )


@router.post("/giris", response_model=TokenYanit, summary="Kullanıcı Girişi")
def giris_yap(
    giris: GirisGirdi, 
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Kullanıcı girişi yapar ve JWT access token döndürür.
    
    - **email**: Kayıtlı email adresi
    - **sifre**: Kullanıcı şifresi
    
    Başarılı girişte `access_token` döner. Bu token Authorization header'ında kullanılmalıdır:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    kullanici = auth_servisi.kullanici_dogrula(db, giris.email, giris.sifre)
    
    if not kullanici:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token oluştur
    access_token = auth_servisi.token_olustur({"sub": kullanici.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "rol": kullanici.rol
    }


@router.get("/me", response_model=KullaniciYanit, summary="Mevcut Kullanıcı Bilgileri")
def mevcut_kullanici_getir(
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
):
    """Giriş yapmış kullanıcının bilgilerini döndürür."""
    return kullanici


@router.put("/me", response_model=KullaniciYanit, summary="Bilgileri Güncelle")
def bilgileri_guncelle(
    veri: KullaniciGuncelle,
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Kullanıcının profil bilgilerini (Ad Soyad) günceller.
    Email değişimi şimdilik desteklenmemektedir (güvenlik nedeniyle).
    """
    return auth_servisi.kullanici_guncelle(db, kullanici, veri.ad_soyad)


@router.put("/sifre-degistir", status_code=status.HTTP_204_NO_CONTENT, summary="Şifre Değiştir")
def sifre_degistir(
    veri: SifreDegistir,
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al),
    db: Session = Depends(veritabani_baglantisi_al)
):
    """
    Kullanıcının şifresini değiştirir.
    Eski şifre doğrulanmalıdır.
    """
    if not auth_servisi.sifre_dogrula(veri.eski_sifre, kullanici.sifre_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Eski şifre hatalı"
        )
        
    auth_servisi.sifre_degistir(db, kullanici, veri.yeni_sifre)
    return None
