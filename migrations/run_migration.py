"""
Veritabanı Migration Script
Kullanıcı sistemi için tablo güncellemeleri
"""
import mysql.connector
from passlib.context import CryptContext

# Şifreleme contexti
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Veritabanı bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="arac_takip"
)

cursor = db.cursor()

print("🔧 Migration başlatılıyor...")

# 1. kullanicilar tablosunu oluştur
print("\n1️⃣ kullanicilar tablosu oluşturuluyor...")
create_table_sql = """
CREATE TABLE IF NOT EXISTS kullanicilar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    ad_soyad VARCHAR(255) NOT NULL,
    sifre_hash VARCHAR(255) NOT NULL,
    aktif_mi BOOLEAN DEFAULT TRUE,
    olusturulma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    guncellenme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci
"""
cursor.execute(create_table_sql)
print("✅ kullanicilar tablosu oluşturuldu")

# 2. Admin kullanıcısı oluştur
print("\n2️⃣ Admin kullanıcısı oluşturuluyor...")
admin_sifre = "admin123"
admin_hash = pwd_context.hash(admin_sifre)

insert_admin_sql = """
INSERT INTO kullanicilar (email, ad_soyad, sifre_hash, aktif_mi)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE ad_soyad = ad_soyad
"""
cursor.execute(insert_admin_sql, (
    'admin@aractakip.com',
    'Sistem Yöneticisi',
    admin_hash,
    True
))
print(f"✅ Admin kullanıcısı: admin@aractakip.com / {admin_sifre}")

# 3. araclar tablosuna kullanici_id sütunu ekle (eğer yoksa)
print("\n3️⃣ araclar tablosuna kullanici_id ekleniyor...")
try:
    cursor.execute("ALTER TABLE araclar ADD COLUMN kullanici_id INT")
    print("✅ kullanici_id sütunu eklendi")
except mysql.connector.Error as e:
    if "Duplicate column name" in str(e):
        print("⚠️  kullanici_id sütunu zaten mevcut")
    else:
        raise e

# 4. Index ekle
try:
    cursor.execute("ALTER TABLE araclar ADD INDEX idx_kullanici_id (kullanici_id)")
    print("✅ Index eklendi")
except mysql.connector.Error as e:
    if "Duplicate key name" in str(e):
        print("⚠️  Index zaten mevcut")
    else:
        raise e

# 5. Mevcut araçları admin'e ata
print("\n4️⃣ Mevcut araçlar admin kullanıcısına atanıyor...")
cursor.execute("""
    UPDATE araclar 
    SET kullanici_id = (SELECT id FROM kullanicilar WHERE email = 'admin@aractakip.com' LIMIT 1)
    WHERE kullanici_id IS NULL
""")
affected = cursor.rowcount
print(f"✅ {affected} araç admin kullanıcısına atandı")

# 6. kullanici_id'yi NOT NULL yap ve foreign key ekle
print("\n5️⃣ Foreign key oluşturuluyor...")
try:
    cursor.execute("ALTER TABLE araclar MODIFY COLUMN kullanici_id INT NOT NULL")
    print("✅ kullanici_id NOT NULL yapıldı")
except mysql.connector.Error as e:
    print(f"⚠️  NOT NULL constraint: {e}")

try:
    cursor.execute("""
        ALTER TABLE araclar 
        ADD CONSTRAINT fk_araclar_kullanici 
        FOREIGN KEY (kullanici_id) 
        REFERENCES kullanicilar(id) 
        ON DELETE CASCADE
    """)
    print("✅ Foreign key constraint eklendi")
except mysql.connector.Error as e:
    if "Duplicate foreign key" in str(e) or "already exists" in str(e):
        print("⚠️  Foreign key zaten mevcut")
    else:
        print(f"⚠️  Foreign key hatası: {e}")

# Commit
db.commit()

# Özet bilgi
print("\n" + "="*50)
print("📊 MIGRATION ÖZET")
print("="*50)

cursor.execute("SELECT COUNT(*) FROM kullanicilar")
kullanici_sayisi = cursor.fetchone()[0]
print(f"👥 Toplam Kullanıcı: {kullanici_sayisi}")

cursor.execute("SELECT COUNT(*) FROM araclar")
arac_sayisi = cursor.fetchone()[0]
print(f"🚗 Toplam Araç: {arac_sayisi}")

cursor.execute("SELECT email, ad_soyad FROM kullanicilar")
for email, ad in cursor.fetchall():
    print(f"   - {ad} ({email})")

print("\n✅ Migration başarıyla tamamlandı!")
print(f"\n🔑 Admin Giriş Bilgileri:")
print(f"   Email: admin@aractakip.com")
print(f"   Şifre: {admin_sifre}")

cursor.close()
db.close()
