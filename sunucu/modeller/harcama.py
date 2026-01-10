"""
Harcamalar Modeli
Aracla ilgili genel harcamalari tutar.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sunucu.veritabani import Base


class Harcamalar(Base):
    """Harcamalar tablosu - Genel harcama kayitlarini saklar"""
    
    __tablename__ = "harcamalar"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    arac_id = Column(Integer, ForeignKey("araclar.id", ondelete="CASCADE"), nullable=False, index=True, comment="Arac ID")
    
    # Harcama Bilgileri
    kategori = Column(String(50), nullable=False, index=True, comment="Harcama kategorisi (Sigorta, MTV, Otopark, Ceza)")
    tarih = Column(Date, nullable=False, index=True, comment="Harcama tarihi")
    tutar = Column(Numeric(10, 2), nullable=False, comment="Harcama miktari")
    aciklama = Column(Text, comment="Harcama detaylari")
    fis_no = Column(String(50), comment="Fis/Fatura numarasi")
    
    # Durum Bilgileri
    silinmis_mi = Column(Boolean, default=False, index=True, comment="Soft delete bayragi")
    
    # Zaman Damgalari
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now(), comment="Olusturulma zamani")
    guncellenme_tarihi = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Guncellenme zamani")
    
    # Iliskiler (Many-to-One)
    arac = relationship("Araclar", back_populates="harcamalar")
    
    def __repr__(self):
        return f"<Harcama(id={self.id}, arac_id={self.arac_id}, kategori='{self.kategori}', tutar={self.tutar})>"
