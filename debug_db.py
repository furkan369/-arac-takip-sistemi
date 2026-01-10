from sunucu.veritabani import SessionLocal
from sunucu.modeller.arac import Araclar
from sunucu.modeller.kullanici import Kullanicilar

def check_vehicles():
    db = SessionLocal()
    try:
        # 1. Kullanıcıları Listele
        users = db.query(Kullanicilar).all()
        print("\n--- KULLANICILAR ---")
        for u in users:
            print(f"ID: {u.id}, Ad: {u.ad_soyad}, Rol: {u.rol}")

        # 2. Araçları Listele
        vehicles = db.query(Araclar).all()
        print("\n--- ARAÇLAR ---")
        for v in vehicles:
            status = "SİLİNMİŞ" if v.silinmis_mi else "AKTİF"
            print(f"ID: {v.id}, Plaka: {v.plaka}, Sahip ID: {v.kullanici_id}, Durum: {status}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_vehicles()
