from sqlalchemy import text
from sunucu.veritabani import SessionLocal

def run_migration():
    db = SessionLocal()
    try:
        print("Migration başlatılıyor (RBAC)...")
        
        # SQL dosyasını oku
        with open("migrations/003_add_role_column.sql", "r", encoding="utf-8") as f:
            sql_content = f.read()
            
        # Komutları ayır ve çalıştır
        commands = sql_content.split(';')
        for command in commands:
            if command.strip():
                print(f"Calistiriliyor: {command.strip()[:50]}...")
                db.execute(text(command))
                
        db.commit()
        print("✅ Migration başarıyla tamamlandı! Rol sistemi aktif.")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
