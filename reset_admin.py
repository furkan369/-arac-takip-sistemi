from sunucu.veritabani import SessionLocal
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.servisler.auth_servisi import sifre_hashle

def reset_admin():
    db = SessionLocal()
    try:
        email = "admin@aractakip.com"
        yeni_sifre = "admin123"
        
        admin = db.query(Kullanicilar).filter(Kullanicilar.email == email).first()
        
        if admin:
            admin.sifre_hash = sifre_hashle(yeni_sifre)
            admin.rol = "admin" # Rolü de garantiye alalım
            db.commit()
            print(f"✅ Admin şifresi güncellendi: {email} -> {yeni_sifre}")
        else:
            # Admin yoksa oluşturalım
            yeni_admin = Kullanicilar(
                email=email,
                ad_soyad="Sistem Yöneticisi",
                sifre_hash=sifre_hashle(yeni_sifre),
                rol="admin"
            )
            db.add(yeni_admin)
            db.commit()
            print(f"✅ Admin oluşturuldu: {email} -> {yeni_sifre}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
