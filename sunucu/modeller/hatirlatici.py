"""
Hatirlaticilar Modeli
Gelecek bakim ve islemler icin hatirlaticilar tutar.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sunucu.veritabani import Base


class Hatirlaticilar(Base):
    """Hatirlaticilar tablosu - Gelecek bakim ve islem hatirlaticilarini saklar"""
    
    __tablename__ = "hatirlaticilar"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    arac_id = Column(Integer, ForeignKey("araclar.id", ondelete="CASCADE"), nullable=False, index=True, comment="Arac ID")
    
    # Hatirlatici Bilgileri
    baslik = Column(String(100), nullable=False, comment="Hatirlatici basligi")
    aciklama = Column(Text, comment="Hatirlatici detaylari")
    hedef_tarih = Column(Date, index=True, comment="Hedef tarih")
    hedef_km = Column(Integer, comment="Hedef kilometre")
    oncelik = Column(String(20), default="Normal", comment="Oncelik seviyesi (Dusuk, Normal, Yuksek, Acil)")
    durum = Column(String(20), default="Bekliyor", index=True, comment="Hatirlatici durumu (Bekliyor, Tamamlandi, Iptal)")
    tamamlanma_tarihi = Column(DateTime(timezone=True), comment="Tamamlanma tarihi")
    
    # Durum Bilgileri
    silinmis_mi = Column(Boolean, default=False, index=True, comment="Soft delete bayragi")
    
    # Zaman Damgalari
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now(), comment="Olusturulma zamani")
    guncellenme_tarihi = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Guncellenme zamani")
    
    # Iliskiler (Many-to-One)
    arac = relationship("Araclar", back_populates="hatirlaticilar")
    
    def __repr__(self):
        return f"<Hatirlatici(id={self.id}, arac_id={self.arac_id}, baslik='{self.baslik}', durum='{self.durum}')>"
