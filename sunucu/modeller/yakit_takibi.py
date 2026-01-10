"""
Yakit Takibi Modeli
Yakit alma kayitlarini ve tuketim verilerini tutar.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sunucu.veritabani import Base


class Yakit_Takibi(Base):
    """Yakit_Takibi tablosu - Yakit tuketim kayitlarini saklar"""
    
    __tablename__ = "yakit_takibi"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    arac_id = Column(Integer, ForeignKey("araclar.id", ondelete="CASCADE"), nullable=False, index=True, comment="Arac ID")
    
    # Yakit Bilgileri
    tarih = Column(Date, nullable=False, index=True, comment="Yakit alma tarihi")
    km = Column(Integer, nullable=False, comment="Yakit alma sirasindaki kilometre")
    litre = Column(Numeric(8, 2), nullable=False, comment="Alinan yakit miktari")
    fiyat = Column(Numeric(8, 2), nullable=False, comment="Litre basina fiyat")
    toplam_tutar = Column(Numeric(10, 2), nullable=False, comment="Toplam maliyet")
    yakit_turu = Column(String(20), nullable=False, comment="Yakit turu (Benzin, Dizel, LPG, Elektrik)")
    istasyon = Column(String(100), comment="Yakit istasyonu")
    tam_depo = Column(Boolean, default=False, comment="Depo dolu mu?")
    
    # Hesaplanan Degerler
    ortalama_tuketim = Column(Numeric(5, 2), comment="Hesaplanan ortalama tuketim (L/100km)")
    notlar = Column(Text, comment="Ekstra notlar")
    
    # Durum Bilgileri
    silinmis_mi = Column(Boolean, default=False, index=True, comment="Soft delete bayragi")
    
    # Zaman Damgalari
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now(), comment="Olusturulma zamani")
    guncellenme_tarihi = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Guncellenme zamani")
    
    # Iliskiler (Many-to-One)
    arac = relationship("Araclar", back_populates="yakit_kayitlari")
    
    def __repr__(self):
        return f"<YakitKaydi(id={self.id}, arac_id={self.arac_id}, yakit_turu='{self.yakit_turu}', litre={self.litre})>"
