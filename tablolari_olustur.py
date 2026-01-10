"""
Tablo Oluşturma Script'i (Manuel)
"""
from sunucu.veritabani import Base, engine

# Tüm modelleri import et
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

# Tabloları kontrol et
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='369furki2929',
    database='arac_takip'
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")
tablolar = cursor.fetchall()

print("\n📋 Oluşturulmuş tablolar:")
for tablo in tablolar:
    print(f"   ✅ {tablo[0]}")

cursor.close()
conn.close()
