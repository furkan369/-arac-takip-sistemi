"""
Admin Data Import Endpoint
One-time use endpoint to import data from JSON to PostgreSQL
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sunucu.veritabani import veritabani_baglantisi_al
from sunucu.modeller.kullanici import Kullanicilar
from sunucu.modeller.arac import Araclar
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.yakit_takibi import Yakit_Takibi
from sunucu.modeller.hatirlatici import Hatirlaticilar
import json
from datetime import datetime
from pathlib import Path

router = APIRouter()

@router.post("/admin/import-data")
async def import_data(import_data_json: dict, db: Session = Depends(veritabani_baglantisi_al)):
    """
    ÖZEL: Tek kullanımlık data import endpoint
    JSON data'yı request body'den alır ve PostgreSQL'e yazar
    
    ⚠️ UYARI: Import sonrası bu endpoint'i kaldırın!
    """
    try:
        # JSON data request body'den geliyor
        data = import_data_json
        
        stats = {
            "kullanicilar": 0,
            "araclar": 0,
            "bakimlar": 0,
            "harcamalar": 0,
            "yakit_takibi": 0,
            "hatirlaticilar": 0,
            "errors": []
        }
        
        # ID Mapping (MySQL ID → PostgreSQL ID)
        user_mapping = {}
        arac_mapping = {}
        
        # 1. KULLANICILAR
        for user_data in data.get("kullanicilar", []):
            try:
                old_id = user_data.pop("id")
                
                # Tarihleri parse et
                if "olusturulma_tarihi" in user_data and isinstance(user_data["olusturulma_tarihi"], str):
                    user_data["olusturulma_tarihi"] = datetime.fromisoformat(user_data["olusturulma_tarihi"])
                if "guncellenme_tarihi" in user_data and isinstance(user_data["guncellenme_tarihi"], str):
                    user_data["guncellenme_tarihi"] = datetime.fromisoformat(user_data["guncellenme_tarihi"])
                
                user = Kullanicilar(**user_data)
                db.add(user)
                db.flush()  # ID al
                
                user_mapping[old_id] = user.id
                stats["kullanicilar"] += 1
            except Exception as e:
                stats["errors"].append(f"Kullanici {old_id}: {str(e)}")
        
        # 2. ARAÇLAR
        for arac_data in data.get("araclar", []):
            try:
                old_id = arac_data.pop("id")
                
                # Foreign key güncelle
                old_user_id = arac_data.get("kullanici_id")
                if old_user_id in user_mapping:
                    arac_data["kullanici_id"] = user_mapping[old_user_id]
                
                # Tarihleri parse et
                if "olusturulma_tarihi" in arac_data and isinstance(arac_data["olusturulma_tarihi"], str):
                    arac_data["olusturulma_tarihi"] = datetime.fromisoformat(arac_data["olusturulma_tarihi"])
                if "guncellenme_tarihi" in arac_data and isinstance(arac_data["guncellenme_tarihi"], str):
                    arac_data["guncellenme_tarihi"] = datetime.fromisoformat(arac_data["guncellenme_tarihi"])
                
                arac = Araclar(**arac_data)
                db.add(arac)
                db.flush()
                
                arac_mapping[old_id] = arac.id
                stats["araclar"] += 1
            except Exception as e:
                stats["errors"].append(f"Arac {old_id}: {str(e)}")
        
        # 3. BAKIMLAR
        for bakim_data in data.get("bakimlar", []):
            try:
                bakim_data.pop("id")
                
                # Foreign key
                old_arac_id = bakim_data.get("arac_id")
                if old_arac_id in arac_mapping:
                    bakim_data["arac_id"] = arac_mapping[old_arac_id]
                
                # Tarihleri parse et
                for field in ["tarih", "sonraki_bakim_tarih", "olusturulma_tarihi", "guncellenme_tarihi"]:
                    if field in bakim_data and isinstance(bakim_data[field], str):
                        bakim_data[field] = datetime.fromisoformat(bakim_data[field]) if bakim_data[field] else None
                
                bakim = Bakimlar(**bakim_data)
                db.add(bakim)
                stats["bakimlar"] += 1
            except Exception as e:
                stats["errors"].append(f"Bakim: {str(e)}")
        
        # 4. HARCAMALAR
        for harcama_data in data.get("harcamalar", []):
            try:
                harcama_data.pop("id")
                
                old_arac_id = harcama_data.get("arac_id")
                if old_arac_id in arac_mapping:
                    harcama_data["arac_id"] = arac_mapping[old_arac_id]
                
                for field in ["tarih", "olusturulma_tarihi", "guncellenme_tarihi"]:
                    if field in harcama_data and isinstance(harcama_data[field], str):
                        harcama_data[field] = datetime.fromisoformat(harcama_data[field]) if harcama_data[field] else None
                
                harcama = Harcamalar(**harcama_data)
                db.add(harcama)
                stats["harcamalar"] += 1
            except Exception as e:
                stats["errors"].append(f"Harcama: {str(e)}")
        
        # 5. YAKIT TAKİBİ
        for yakit_data in data.get("yakit_takibi", []):
            try:
                yakit_data.pop("id")
                
                old_arac_id = yakit_data.get("arac_id")
                if old_arac_id in arac_mapping:
                    yakit_data["arac_id"] = arac_mapping[old_arac_id]
                
                for field in ["tarih", "olusturulma_tarihi", "guncellenme_tarihi"]:
                    if field in yakit_data and isinstance(yakit_data[field], str):
                        yakit_data[field] = datetime.fromisoformat(yakit_data[field]) if yakit_data[field] else None
                
                yakit = Yakit_Takibi(**yakit_data)
                db.add(yakit)
                stats["yakit_takibi"] += 1
            except Exception as e:
                stats["errors"].append(f"Yakit: {str(e)}")
        
        # 6. HATIRLATICILAR
        for hatirlatici_data in data.get("hatirlaticilar", []):
            try:
                hatirlatici_data.pop("id")
                
                old_arac_id = hatirlatici_data.get("arac_id")
                if old_arac_id in arac_mapping:
                    hatirlatici_data["arac_id"] = arac_mapping[old_arac_id]
                
                for field in ["tarih", "olusturulma_tarihi", "guncellenme_tarihi"]:
                    if field in hatirlatici_data and isinstance(hatirlatici_data[field], str):
                        hatirlatici_data[field] = datetime.fromisoformat(hatirlatici_data[field]) if hatirlatici_data[field] else None
                
                hatirlatici = Hatirlaticilar(**hatirlatici_data)
                db.add(hatirlatici)
                stats["hatirlaticilar"] += 1
            except Exception as e:
                stats["errors"].append(f"Hatirlatici: {str(e)}")
        
        # Commit
        db.commit()
        
        return {
            "success": True,
            "message": "Import tamamlandı",
            "stats": stats
        }
        
    except FileNotFoundError as e:
        import traceback
        error_detail = f"Dosya bulunamadı: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"❌ FileNotFoundError: {error_detail}")
        raise HTTPException(
            status_code=404,
            detail=error_detail
        )
    except Exception as e:
        import traceback
        error_detail = f"Import hatası: {type(e).__name__}: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"❌ Exception: {error_detail}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )
