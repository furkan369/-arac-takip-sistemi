"""
Araç Sahiplik Kontrolü - Dependency Injection
FastAPI dependency fonksiyonları ile temiz ve modüler sahiplik kontrolü
"""
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sunucu.modeller.arac import Araclar
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.yakit_takibi import Yakit_Takibi as YakitKayitlari
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.bagimliliklar.auth import mevcut_kullanici_al


def arac_sahipligini_dogrula(
    arac_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
) -> Araclar:
    """
    Araç sahipliğini doğrula
    
    Args:
        arac_id: Araç ID
        db: Veritabanı oturumu
        kullanici: Mevcut kullanıcı (JWT'den)
    
    Returns:
        Araclar: Doğrulanmış araç objesi
        
    Raises:
        HTTPException: 404 araç bulunamadı, 403 yetkisiz erişim
    """
    arac = db.query(Araclar).filter(Araclar.id == arac_id).first()
    
    if not arac:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Araç bulunamadı"
        )
    
    # Yönetici ise erişebilir
    if kullanici.rol == 'admin':
        return arac
    
    if arac.kullanici_id != kullanici.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu araca erişim yetkiniz yok"
        )
    
    return arac


def bakim_sahipligini_dogrula(
    bakim_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
) -> Bakimlar:
    """
    Bakım kaydı sahipliğini doğrula (araç üzerinden)
    """
    bakim = db.query(Bakimlar).filter(Bakimlar.id == bakim_id).first()
    
    if not bakim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bakım kaydı bulunamadı"
        )
    
    # Bakımın ait olduğu aracı kontrol et
    arac = db.query(Araclar).filter(Araclar.id == bakim.arac_id).first()
    
    # Yönetici ise erişebilir
    if kullanici.rol == 'admin':
        return bakim
    
    if not arac or arac.kullanici_id != kullanici.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu bakım kaydına erişim yetkiniz yok"
        )
    
    return bakim


def harcama_sahipligini_dogrula(
    harcama_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
) -> Harcamalar:
    """
    Harcama kaydı sahipliğini doğrula (araç üzerinden)
    """
    harcama = db.query(Harcamalar).filter(Harcamalar.id == harcama_id).first()
    
    if not harcama:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Harcama kaydı bulunamadı"
        )
    
    # Harcamanın ait olduğu aracı kontrol et
    arac = db.query(Araclar).filter(Araclar.id == harcama.arac_id).first()
    
    # Yönetici ise erişebilir
    if kullanici.rol == 'admin':
        return harcama
        
    if not arac or arac.kullanici_id != kullanici.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu harcama kaydına erişim yetkiniz yok"
        )
    
    return harcama


def yakit_sahipligini_dogrula(
    yakit_id: int,
    db: Session = Depends(veritabani_baglantisi_al),
    kullanici: Kullanicilar = Depends(mevcut_kullanici_al)
) -> YakitKayitlari:
    """
    Yakıt kaydı sahipliğini doğrula (araç üzerinden)
    """
    yakit = db.query(YakitKayitlari).filter(YakitKayitlari.id == yakit_id).first()
    
    if not yakit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yakıt kaydı bulunamadı"
        )
    
    # Yakıt kaydının ait olduğu aracı kontrol et
    arac = db.query(Araclar).filter(Araclar.id == yakit.arac_id).first()
    
    # Yönetici ise erişebilir
    if kullanici.rol == 'admin':
        return yakit
        
    if not arac or arac.kullanici_id != kullanici.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu yakıt kaydına erişim yetkiniz yok"
        )
    
    return yakit
