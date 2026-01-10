"""
MySQL Tablo Kontrol ve Oluşturma
"""
import mysql.connector

try:
    # MySQL'e bağlan
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='369furki2929',
        database='arac_takip'
    )
    
    cursor = conn.cursor()
    
    # Mevcut tabloları göster
    print("📋 Mevcut tablolar:")
    cursor.execute("SHOW TABLES")
    tablolar = cursor.fetchall()
    
    if tablolar:
        for tablo in tablolar:
            print(f"  - {tablo[0]}")
    else:
        print("  ❌ Hiç tablo yok!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
