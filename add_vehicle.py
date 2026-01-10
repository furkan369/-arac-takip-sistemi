from sunucu.veritabani import SessionLocal
from sunucu.modeller.arac import Araclar
from sunucu.modeller.kullanici import Kullanicilar

def add_customer_vehicle():
    db = SessionLocal()
    try:
        # ID:4 yani Müşteri için araç ekle
        yeni_arac = Araclar(
            plaka="34MUSTERI99",
            marka="Fiat",
            model="Egea",
            yil=2023,
            renk="Beyaz",
            kullanici_id=4,  # Test Müşteri
            aktif_mi=True,
            silinmis_mi=False
        )
        db.add(yeni_arac)
        db.commit()
        print(f"✅ Müşteri aracı eklendi: 34MUSTERI99 (Sahip ID: 4)")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_customer_vehicle()
