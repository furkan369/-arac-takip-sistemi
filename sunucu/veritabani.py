"""
Veritabani Baglanti Yonetimi
MySQL baglantisini kurar ve SQLAlchemy session yonetimini saglar.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sunucu.ayarlar import ayarlar


# Veritabani baglanti URL'i olustur
VERITABANI_URL = (
    f"mysql+mysqlconnector://{ayarlar.VERITABANI_KULLANICI}:"
    f"{ayarlar.VERITABANI_SIFRE}@{ayarlar.VERITABANI_SUNUCU}:"
    f"{ayarlar.VERITABANI_PORT}/{ayarlar.VERITABANI_ADI}"
    f"?charset=utf8mb4"
)

# SQLAlchemy engine olustur
engine = create_engine(
    VERITABANI_URL,
    pool_pre_ping=True,  # Baglanti sagligini kontrol et
    pool_recycle=3600,   # Her 1 saatte bir baglantilari yenile
    echo=ayarlar.HATA_AYIKLAMA_MODU  # SQL sorgularini logla
)

# Session factory olustur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model sinifi
Base = declarative_base()


def veritabani_baglantisi_al():
    """
    Veritabani baglantisi (session) olusturur ve yield ile dondurur.
    FastAPI dependency olarak kullanilir.
    
    Yields:
        Session: SQLAlchemy veritabani session'i
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def tablolari_olustur():
    """
    Tum veritabani tablolarini olusturur.
    Modeller import edildikten sonra calistirilmalidir.
    """
    # Tum modelleri import et
    from sunucu.modeller import arac, bakim, harcama, yakit_takibi, hatirlatici
    
    # Tablolari olustur
    Base.metadata.create_all(bind=engine)
    print("✅ Tum veritabani tablolari basariyla olusturuldu!")


if __name__ == "__main__":
    """
    Bu dosya direkt calistirildiginda tablolari olusturur.
    Kullanim: python sunucu/veritabani.py
    """
    print("Veritabani tablolari olusturuluyor...")
    tablolari_olustur()
