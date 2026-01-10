"""
Araclar Modeli
Kullanicinin sahip oldugu araclarin bilgilerini tutar.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sunucu.veritabani import Base


class Araclar(Base):
    """Araclar tablosu - Arac bilgilerini saklar"""
    
    __tablename__ = "araclar"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key - Kullanıcı İlişkisi
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=False, index=True, comment="Araç sahibi kullanıcı")
    
    # Arac Bilgileri
    plaka = Column(String(20), unique=True, nullable=False, index=True, comment="Arac plakasi")
    marka = Column(String(50), nullable=False, comment="Arac markasi")
    model = Column(String(50), nullable=False, comment="Arac modeli")
    yil = Column(Integer, comment="Model yili")
    renk = Column(String(30), comment="Arac rengi")
    km = Column(Integer, default=0, comment="Guncel kilometre")
    sase_no = Column(String(50), unique=True, comment="Sase numarasi")
    motor_no = Column(String(50), comment="Motor numarasi")
    notlar = Column(Text, comment="Ekstra notlar")
    
    # Durum Bilgileri
    aktif_mi = Column(Boolean, default=True, comment="Arac aktif mi?")
    silinmis_mi = Column(Boolean, default=False, index=True, comment="Soft delete bayragi")
    
    # Zaman Damgalari
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now(), comment="Olusturulma zamani")
    guncellenme_tarihi = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Guncellenme zamani")
    
    # Iliskiler (Many-to-One)
    kullanici = relationship("Kullanicilar", back_populates="araclar")
    
    # Iliskiler (One-to-Many)
    bakimlar = relationship("Bakimlar", back_populates="arac", cascade="all, delete-orphan")
    harcamalar = relationship("Harcamalar", back_populates="arac", cascade="all, delete-orphan")
    yakit_kayitlari = relationship("Yakit_Takibi", back_populates="arac", cascade="all, delete-orphan")
    hatirlaticilar = relationship("Hatirlaticilar", back_populates="arac", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Arac(id={self.id}, plaka='{self.plaka}', marka='{self.marka}', model='{self.model}')>"
