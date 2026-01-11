"""
Tablo Oluşturma Script'i (Manuel)
"""
from sunucu.veritabani import Base, engine

# Tüm modelleri import et (Foreign key sırası önemli!)
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.arac import Araclar
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.yakit_takibi import Yakit_Takibi
from sunucu.modeller.hatirlatici import Hatirlaticilar

print("🔨 Veritabanı tabloları oluşturuluyor...")
print(f"   Bağlantı: {engine.url}")

# Tablolar oluşturulsun
Base.metadata.create_all(bind=engine)

print("\n✅ Tablolar başarıyla oluşturuldu!")
