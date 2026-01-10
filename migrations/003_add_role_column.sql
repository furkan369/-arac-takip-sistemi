-- Kullanıcı Rol Yönetimi Migration
-- Rol sütunu ekle ve Admin'i yetkilendir

-- 1. Rol sütunu ekle (Varsayılan: 'kullanici')
ALTER TABLE kullanicilar 
ADD COLUMN rol VARCHAR(20) NOT NULL DEFAULT 'kullanici';

-- 2. ID:1 olan kullanıcıyı 'admin' yap (Patron)
UPDATE kullanicilar 
SET rol = 'admin' 
WHERE id = 1;

-- 3. Kontrol
SELECT id, email, ad_soyad, rol FROM kullanicilar;
