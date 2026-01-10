"""
İstatistik Servisi
Grafik ve raporlar için veri sağlar
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from typing import List, Dict, Any

from sunucu.modeller.harcama import Harcamalar
from sunucu.modeller.yakit_takibi import Yakit_Takibi
from sunucu.modeller.bakim import Bakimlar
from sunucu.modeller.arac import Araclar


def aylik_harcama_trendi(db: Session, kullanici_id: int, arac_id: int = None, ay_sayisi: int = 6, kullanici_rol: str = "kullanici") -> List[Dict[str, Any]]:
    """
    Son N ayın aylık toplam harcamalarını döndürür (kullanıcıya özel)
    Admin ise tüm harcamaları görebilir.
    """
    # Başlangıç ayını hesapla
    bugun = datetime.now()
    baslangic_tarihi = bugun - timedelta(days=ay_sayisi * 30)
    
    # Sorgu
    sorgu = db.query(
        func.DATE_FORMAT(Harcamalar.tarih, '%Y-%m').label('ay'),
        func.sum(Harcamalar.tutar).label('tutar')
    ).join(Araclar, Harcamalar.arac_id == Araclar.id)
    
    # Tarih filtresi
    sorgu = sorgu.filter(Harcamalar.tarih >= baslangic_tarihi)
    
    # Admin değilse kullanıcı filtresi ekle
    if kullanici_rol != 'admin':
        sorgu = sorgu.filter(Araclar.kullanici_id == kullanici_id)
    
    if arac_id:
        sorgu = sorgu.filter(Harcamalar.arac_id == arac_id)
    
    sonuclar = sorgu.group_by('ay').order_by('ay').all()
    
    return [{'ay': sonuc.ay, 'tutar': float(sonuc.tutar or 0)} for sonuc in sonuclar]



def kategori_dagilimi(db: Session, kullanici_id: int, arac_id: int = None, kullanici_rol: str = "kullanici") -> List[Dict[str, Any]]:
    """
    Harcama kategorilerinin toplam tutarlarını döndürür (kullanıcıya özel)
    Admin hepsini görür.
    """
    sorgu = db.query(
        Harcamalar.kategori,
        func.sum(Harcamalar.tutar).label('tutar')
    ).join(Araclar, Harcamalar.arac_id == Araclar.id)
    
    # Admin değilse filtrele
    if kullanici_rol != 'admin':
        sorgu = sorgu.filter(Araclar.kullanici_id == kullanici_id)
    
    if arac_id:
        sorgu = sorgu.filter(Harcamalar.arac_id == arac_id)
    
    sonuclar = sorgu.group_by(Harcamalar.kategori).all()
    
    toplam = sum(float(s.tutar or 0) for s in sonuclar)
    
    return [{
        'kategori': sonuc.kategori,
        'tutar': float(sonuc.tutar or 0),
        'oran': round((float(sonuc.tutar or 0) / toplam * 100) if toplam > 0 else 0, 1)
    } for sonuc in sonuclar]


def yakit_tuketim_analizi(db: Session, arac_id: int, ay_sayisi: int = 12) -> List[Dict[str, Any]]:
    """
    Aylık yakıt tüketimi ve ortalama hesaplar
    """
    bugun = datetime.now()
    baslangic_tarihi = bugun - timedelta(days=ay_sayisi * 30)
    
    sonuclar = db.query(
        func.DATE_FORMAT(Yakit_Takibi.tarih, '%Y-%m').label('ay'),
        func.sum(Yakit_Takibi.litre).label('toplam_litre'),
        func.sum(Yakit_Takibi.fiyat * Yakit_Takibi.litre).label('toplam_tutar'),
        func.count(Yakit_Takibi.id).label('adet')
    ).filter(
        and_(
            Yakit_Takibi.arac_id == arac_id,
            Yakit_Takibi.tarih >= baslangic_tarihi
        )
    ).group_by('ay').order_by('ay').all()
    
    return [{
        'ay': sonuc.ay,
        'litre': float(sonuc.toplam_litre or 0),
        'tutar': float(sonuc.toplam_tutar or 0),
        'adet': sonuc.adet,
        'ortalama_fiyat': round(float(sonuc.toplam_tutar or 0) / float(sonuc.toplam_litre or 1), 2)
    } for sonuc in sonuclar]



def arac_karsilastirma(db: Session, kullanici_id: int, kullanici_rol: str = "kullanici") -> List[Dict[str, Any]]:
    """
    Kullanıcının tüm araçlarını karşılaştırır.
    Admin ise tüm filoyu karşılaştırır.
    """
    sorgu = db.query(Araclar).filter(Araclar.silinmis_mi == False)
    
    # Admin değilse filtre
    if kullanici_rol != 'admin':
        sorgu = sorgu.filter(Araclar.kullanici_id == kullanici_id)
        
    araclar = sorgu.all()
    
    sonuclar = []
    for arac in araclar:
        # Harcamalar
        harcama_toplam = db.query(func.sum(Harcamalar.tutar)).filter(
            Harcamalar.arac_id == arac.id
        ).scalar() or 0
        
        # Yakıt
        yakit_toplam = db.query(
            func.sum(Yakit_Takibi.litre * Yakit_Takibi.fiyat)
        ).filter(Yakit_Takibi.arac_id == arac.id).scalar() or 0
        
        # Bakım
        bakim_toplam = db.query(func.sum(Bakimlar.tutar)).filter(
            Bakimlar.arac_id == arac.id
        ).scalar() or 0
        
        toplam = float(harcama_toplam) + float(yakit_toplam) + float(bakim_toplam)
        
        sonuclar.append({
            'arac': f"{arac.plaka} ({arac.marka} {arac.model})",
            'plaka': arac.plaka,
            'harcama': float(harcama_toplam),
            'yakit': float(yakit_toplam),
            'bakim': float(bakim_toplam),
            'toplam': toplam
        })
    
    return sorted(sonuclar, key=lambda x: x['toplam'], reverse=True)


def bakim_takip_gostergesi(db: Session, arac_id: int) -> Dict[str, Any]:
    """
    Bakım takip kadranı için veri
    """
    arac = db.query(Araclar).filter(Araclar.id == arac_id).first()
    if not arac:
        return {'hata': 'Araç bulunamadı'}
    
    # Son bakımı bul
    son_bakim = db.query(Bakimlar).filter(
        Bakimlar.arac_id == arac_id
    ).order_by(Bakimlar.tarih.desc()).first()
    
    mevcut_km = arac.km or 0
    son_bakim_km = son_bakim.km if son_bakim else 0
    sonraki_bakim_km = son_bakim.sonraki_bakim_km if (son_bakim and son_bakim.sonraki_bakim_km) else (mevcut_km + 10000)
    
    kalan_km = max(0, sonraki_bakim_km - mevcut_km)
    oran = min(100, max(0, ((mevcut_km - son_bakim_km) / (sonraki_bakim_km - son_bakim_km) * 100) if sonraki_bakim_km > son_bakim_km else 0))
    
    return {
        'mevcut_km': mevcut_km,
        'son_bakim_km': son_bakim_km,
        'sonraki_bakim_km': sonraki_bakim_km,
        'kalan_km': kalan_km,
        'oran': round(oran, 1),
        'durum': 'tehlike' if kalan_km < 1000 else ('uyari' if kalan_km < 3000 else 'normal')
    }
