"""
Bakimlar Modeli
Araclarin bakim kayitlarini tutar.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sunucu.veritabani import Base


class Bakimlar(Base):
    """Bakimlar tablosu - Bakim kayitlarini saklar"""
    
    __tablename__ = "bakimlar"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    arac_id = Column(Integer, ForeignKey("araclar.id", ondelete="CASCADE"), nullable=False, index=True, comment="Arac ID")
    
    # Bakim Bilgileri
    bakim_turu = Column(String(100), nullable=False, comment="Bakim turu (Yag Degisimi, Filtre, Fren)")
    tarih = Column(Date, nullable=False, index=True, comment="Bakim tarihi")
    km = Column(Integer, nullable=False, comment="Bakim sirasindaki kilometre")
    tutar = Column(Numeric(10, 2), default=0, comment="Bakim maliyeti")
    servis_yeri = Column(String(100), comment="Bakimin yapildigi yer")
    aciklama = Column(Text, comment="Bakim detaylari")
    
    # Gelecek Bakim Bilgileri
    sonraki_bakim_km = Column(Integer, comment="Bir sonraki bakim kilometresi")
    sonraki_bakim_tarih = Column(Date, comment="Bir sonraki bakim tahmini tarihi")
    
    # Durum Bilgileri
    silinmis_mi = Column(Boolean, default=False, index=True, comment="Soft delete bayragi")
    
    # Zaman Damgalari
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now(), comment="Olusturulma zamani")
    guncellenme_tarihi = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Guncellenme zamani")
    
    # Iliskiler (Many-to-One)
    arac = relationship("Araclar", back_populates="bakimlar")
    
    def __repr__(self):
        return f"<Bakim(id={self.id}, arac_id={self.arac_id}, bakim_turu='{self.bakim_turu}', tarih='{self.tarih}')>"
