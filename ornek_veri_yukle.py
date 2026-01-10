"""
Örnek Veri Yükleme Scripti
API'yi test etmek için gerçekçi örnek veriler ekler.
"""
import requests
import random
from datetime import date, timedelta
from decimal import Decimal

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def tarih_uret(gun_once):
    """Belirli gün öncesinden tarih üret"""
    return (date.today() - timedelta(days=gun_once)).isoformat()


def araclar_ekle():
    """Örnek araçlar ekle"""
    print("\n🚗 Araçlar ekleniyor...")
    
    araclar = [
        {
            "plaka": "34ABC123",
            "marka": "Toyota",
            "model": "Corolla",
            "yil": 2018,
            "renk": "Beyaz",
            "km": 85000,
            "sase_no": "JTDBL40E289123456",
            "motor_no": "1NZ1234567",
            "notlar": "Özel araç, düzenli bakım yapılıyor"
        },
        {
            "plaka": "06XYZ789",
            "marka": "Volkswagen",
            "model": "Passat",
            "yil": 2020,
            "renk": "Siyah",
            "km": 45000,
            "sase_no": "WVWZZZ3CZ9E123456",
            "motor_no": "CAWA987654",
            "notlar": "İkinci el alındı, temiz araç"
        },
        {
            "plaka": "35DEF456",
            "marka": "Renault",
            "model": "Megane",
            "yil": 2019,
            "renk": "Gri",
            "km": 62000,
            "sase_no": "VF1LM1B0H56789012",
            "motor_no": "M4R789456",
            "notlar": "Aile aracı"
        },
        {
            "plaka": "16GHI321",
            "marka": "Honda",
            "model": "Civic",
            "yil": 2021,
            "renk": "Kırmızı",
            "km": 28000,
            "sase_no": "SHHFK7850MU123456",
            "motor_no": "R18A4567890",
            "notlar": "Yeni model, az kullanıldı"
        }
    ]
    
    arac_idler = []
    for arac in araclar:
        try:
            response = requests.post(f"{BASE_URL}/araclar", json=arac)
            if response.status_code == 201:
                veri = response.json()
                arac_idler.append(veri["id"])
                print(f"✅ {arac['plaka']} - {arac['marka']} {arac['model']} eklendi (ID: {veri['id']})")
            else:
                print(f"❌ Hata: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
    
    return arac_idler


def bakimlar_ekle(arac_idler):
    """Her araç için bakım kayıtları ekle"""
    print("\n🔧 Bakım kayıtları ekleniyor...")
    
    bakim_turleri = [
        "Yağ ve Filtre Değişimi",
        "Fren Balatası Değişimi",
        "Lastik Değişimi",
        "Akü Değişimi",
        "Klima Bakımı",
        "Tam Bakım",
        "Motor Yağı Değişimi",
        "Hava Filtresi Değişimi",
        "Polen Filtresi Değişimi",
        "Triger Kayışı Değişimi"
    ]
    
    servis_yerleri = [
        "ABC Oto Servis",
        "Yetkili Servis",
        "Özel Tamirhane",
        "CarService Pro",
        "Oto Bakım Merkezi"
    ]
    
    toplam = 0
    for arac_id in arac_idler:
        # Her araç için 8-15 bakım kaydı
        bakim_sayisi = random.randint(8, 15)
        
        for i in range(bakim_sayisi):
            gun_once = random.randint(30 + (i * 30), 60 + (i * 30))
            km_azaltma = random.randint(3000, 8000) * i
            
            bakim = {
                "arac_id": arac_id,
                "bakim_turu": random.choice(bakim_turleri),
                "tarih": tarih_uret(gun_once),
                "km": 85000 - km_azaltma,  # Geçmişe gidildikçe km azalıyor
                "tutar": round(random.uniform(200, 2500), 2),
                "servis_yeri": random.choice(servis_yerleri),
                "aciklama": f"Düzenli bakım yapıldı. {random.choice(['Sorunsuz', 'Kontrol yapıldı', 'Tavsiye edilen işlemler yapıldı'])}",
                "sonraki_bakim_km": 85000 - km_azaltma + random.randint(8000, 12000)
            }
            
            try:
                response = requests.post(f"{BASE_URL}/bakimlar", json=bakim)
                if response.status_code == 201:
                    toplam += 1
                    if toplam % 10 == 0:
                        print(f"  ✅ {toplam} bakım kaydı eklendi...")
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    print(f"✅ Toplam {toplam} bakım kaydı eklendi")


def harcamalar_ekle(arac_idler):
    """Her araç için harcama kayıtları ekle"""
    print("\n💰 Harcama kayıtları ekleniyor...")
    
    kategoriler = {
        "Sigorta": (1200, 3500),
        "Kasko": (2500, 8000),
        "MTV": (800, 2500),
        "Otopark": (50, 200),
        "Yıkama": (30, 80),
        "Oto Aksesuar": (100, 1500),
        "Lastik": (1500, 5000),
        "Ceza": (200, 1000),
        "Köprü/Otoyol": (20, 150),
        "Oto Kokusu": (25, 100)
    }
    
    toplam = 0
    for arac_id in arac_idler:
        # Her araç için 12-20 harcama kaydı
        harcama_sayisi = random.randint(12, 20)
        
        for i in range(harcama_sayisi):
            kategori = random.choice(list(kategoriler.keys()))
            min_tutar, max_tutar = kategoriler[kategori]
            
            harcama = {
                "arac_id": arac_id,
                "kategori": kategori,
                "tarih": tarih_uret(random.randint(1, 365)),
                "tutar": round(random.uniform(min_tutar, max_tutar), 2),
                "aciklama": f"{kategori} ödemesi yapıldı",
                "fis_no": f"FIS{random.randint(100000, 999999)}" if random.random() > 0.3 else None
            }
            
            try:
                response = requests.post(f"{BASE_URL}/harcamalar", json=harcama)
                if response.status_code == 201:
                    toplam += 1
                    if toplam % 10 == 0:
                        print(f"  ✅ {toplam} harcama kaydı eklendi...")
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    print(f"✅ Toplam {toplam} harcama kaydı eklendi")


def yakit_kayitlari_ekle(arac_idler):
    """Her araç için yakıt kayıtları ekle"""
    print("\n⛽ Yakıt kayıtları ekleniyor...")
    
    yakit_turleri = ["Benzin", "Dizel", "LPG"]
    istasyonlar = [
        "Shell", "BP", "Opet", "Petrol Ofisi", 
        "Total", "Aytemiz", "Alpet", "Moil"
    ]
    
    toplam = 0
    for idx, arac_id in enumerate(arac_idler):
        # İlk araç benzin, ikinci dizel, üçüncü benzin, dördüncü dizel
        yakit_turu = "Dizel" if idx % 2 == 1 else "Benzin"
        
        # Her araç için 15-25 yakıt kaydı
        yakit_sayisi = random.randint(15, 25)
        baslangic_km = 85000 - (yakit_sayisi * random.randint(350, 550))
        
        for i in range(yakit_sayisi):
            gun_once = yakit_sayisi * 7 - (i * 7)  # Her hafta yakıt alımı
            km = baslangic_km + (i * random.randint(350, 550))
            litre = round(random.uniform(35, 55), 2)
            
            # Benzin ve dizel fiyatları farklı
            if yakit_turu == "Benzin":
                fiyat = round(random.uniform(42, 48), 2)
            elif yakit_turu == "Dizel":
                fiyat = round(random.uniform(43, 49), 2)
            else:  # LPG
                fiyat = round(random.uniform(20, 25), 2)
            
            yakit = {
                "arac_id": arac_id,
                "tarih": tarih_uret(gun_once),
                "km": km,
                "litre": litre,
                "fiyat": fiyat,
                "toplam_tutar": round(litre * fiyat, 2),
                "yakit_turu": yakit_turu,
                "istasyon": random.choice(istasyonlar),
                "tam_depo": random.choice([True, False, False]),  # %33 tam depo
                "notlar": random.choice([
                    "Uzun yol öncesi",
                    "Rutin dolum",
                    "İndirimli fiyattan alındı",
                    None, None  # Çoğunlukla not yok
                ])
            }
            
            try:
                response = requests.post(f"{BASE_URL}/yakit", json=yakit)
                if response.status_code == 201:
                    toplam += 1
                    if toplam % 10 == 0:
                        print(f"  ✅ {toplam} yakıt kaydı eklendi...")
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    print(f"✅ Toplam {toplam} yakıt kaydı eklendi")


def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("📊 ÖRNEK VERİ YÜKLEME BAŞLIYOR")
    print("=" * 60)
    
    # Araçları ekle
    arac_idler = araclar_ekle()
    
    if not arac_idler:
        print("\n❌ Araç eklenemedi, işlem durduruluyor!")
        return
    
    print(f"\n✅ {len(arac_idler)} araç başarıyla eklendi!")
    
    # Bakım kayıtları ekle
    bakimlar_ekle(arac_idler)
    
    # Harcama kayıtları ekle
    harcamalar_ekle(arac_idler)
    
    # Yakıt kayıtları ekle
    yakit_kayitlari_ekle(arac_idler)
    
    print("\n" + "=" * 60)
    print("🎉 TÜM ÖRNEK VERİLER BAŞARIYLA YÜKLENDİ!")
    print("=" * 60)
    print(f"\n📋 Özet:")
    print(f"   • {len(arac_idler)} Araç")
    print(f"   • ~{len(arac_idler) * 12} Bakım Kaydı")
    print(f"   • ~{len(arac_idler) * 16} Harcama Kaydı")
    print(f"   • ~{len(arac_idler) * 20} Yakıt Kaydı")
    print(f"\n🌐 API Dokümantasyonu: http://localhost:8000/docs")
    print("\n")


if __name__ == "__main__":
    main()
