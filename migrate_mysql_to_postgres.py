"""
MySQL to PostgreSQL Data Migration Script
Transfers all data from local MySQL to Render PostgreSQL
"""
import pymysql
import psycopg2
from psycopg2.extras import execute_values
import sys

# ===== BAĞLANTI BİLGİLERİ =====

# LOCAL MySQL (Kaynak)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '369furki2929',
    'database': 'arac_takip'
}

# RENDER PostgreSQL (Hedef)
POSTGRES_URL = "postgresql://arac_user:a0A7Ay+mpNwvCeEEj6KNdAzBPf3VcNAA1adpg@dpg-d5h35ushg0os73fn3qe0-a:5432/arac_takip_db"

# ===== YARDIMCI FONKSİYONLAR =====

def mysql_connection():
    """MySQL bağlantısı oluştur"""
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ MySQL bağlantısı başarılı")
        return conn
    except Exception as e:
        print(f"❌ MySQL bağlantı hatası: {e}")
        sys.exit(1)

def postgres_connection():
    """PostgreSQL bağlantısı oluştur"""
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        print("✅ PostgreSQL bağlantısı başarılı")
        return conn
    except Exception as e:
        print(f"❌ PostgreSQL bağlantı hatası: {e}")
        sys.exit(1)

def migrate_table(mysql_cur, pg_cur, table_name, columns, id_mapping=None):
    """
    Bir tabloyu MySQL'den PostgreSQL'e kopyala
    
    Args:
        mysql_cur: MySQL cursor
        pg_cur: PostgreSQL cursor
        table_name: Tablo adı
        columns: Sütun listesi
        id_mapping: Foreign key için ID mapping (optional)
    """
    print(f"\n📊 {table_name} tablosu migrate ediliyor...")
    
    # MySQL'den veri oku
    mysql_cur.execute(f"SELECT * FROM {table_name}")
    rows = mysql_cur.fetchall()
    
    if not rows:
        print(f"   ⚠️  {table_name} tablosu boş, atlanıyor")
        return {}
    
    print(f"   📦 {len(rows)} kayıt bulundu")
    
    # PostgreSQL'e insert
    placeholders = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING id"
    
    new_id_mapping = {}
    inserted_count = 0
    
    for row in rows:
        try:
            # Veriyi hazırla
            data = list(row)
            old_id = data[0]  # İlk sütun ID olduğunu varsayıyoruz
            
            # Foreign key güncellemesi (eğer varsa)
            if id_mapping:
                # Örnek: kullanici_id güncellemesi
                if 'kullanici_id' in columns:
                    idx = columns.index('kullanici_id')
                    if data[idx] in id_mapping:
                        data[idx] = id_mapping[data[idx]]
            
            # ID sütununu kaldır (PostgreSQL otomatik oluşturacak)
            data_without_id = data[1:]
            columns_without_id = columns[1:]
            
            # Insert et
            placeholders = ', '.join(['%s'] * len(columns_without_id))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns_without_id)}) VALUES ({placeholders}) RETURNING id"
            
            pg_cur.execute(insert_query, data_without_id)
            new_id = pg_cur.fetchone()[0]
            
            # ID mapping kaydet
            new_id_mapping[old_id] = new_id
            inserted_count += 1
            
        except Exception as e:
            print(f"   ❌ Kayıt eklenemedi (ID: {old_id}): {e}")
            continue
    
    print(f"   ✅ {inserted_count}/{len(rows)} kayıt başarıyla eklendi")
    return new_id_mapping

# ===== ANA MİGRATİON FONKSİYONU =====

def main():
    print("=" * 60)
    print("🚀 MySQL → PostgreSQL Data Migration")
    print("=" * 60)
    
    # Bağlantıları oluştur
    mysql_conn = mysql_connection()
    pg_conn = postgres_connection()
    
    mysql_cur = mysql_conn.cursor()
    pg_cur = pg_conn.cursor()
    
    try:
        print("\n🔄 Migration başlıyor...\n")
        
        # 1. KULLANICILAR (Parent table)
        user_mapping = migrate_table(
            mysql_cur, pg_cur,
            table_name='kullanicilar',
            columns=['id', 'email', 'ad_soyad', 'sifre_hash', 'aktif_mi', 
                    'olusturulma_tarihi', 'guncellenme_tarihi', 'rol']
        )
        
        # 2. ARAÇLAR (kullanici_id FK)
        arac_mapping = migrate_table(
            mysql_cur, pg_cur,
            table_name='araclar',
            columns=['id', 'kullanici_id', 'marka', 'model', 'yil', 'plaka', 
                    'renk', 'motor_hacmi', 'yakit_tipi', 'vites_tipi', 
                    'kilometre', 'sase_no', 'motor_no', 'notlar', 
                    'aktif_mi', 'olusturulma_tarihi', 'guncellenme_tarihi'],
            id_mapping=user_mapping
        )
        
        # 3. BAKIMLAR (arac_id FK)
        migrate_table(
            mysql_cur, pg_cur,
            table_name='bakimlar',
            columns=['id', 'arac_id', 'bakim_tipi', 'aciklama', 'tarih', 
                    'kilometre', 'tutar', 'servis_adi', 'sonraki_bakim_km', 
                    'sonraki_bakim_tarih', 'notlar', 'olusturulma_tarihi', 
                    'guncellenme_tarihi'],
            id_mapping={'arac_id': arac_mapping}
        )
        
        # 4. HARCAMALAR (arac_id FK)
        migrate_table(
            mysql_cur, pg_cur,
            table_name='harcamalar',
            columns=['id', 'arac_id', 'kategori', 'aciklama', 'tutar', 
                    'tarih', 'notlar', 'olusturulma_tarihi', 
                    'guncellenme_tarihi'],
            id_mapping={'arac_id': arac_mapping}
        )
        
        # 5. YAKIT TAKİBİ (arac_id FK)
        migrate_table(
            mysql_cur, pg_cur,
            table_name='yakit_takibi',
            columns=['id', 'arac_id', 'tarih', 'litre', 'tutar', 
                    'birim_fiyat', 'kilometre', 'tam_depo', 'istasyon', 
                    'notlar', 'olusturulma_tarihi', 'guncellenme_tarihi'],
            id_mapping={'arac_id': arac_mapping}
        )
        
        # 6. HATIRLATICILAR (arac_id FK)
        migrate_table(
            mysql_cur, pg_cur,
            table_name='hatirlaticilar',
            columns=['id', 'arac_id', 'baslik', 'aciklama', 'tarih', 
                    'kilometre', 'hatirlatici_tipi', 'tamamlandi_mi', 
                    'olusturulma_tarihi', 'guncellenme_tarihi'],
            id_mapping={'arac_id': arac_mapping}
        )
        
        # Commit yap
        pg_conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration başarıyla tamamlandı!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Migration sırasında hata: {e}")
        pg_conn.rollback()
        raise
        
    finally:
        mysql_cur.close()
        pg_cur.close()
        mysql_conn.close()
        pg_conn.close()
        print("\n🔒 Bağlantılar kapatıldı")

if __name__ == "__main__":
    print("\n⚠️  DİKKAT: Bu script local MySQL verilerinizi Render PostgreSQL'e kopyalayacak!")
    confirm = input("Devam etmek istiyor musunuz? (evet/hayir): ")
    
    if confirm.lower() in ['evet', 'e', 'yes', 'y']:
        main()
    else:
        print("❌ Migration iptal edildi")
