-- HIZLI MİGRATION SCRIPT (MySQL Uyumlu)
-- Bu SQL'i MySQL Workbench'de çalıştırın

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

-- 2. araclar tablosuna kullanici_id ekle
-- Önce kontrol et
SET @col_exists = (
    SELECT COUNT(*) 
    FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = 'arac_takip' 
    AND TABLE_NAME = 'araclar' 
    AND COLUMN_NAME = 'kullanici_id'
);

-- Sütun yoksa ekle
SET @query = IF(@col_exists = 0, 
    'ALTER TABLE araclar ADD COLUMN kullanici_id INT',
    'SELECT "kullanici_id sütunu zaten var" as Message'
);
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Index ekle (hata olsa bile devam eder)
ALTER TABLE araclar ADD INDEX idx_kullanici_id (kullanici_id);

-- TAMAMLANDI!
SELECT 'Migration başarılı!' as Status;
