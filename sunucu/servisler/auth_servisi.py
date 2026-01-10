"""
Authentication Servisleri
Şifre hashing, JWT token oluşturma ve kullanıcı doğrulama
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.ayarlar import ayarlar


def sifre_hashle(sifre: str) -> str:
    """Şifreyi bcrypt ile hashler"""
    # String'i bytes'a çevir
    sifre_bytes = sifre.encode('utf-8')
    # Hash oluştur
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(sifre_bytes, salt)
    # Bytes'ı stringe çevir (veritabanı için)
    return hash_bytes.decode('utf-8')


def sifre_dogrula(duz_sifre: str, hash_sifre: str) -> bool:
    """Şifre doğrulama"""
    try:
        duz_sifre_bytes = duz_sifre.encode('utf-8')
        hash_sifre_bytes = hash_sifre.encode('utf-8')
        return bcrypt.checkpw(duz_sifre_bytes, hash_sifre_bytes)
    except Exception:
        return False


def token_olustur(data: dict) -> str:
    """JWT access token oluşturur"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ayarlar.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, ayarlar.SECRET_KEY, algorithm=ayarlar.ALGORITHM)
    return encoded_jwt


def token_dogrula(token: str) -> dict:
    """JWT token doğrulama ve payload çıkarma"""
    try:
        payload = jwt.decode(token, ayarlar.SECRET_KEY, algorithms=[ayarlar.ALGORITHM])
        return payload
    except Exception:
        return None


def kullanici_kaydet(db: Session, email: str, ad_soyad: str, sifre: str) -> Kullanicilar:
    """Yeni kullanıcı kaydı"""
    sifre_hash = sifre_hashle(sifre)
    kullanici = Kullanicilar(
        email=email,
        ad_soyad=ad_soyad,
        sifre_hash=sifre_hash
    )
    db.add(kullanici)
    db.commit()
    db.refresh(kullanici)
    return kullanici


def kullanici_dogrula(db: Session, email: str, sifre: str) -> Kullanicilar | None:
    """Kullanıcı doğrulama (email + şifre)"""
    kullanici = db.query(Kullanicilar).filter(Kullanicilar.email == email).first()
    if not kullanici:
        return None
    if not sifre_dogrula(sifre, kullanici.sifre_hash):
        return None
    if not kullanici.aktif_mi:
        return None
    return kullanici


def email_ile_kullanici_getir(db: Session, email: str) -> Kullanicilar | None:
    """Email ile kullanıcı getir"""
    return db.query(Kullanicilar).filter(Kullanicilar.email == email).first()


def kullanici_guncelle(db: Session, db_kullanici: Kullanicilar, ad_soyad: str) -> Kullanicilar:
    """Kullanıcı bilgilerini günceller"""
    db_kullanici.ad_soyad = ad_soyad
    db.commit()
    db.refresh(db_kullanici)
    return db_kullanici


def sifre_degistir(db: Session, db_kullanici: Kullanicilar, yeni_sifre: str) -> None:
    """Kullanıcı şifresini günceller"""
    db_kullanici.sifre_hash = sifre_hashle(yeni_sifre)
    db.commit()
