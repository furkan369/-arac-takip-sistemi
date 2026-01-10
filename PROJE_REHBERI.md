# Akıllı Araç Bakım ve Masraf Takip Sistemi - Proje Rehberi

Bu dosya, projenin tüm geliştirme aşamalarında uyulması gereken standartları, kod optimizasyon kurallarını, yol haritasını ve özellik listesini içerir.

---

## 📋 KOD OPTİMİZASYON KURALLARI

### 1. "Refactoring" (Kod İyileştirme) Tekniği

AI'ya kodu yazdırdıktan sonra hemen kabul etme. İkinci bir adım olarak "temizlik" yaptır.

**Kritik Prompt:** "Bu yazdığın kod çok uzun ve karmaşık. Bunu DRY (Don't Repeat Yourself) prensibine göre optimize et. Tekrar eden kısımları fonksiyonlara ayır ve kod satır sayısını azaltırken aynı performansı (hatta daha iyisini) koru."

### 2. Kütüphanelerin Gücünü Kullan (Az Kod = Az Sermaye)

Eğer AI her şeyi sıfırdan (vanilla) yazmaya çalışıyorsa, kod uzar. Modern kütüphaneler 100 satırlık işi 5 satıra indirir.

**Strateji:** AI'ya şunu de: "Bu işlemi ham kodla (hard-coded) yapmak yerine, en popüler ve performanslı kütüphaneleri (örneğin veri için Pandas, tasarım için Tailwind, API için Axios) kullanarak en kısa yoldan yaz."

**Maliyet:** Daha az kod, daha az hata demektir. Hata ayıklama (debug) süren kısalacağı için "zaman sermayenden" tasarruf edersin.

### 3. "Incremental" (Kademeli) Optimizasyon

Projeyi kökten ele alma hatasına düşmemek için "Cerrahi Müdahale" yapmalısın.

**Yöntem:** Tüm projeyi AI'ya verip "bunu kısalt" dersen kafası karışır ve her şeyi bozar.

**Uygulama:** Sadece tek bir fonksiyonu veya tek bir dosyayı seç. "Sadece bu dosyadaki mantığı sadeleştir, diğer dosyalara dokunma" de. Parça parça iyileştirerek ilerle.

### 4. Algoritmik Verimlilik (Performans)

Az kod her zaman hızlı kod demek değildir. Bazen 3 satırlık bir kod, 100 satırlık koddan daha yavaş çalışabilir.

**Performans Promptu:** "Bu kodun Zaman Karmaşıklığını (Time Complexity) analiz et. Daha az bellek (RAM) ve CPU harcayacak şekilde optimize et. Döngüleri (loops) minimize et."

---

## 🗺️ PROJE YOL HARİTASI

### 1. Aşama: Temel Mimari ve Standartların Belirlenmesi

Projenin en kritik kuralı, tüm isimlendirmelerin ve kod içi açıklamaların tamamen Türkçe olmasıdır.

**Klasör Yapısı:**
- `/sunucu` ana klasörü altında `/uygulama`, `/modeller`, `/semalar` ve `/yonlendiriciler` klasörleri oluşturulmalıdır.

**Veritabanı Bağlantısı:**
- `veritabani.py` dosyası içinde `mysql+mysqlconnector` kullanılarak MySQL bağlantısı yapılandırılmalıdır.

**Teknoloji Yığını:**
- Backend için FastAPI
- Veritabanı yönetimi için SQLAlchemy (ORM)
- Tasarım için Material 3 standartları

### 2. Aşama: Veri Modellerinin ve Şemaların Genişletilmesi

**Mevcut Modeller:**
- Araclar (plaka, marka, model)
- Bakimlar (son_bakim_km, yapilan_islem)
- Harcamalar (tutar, kategori)

**Kapsamı Artıracak Eklemeler:**
- **Yakıt Takibi:** YakitAlimlari tablosu eklenerek aracın yakıt tüketim verimliliği ölçülebilir.
- **Hatırlatıcılar:** Sigorta, kasko veya periyodik bakım vakti geldiğinde kullanıcıyı uyaran bir Hatirlaticilar tablosu.
- **Kullanıcı Yönetimi:** Birden fazla aracın yönetilebilmesi için bir Kullanicilar modeli.

### 3. Aşama: API Uç Noktaları ve İş Mantığı (Logic)

`/yonlendiriciler` klasörü altında işlevsel API'lar geliştirilir:

**CRUD İşlemleri:**
- Araç ekleme, silme ve güncelleme fonksiyonları

**Hesaplama Motoru:**
- Aracın toplam masrafını veya kilometre başına maliyetini hesaplayan özel fonksiyonlar

**Dokümantasyon:**
- FastAPI'nin otomatik dokümantasyon özelliği kullanılarak tüm API uç noktaları test edilebilir hale getirilir

### 4. Aşama: Kullanıcı Deneyimi ve Arayüz Tasarımı

Sistemin tasarımı Material 3 standartlarına uygun olarak planlanmalıdır:

**Görselleştirme:**
- Harcamaların kategorilerine göre (yakıt, bakım, vergi) grafiklerle gösterilmesi

**Mobil Uyumluluk:**
- Aracın yanındayken masraf girişini kolaylaştıracak sade bir arayüz

### 5. Aşama: Test ve Dağıtım

- Her fonksiyonun ne işe yaradığını açıklayan Türkçe yorum satırları ile kodun okunabilirliği artırılmalıdır
- Veritabanı tablolarının ve ilişkilerinin doğruluğu SQLAlchemy üzerinden kontrol edilmelidir

---

## 🎯 ÖZELLİK LİSTESİ

### 1. Kullanıcı Yönetimi ve Yetkilendirme

**Kullanicilar Tablosu:**
- Birden fazla kullanıcının kendi araçlarını yönetebilmesi için bir profil sistemi

**Giriş Sistemi:**
- OAuth2 veya JWT kullanarak güvenli giriş ve kayıt olma özellikleri

### 2. Yakıt Takip Modülü

Mevcut "Harcamalar" modelini detaylandırarak sadece yakıt verilerini işleyen bir yapı:

**Yakit_Verimliligi:**
- Alınan yakıt miktarı ve gidilen mesafe üzerinden aracın 100 km'de ne kadar yaktığını hesaplayan bir fonksiyon

**İstasyon Bazlı Takip:**
- Hangi yakıt istasyonundan alınan yakıtın daha uzun mesafe gittiğini analiz eden bir veri alanı

### 3. Hatırlatıcılar ve Bildirim Sistemi

"Bakimlar" tablosundaki son_bakim_km verisini kullanarak akıllı uyarılar:

**Periyodik Bakım Uyarıları:**
- Bir sonraki bakım zamanı yaklaştığında (örneğin 10.000 km dolmaya yakın) kullanıcıya uyarı veren bir mantık

**Resmi Evrak Takibi:**
- Sigorta, kasko ve muayene tarihlerini saklayan ve bitişine 30 gün kala bildirim gönderen bir yapı

### 4. Gelişmiş Raporlama ve İstatistikler

"Harcamalar" tablosundaki verileri anlamlı bilgilere dönüştürme:

**Kategori Bazlı Harcama:**
- Aylık toplam masrafın ne kadarının yakıt, ne kadarının bakım veya vergi olduğunun yüzdesel dağılımı

**Kilometre Başına Maliyet:**
- Aracın toplam kullanım süresince kilometre başına kaç TL harcadığının hesaplanması

### 5. Belge Arşivi (Dijital Torpido Gözü)

**Dosya Yönetimi:**
- Aracın ruhsat fotokopisi, sigorta poliçesi veya bakım faturalarının PDF/Görsel olarak sisteme yüklenmesi
- Bu özellik için sunucu tarafında dosya yükleme uç noktaları eklenmelidir

### 6. Lastik Takip ve Yönetim Modülü

**Lastik_Bilgileri Tablosu:**
- Lastiklerin markası, üretim tarihi (DOT), takıldığı kilometre ve tipi (Yaz/Kış/Dört Mevsim)

**Değişim Uyarıcı:**
- Mevsim geçişlerinde (Nisan/Ekim) veya belirli bir kilometre sınırına ulaşıldığında kullanıcıya lastik değişimi hatırlatması

### 7. Parça Bazlı Stok ve Envanter Yönetimi

**Yedek_Parcalar Modeli:**
- Yağ filtresi, balata, silecek gibi sık değişen parçaların fiyat ve marka bilgisinin tutulması

**Maliyet Analizi:**
- Harcamalar tablosuyla ilişkilendirilerek, hangi markanın daha uzun süre dayandığının (performans/maliyet oranı) takibi

### 8. Dijital Servis Defteri ve PDF Raporlama

**Ekspertiz Hazırlığı:**
- Aracın satılması durumunda, yapılan tüm işlemlerin tarih, kilometre ve tutar bazlı dökümünün PDF olarak dışa aktarılması

**Görsel Kanıtlar:**
- Bakım sırasında çekilen fatura veya eski-yeni parça fotoğraflarının sisteme yüklenmesi
- Bu özellik için sunucu tarafında dosya saklama mantığı eklenmelidir

### 9. Yakıt Tüketim Analizi ve Rota Maliyeti

**Anlık Verimlilik:**
- Son alınan yakıt ile gidilen mesafe üzerinden "Şehir içi/Şehir dışı" tüketim farklarının hesaplanması

**Seyahat Planlayıcı:**
- Gidilecek mesafe girildiğinde, aracın ortalama verilerine dayanarak ne kadar yakıt harcayacağının tahmin edilmesi

### 10. Resmi Ödemeler ve Yasal Takip

**Resmi_Odemeler Tablosu:**
- MTV (Motorlu Taşıtlar Vergisi), Trafik Sigortası ve Kasko tarihlerinin takibi

**Muayene Randevu Hatırlatıcı:**
- Araclar tablosundaki bilgilere dayanarak muayene tarihinin yaklaşması durumunda bildirim gönderilmesi

---

## 🔮 GELECEKTEKİ ÖZELLİKLER (Kaynak Dışı Öneriler)

> **Not:** Aşağıdaki öneriler temel planlarda yer almamaktadır, isteğe bağlı eklemelerdir.

### Dış Servis Entegrasyonları
- Güncel yakıt fiyatlarını otomatik çeken bir API entegrasyonu

### Servis Randevu Sistemi
- Anlaşmalı servislerden doğrudan uygulama üzerinden randevu alma özelliği

### Harita Entegrasyonu
- En yakın tamirhane veya akaryakıt istasyonunu gösteren bir harita modülü

---

## 📐 MİMARİ STANDARTLAR

### Zorunlu Kurallar

1. **Tamamen Türkçe İsimlendirme:**
   - Tüm klasör isimleri Türkçe
   - Tüm dosya isimleri Türkçe
   - Tüm değişken isimleri Türkçe
   - Tüm tablo ve sütun isimleri Türkçe
   - Tüm yorumlar Türkçe

2. **DRY Prensibi:**
   - Kod tekrarından kaçınılmalı
   - Ortak fonksiyonlar ayrı modüllere çıkarılmalı

3. **Kütüphane Kullanımı:**
   - Modern ve güncel kütüphaneler tercih edilmeli
   - Vanilla kod yerine kütüphane gücü kullanılmalı

4. **Kod Yorumları:**
   - Her dosyanın başında ne işe yaradığını açıklayan Türkçe yorum
   - Kritik fonksiyonlarda açıklayıcı yorumlar

5. **Soft Delete:**
   - Kayıtlar fiziksel olarak silinmeyecek
   - `silinmis_mi` bayrağı kullanılacak

6. **Otomatik Zaman Damgaları:**
   - Her kayıt `olusturulma_tarihi` ve `guncellenme_tarihi` alanlarına sahip olacak

---

## 🎨 TASARIM STANDARTLARI

- **Tasarım Sistemi:** Material 3
- **Renk Şeması:** Modern ve profesyonel
- **Mobil Uyumluluk:** Responsive tasarım
- **Kullanıcı Deneyimi:** Sade ve kullanımı kolay arayüz

---

## ⚙️ TEKNOLOJİ YIĞINI

**Backend:**
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- MySQL (Veritabanı)
- mysql-connector-python (MySQL Driver)
- Pydantic (Veri Validasyonu)

**Güvenlik:**
- OAuth2 / JWT (Authentication)
- Şifre hashleme
- CORS yapılandırması

**Dokümantasyon:**
- FastAPI otomatik dokümantasyon (Swagger/ReDoc)

---

Bu rehber, projenin her aşamasında temel alınmalı ve tüm geliştirmeler bu standartlara uygun yapılmalıdır.
