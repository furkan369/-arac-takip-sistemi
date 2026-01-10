-- Veritabanı Migration Script
-- Kullanıcı Sistemi için Tablo Güncellemeleri

-- 1. kullanicilar tablosunu oluştur
CREATE TABLE IF NOT EXISTS kullanicilar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    ad_soyad VARCHAR(255) NOT NULL,
    sifre_hash VARCHAR(255) NOT NULL,
    aktif_mi BOOLEAN DEFAULT TRUE,
    olusturulma_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    guncellenme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

-- 2. Admin kullanıcısı oluştur (şifre: admin123)
-- Şifre hash'i: bcrypt ile "admin123" için örnek hash
INSERT INTO kullanicilar (email, ad_soyad, sifre_hash, aktif_mi)
VALUES (
    'admin@aractakip.com',
    'Sistem Yöneticisi',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIRvT.F6.C',  -- admin123
    TRUE
);

-- 3. araclar tablosuna kullanici_id sütunu ekle
ALTER TABLE araclar 
ADD COLUMN kullanici_id INT,
ADD INDEX idx_kullanici_id (kullanici_id);

-- 4. Mevcut tüm araçları admin kullanıcısına ata
UPDATE araclar 
SET kullanici_id = (SELECT id FROM kullanicilar WHERE email = 'admin@aractakip.com' LIMIT 1)
WHERE kullanici_id IS NULL;

-- 5. kullanici_id'yi NOT NULL yap ve foreign key ekle
ALTER TABLE araclar 
MODIFY COLUMN kullanici_id INT NOT NULL,
ADD CONSTRAINT fk_araclar_kullanici 
    FOREIGN KEY (kullanici_id) 
    REFERENCES kullanicilar(id) 
    ON DELETE CASCADE;

-- Migration başarılı!
SELECT 'Migration tamamlandı!' AS Status;
SELECT COUNT(*) AS ToplamKullanici FROM kullanicilar;
SELECT COUNT(*) AS ToplamArac FROM araclar;
