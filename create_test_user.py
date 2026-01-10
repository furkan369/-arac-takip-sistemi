from sunucu.veritabani import SessionLocal
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.servisler.auth_servisi import sifre_hashle

def create_customer():
    db = SessionLocal()
    try:
        email = "musteri@test.com"
        # Önce var mı kontrol et
        existing = db.query(Kullanicilar).filter(Kullanicilar.email == email).first()
        if existing:
            print(f"✅ Kullanıcı zaten mevcut: {email}")
            return

        yeni_kullanici = Kullanicilar(
            email=email,
            ad_soyad="Test Müşteri",
            sifre_hash=sifre_hashle("musteri123"),
            rol="kullanici"  # Standart kullanıcı
        )
        db.add(yeni_kullanici)
        db.commit()
        print(f"✅ Kullanıcı oluşturuldu: {email} / musteri123")
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_customer()
