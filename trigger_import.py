import requests
import json

print("🚀 Import başlatılıyor...")

# JSON dosyasını oku
with open('data_export.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📦 {len(data.get('kullanicilar', []))} kullanıcı, {len(data.get('araclar', []))} araç bulundu")

try:
    response = requests.post(
        'https://arac-takip-backend.onrender.com/api/v1/admin/import-data',
        json=data,  # JSON'u body'de gönder
        timeout=60
    )
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ BAŞARILI!")
        result = response.json()
        print(f"Stats: {result}")
    else:
        print(f"\n❌ HATA: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
