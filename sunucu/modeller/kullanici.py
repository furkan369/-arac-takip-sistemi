"""
Kullanıcı Modeli
Kimlik doğrulama ve yetkilendirme için kullanıcı yapısı
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sunucu.veritabani import Base


class Kullanicilar(Base):
    """Kullanıcı modeli"""
    __tablename__ = "kullanicilar"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    ad_soyad = Column(String(255), nullable=False)
    sifre_hash = Column(String(255), nullable=False)
    aktif_mi = Column(Boolean, default=True)
    olusturulma_tarihi = Column(DateTime, default=datetime.now)
    guncellenme_tarihi = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    rol = Column(String(20), default="kullanici", nullable=False)  # 'admin' veya 'kullanici'
    
    # İlişkiler
    araclar = relationship("Araclar", back_populates="kullanici", cascade="all, delete-orphan")
