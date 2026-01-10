"""
Authentication Dependencies
JWT token doğrulama ve kullanıcı bilgisi çıkarma
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.servisler.auth_servisi import token_dogrula, email_ile_kullanici_getir

# OAuth2 scheme - token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/giris")


async def mevcut_kullanici_al(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(veritabani_baglantisi_al)
) -> Kullanicilar:
    """
    Token'dan kullanıcı bilgisi çıkarır.
    Korumalı endpoint'lerde dependency olarak kullanılır.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulanamadı",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Token doğrulama
    payload = token_dogrula(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Kullanıcıyı veritabanından getir
    kullanici = email_ile_kullanici_getir(db, email=email)
    if kullanici is None:
        raise credentials_exception
    
    if not kullanici.aktif_mi:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kullanıcı hesabı devre dışı"
        )
    
    return kullanici
