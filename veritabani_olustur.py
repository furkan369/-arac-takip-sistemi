"""
Veritabani Olusturma Yardimci Script'i
MySQL'de arac_takip veritabanini olusturur.
"""
import mysql.connector
from mysql.connector import Error

def veritabani_olustur():
    """MySQL'de arac_takip veritabanini olusturur."""
    try:
        # Root kullanici ile baglan (veritabani secmeden)
        print("MySQL'e baglaniliyor...")
        baglanti = mysql.connector.connect(
            host='localhost',
            user='root',
            password=input("MySQL root sifresi: ")
        )
        
        if baglanti.is_connected():
            cursor = baglanti.cursor()
            
            # Veritabani olustur
            print("\nVeritabani olusturuluyor...")
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS arac_takip "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print("✅ Veritabani 'arac_takip' basariyla olusturuldu!")
            
            # Veritabani listesini goster
            cursor.execute("SHOW DATABASES")
            print("\nMevcut veritabanlari:")
            for db in cursor.fetchall():
                print(f"  - {db[0]}")
            
            cursor.close()
            baglanti.close()
            print("\n✅ Islem tamamlandi!")
            
    except Error as e:
        print(f"❌ Hata olustu: {e}")
    finally:
        if baglanti and baglanti.is_connected():
            baglanti.close()

if __name__ == "__main__":
    veritabani_olustur()
