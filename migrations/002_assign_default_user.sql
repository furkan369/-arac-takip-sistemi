-- Veri İzolasyonu Migration
-- Mevcut tüm araçlara varsayılan kullanici_id ata (ID:1 - Admin)

-- 1. Mevcut tüm araçlara kullanici_id=1 ata
UPDATE araclar 
SET kullanici_id = 1 
WHERE kullanici_id IS NULL;

-- 2. Kontrol: Kaç araç güncellendi
SELECT COUNT(*) AS 'Guncellenen_Arac_Sayisi' 
FROM araclar 
WHERE kullanici_id = 1;

-- 3. Tüm araçların kullanici_id'si dolu mu kontrol et
SELECT COUNT(*) AS 'Bos_Kullanici_ID' 
FROM araclar 
WHERE kullanici_id IS NULL;

-- Sonuç: Bos_Kullanici_ID = 0 olmalı
