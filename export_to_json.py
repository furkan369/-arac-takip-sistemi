"""
MySQL to JSON Export Script
Exports all data from local MySQL to JSON file
"""
import pymysql
import json
from datetime import datetime, date
from decimal import Decimal

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '369furki2929',
    'database': 'arac_takip'
}

def datetime_handler(obj):
    """JSON serialization for MySQL data types"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def export_table(cursor, table_name):
    """Export a single table to dict"""
    print(f"📦 {table_name} export ediliyor...")
    
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    
    print(f"   ✅ {len(data)} kayıt export edildi")
    return data

def main():
    print("=" * 60)
    print("📤 MySQL → JSON Export")
    print("=" * 60)
    
    try:
        # MySQL connection
        conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ MySQL bağlantısı başarılı\n")
        cursor = conn.cursor()
        
        # Export all tables
        export_data = {
            'kullanicilar': export_table(cursor, 'kullanicilar'),
            'araclar': export_table(cursor, 'araclar'),
            'bakimlar': export_table(cursor, 'bakimlar'),
            'harcamalar': export_table(cursor, 'harcamalar'),
            'yakit_takibi': export_table(cursor, 'yakit_takibi'),
            'hatirlaticilar': export_table(cursor, 'hatirlaticilar'),
        }
        
        # Write to JSON
        output_file = 'data_export.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=datetime_handler)
        
        print(f"\n✅ Export tamamlandı: {output_file}")
        print("=" * 60)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        raise

if __name__ == "__main__":
    main()
