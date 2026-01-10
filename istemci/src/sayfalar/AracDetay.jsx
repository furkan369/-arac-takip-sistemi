/**
 * Araç Detay Sayfası
 * Material 3 Tabs ve KPI Kartları
 */
import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
    ArrowLeft, Car, Wrench, Receipt, Fuel,
    Calendar, Gauge, TrendingUp
} from 'lucide-react'
import { aracServisi } from '../servisler/api'
import Yukleyici from '../bilesenler/Yukleyici'
import styles from './AracDetay.module.css'

export default function AracDetay() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [aktifTab, setAktifTab] = useState('genel')

    const { data: arac, isLoading, isError, error } = useQuery({
        queryKey: ['arac', id],
        queryFn: () => aracServisi.detayGetir(id),
    })

    if (isLoading) return <Yukleyici />

    if (isError) {
        return (
            <div className={styles.container}>
                <div className={styles.header}>
                    <h3>Hata Oluştu</h3>
                    <p>{error.message}</p>
                    <button onClick={() => navigate(-1)} className="btn btn-birincil">Geri Dön</button>
                </div>
            </div>
        )
    }

    // KPI Hesaplamaları
    const toplamBakim = arac.bakimlar?.reduce((top, b) => top + (b.tutar || 0), 0) || 0
    const toplamHarcama = arac.harcamalar?.reduce((top, h) => top + (h.tutar || 0), 0) || 0
    const toplamYakit = arac.yakitlar?.reduce((top, y) => top + (y.litre * y.fiyat), 0) || 0
    const toplamMasraf = toplamBakim + toplamHarcama + toplamYakit

    return (
        <div className={styles.container}>
            {/* Header */}
            <div className={styles.header}>
                <div className={styles.headerInfo}>
                    <button onClick={() => navigate(-1)} className={styles.backButton}>
                        <ArrowLeft size={24} />
                    </button>
                    <div className={styles.title}>
                        <h1>
                            <span className={styles.plakaBadge}>{arac.plaka}</span>
                            {arac.marka} {arac.model}
                        </h1>
                        <p className={styles.subtitle}>
                            {arac.yil} Model • {arac.renk || 'Renk Belirtilmemiş'} • {arac.yakit_turu || 'Yakıt Tipi Yok'}
                        </p>
                    </div>
                </div>
                <div className="actions">
                    {/* Düzenle/Sil butonları buraya gelebilir */}
                </div>
            </div>

            {/* KPI Kartları */}
            <div className={styles.kpiGrid}>
                <div className={styles.kpiCard}>
                    <div className={styles.kpiIcon} style={{ background: '#EADDJP', color: '#21005D' }}>
                        <Gauge />
                    </div>
                    <div className={styles.kpiInfo}>
                        <h3>Güncel KM</h3>
                        <p>{arac.km?.toLocaleString('tr-TR')} km</p>
                    </div>
                </div>

                <div className={styles.kpiCard}>
                    <div className={styles.kpiIcon} style={{ background: '#FFD8E4', color: '#31111D' }}>
                        <Receipt />
                    </div>
                    <div className={styles.kpiInfo}>
                        <h3>Toplam Masraf</h3>
                        <p>₺{toplamMasraf.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}</p>
                    </div>
                </div>

                <div className={styles.kpiCard}>
                    <div className={styles.kpiIcon} style={{ background: '#E6E0E9', color: '#49454F' }}>
                        <Wrench />
                    </div>
                    <div className={styles.kpiInfo}>
                        <h3>Son Bakım</h3>
                        <p>{arac.bakimlar?.[0]?.tarih ? new Date(arac.bakimlar[0].tarih).toLocaleDateString('tr-TR') : '-'}</p>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className={styles.tabsContainer}>
                <div className={styles.tabsHeader}>
                    <button
                        className={`${styles.tabButton} ${aktifTab === 'genel' ? styles.active : ''}`}
                        onClick={() => setAktifTab('genel')}
                    >
                        Genel Bakış
                    </button>
                    <button
                        className={`${styles.tabButton} ${aktifTab === 'bakim' ? styles.active : ''}`}
                        onClick={() => setAktifTab('bakim')}
                    >
                        Bakımlar ({arac.bakimlar?.length || 0})
                    </button>
                    <button
                        className={`${styles.tabButton} ${aktifTab === 'harcama' ? styles.active : ''}`}
                        onClick={() => setAktifTab('harcama')}
                    >
                        Harcamalar ({arac.harcamalar?.length || 0})
                    </button>
                    <button
                        className={`${styles.tabButton} ${aktifTab === 'yakit' ? styles.active : ''}`}
                        onClick={() => setAktifTab('yakit')}
                    >
                        Yakıt ({arac.yakitlar?.length || 0})
                    </button>
                </div>

                <div className={styles.tabContent}>
                    {/* Bakım Listesi */}
                    {aktifTab === 'bakim' && (
                        <div className={styles.listContainer}>
                            {arac.bakimlar?.length > 0 ? arac.bakimlar.map(bakim => (
                                <div key={bakim.id} className={styles.listItem}>
                                    <div className={styles.itemLeft}>
                                        <div className={styles.itemIcon}>
                                            <Wrench size={20} />
                                        </div>
                                        <div className={styles.itemInfo}>
                                            <h4>{bakim.bakim_turu}</h4>
                                            <p>{bakim.aciklama || 'Açıklama yok'}</p>
                                        </div>
                                    </div>
                                    <div className={styles.itemRight}>
                                        <div className={styles.amount}>₺{bakim.tutar?.toLocaleString('tr-TR')}</div>
                                        <span className={styles.date}>{new Date(bakim.tarih).toLocaleDateString('tr-TR')}</span>
                                    </div>
                                </div>
                            )) : <div className={styles.emptyState}>Kayıt bulunamadı.</div>}
                        </div>
                    )}

                    {/* Harcama Listesi */}
                    {aktifTab === 'harcama' && (
                        <div className={styles.listContainer}>
                            {arac.harcamalar?.length > 0 ? arac.harcamalar.map(harcama => (
                                <div key={harcama.id} className={styles.listItem}>
                                    <div className={styles.itemLeft}>
                                        <div className={styles.itemIcon}>
                                            <Receipt size={20} />
                                        </div>
                                        <div className={styles.itemInfo}>
                                            <h4>{harcama.kategori}</h4>
                                            <p>{harcama.aciklama || '-'}</p>
                                        </div>
                                    </div>
                                    <div className={styles.itemRight}>
                                        <div className={styles.amount}>₺{harcama.tutar?.toLocaleString('tr-TR')}</div>
                                        <span className={styles.date}>{new Date(harcama.tarih).toLocaleDateString('tr-TR')}</span>
                                    </div>
                                </div>
                            )) : <div className={styles.emptyState}>Kayıt bulunamadı.</div>}
                        </div>
                    )}

                    {/* Yakıt Listesi */}
                    {aktifTab === 'yakit' && (
                        <div className={styles.listContainer}>
                            {arac.yakitlar?.length > 0 ? arac.yakitlar.map(yakit => (
                                <div key={yakit.id} className={styles.listItem}>
                                    <div className={styles.itemLeft}>
                                        <div className={styles.itemIcon}>
                                            <Fuel size={20} />
                                        </div>
                                        <div className={styles.itemInfo}>
                                            <h4>{yakit.yakit_turu} - {yakit.litre} Lt</h4>
                                            <p>{yakit.istasyon || 'İstasyon belirtilmedi'}</p>
                                        </div>
                                    </div>
                                    <div className={styles.itemRight}>
                                        <div className={styles.amount}>₺{(yakit.litre * yakit.fiyat).toLocaleString('tr-TR')}</div>
                                        <span className={styles.date}>{new Date(yakit.tarih).toLocaleDateString('tr-TR')}</span>
                                    </div>
                                </div>
                            )) : <div className={styles.emptyState}>Kayıt bulunamadı.</div>}
                        </div>
                    )}

                    {/* Genel Bakış - Özet Grafik (İleride) */}
                    {aktifTab === 'genel' && (
                        <div className={styles.emptyState}>
                            <TrendingUp size={48} style={{ opacity: 0.2, marginBottom: '16px' }} />
                            <h3>Aylık Özet Grafiği</h3>
                            <p>Çok yakında burada harcama grafiklerini göreceksiniz.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
