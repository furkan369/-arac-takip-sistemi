/**
 * Genel Bakış (Dashboard) Sayfası
 */
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Car, Wrench, Receipt, TrendingUp, Fuel, Plus } from 'lucide-react'
import { aracServisi } from '../servisler/api'
import Skeleton from '../bilesenler/Skeleton'
import AracKarti from '../bilesenler/AracKarti'
import AracEkleFormu from '../bilesenler/araclar/AracEkleFormu'
import BakimEkleFormu from '../bilesenler/bakimlar/BakimEkleFormu'
import HarcamaEkleFormu from '../bilesenler/harcamalar/HarcamaEkleFormu'
import YakitEkleFormu from '../bilesenler/yakit/YakitEkleFormu'
import HarcamaDagilimGrafik from '../bilesenler/grafikler/HarcamaDagilimGrafik'
import MaliyetEgilimGrafik from '../bilesenler/grafikler/MaliyetEgilimGrafik'
import BakimTakipGrafik from '../bilesenler/grafikler/BakimTakipGrafik'
import AracKarsilastirmaGrafik from '../bilesenler/grafikler/AracKarsilastirmaGrafik'
import styles from './GenelBakis.module.css'

export default function GenelBakis() {
    const [formlar, setFormlar] = useState({
        arac: false,
        bakim: false,
        harcama: false,
        yakit: false
    })

    // Modal Aç/Kapa Yardımcısı
    const toggleForm = (formAdi, durum) => {
        setFormlar(prev => ({ ...prev, [formAdi]: durum }))
    }

    const { data: araclar, isLoading, isError, error } = useQuery({
        queryKey: ['araclar'],
        queryFn: () => aracServisi.tumunuGetir({ sadece_aktifler: false }),
    })

    if (isLoading) {
        return (
            <div className={styles.dashboard}>
                <div className={styles.header}>
                    <Skeleton width="200px" height="32px" borderRadius="8px" style={{ marginBottom: 10 }} />
                    <Skeleton width="300px" height="20px" borderRadius="4px" />
                </div>

                <div className={styles.statsGrid}>
                    {[1, 2, 3, 4].map(i => (
                        <Skeleton key={i} height="120px" borderRadius="20px" />
                    ))}
                </div>

                <div className={styles.section}>
                    <div className={styles.sectionHeader} style={{ marginBottom: 20 }}>
                        <Skeleton width="150px" height="28px" borderRadius="8px" />
                        <Skeleton width="140px" height="40px" borderRadius="99px" />
                    </div>
                    <div className={styles.aracGrid}>
                        {[1, 2, 3].map(i => (
                            <Skeleton key={i} height="280px" borderRadius="20px" />
                        ))}
                    </div>
                </div>
            </div>
        )
    }

    if (isError) {
        return (
            <div className={styles.errorCard}>
                <h3>Hata Oluştu</h3>
                <p>{error.message}</p>
            </div>
        )
    }

    const istatistikler = [
        {
            baslik: 'Toplam Araç',
            deger: araclar?.length || 0,
            ikon: Car,
            renkSinifi: 'birincil',
        },
        {
            baslik: 'Aktif Araç',
            deger: araclar?.filter(a => a.aktif_mi).length || 0,
            ikon: TrendingUp,
            renkSinifi: 'ikincil',
        },
        {
            baslik: 'Toplam Bakım',
            deger: '-', // İleride API'den gelecek
            ikon: Wrench,
            renkSinifi: 'birincil',
        },
        {
            baslik: 'Toplam Harcama',
            deger: '-', // İleride API'den gelecek
            ikon: Receipt,
            renkSinifi: 'hata',
        },
    ]

    return (
        <div className={styles.dashboard}>
            {/* Başlık ve Hızlı İşlemler */}
            <div className={styles.header} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '16px' }}>
                <div>
                    <h1 className="baslik-2">Genel Bakış</h1>
                    <p>Araç takip sisteminize hoş geldiniz</p>
                </div>

                <div style={{ display: 'flex', gap: '12px' }}>
                    <button className="btn btn-outline" style={{ padding: '10px 16px', fontSize: '14px' }} onClick={() => toggleForm('yakit', true)}>
                        <Fuel size={18} /> Yakıt
                    </button>
                    <button className="btn btn-outline" style={{ padding: '10px 16px', fontSize: '14px' }} onClick={() => toggleForm('harcama', true)}>
                        <Receipt size={18} /> Harcama
                    </button>
                    <button className="btn btn-outline" style={{ padding: '10px 16px', fontSize: '14px' }} onClick={() => toggleForm('bakim', true)}>
                        <Wrench size={18} /> Bakım
                    </button>
                </div>
            </div>

            {/* İstatistikler */}
            {/* İstatistikler */}
            <div className={styles.statsGrid}>
                {istatistikler.map((stat, index) => {
                    const Ikon = stat.ikon
                    return (
                        <div key={index} className={`${styles.statCard} animate-fade-in`} style={{ animationDelay: `${index * 100}ms` }}>
                            <div className={styles.statContent}>
                                <div className={styles.statInfo}>
                                    <h3>{stat.baslik}</h3>
                                    <p>{stat.deger}</p>
                                </div>
                                <div
                                    className={styles.statIcon}
                                    style={{
                                        background: stat.renkSinifi === 'birincil' ? 'var(--renk-birincil-acik)' :
                                            stat.renkSinifi === 'ikincil' ? 'var(--renk-ikincil-acik)' :
                                                'var(--renk-hata-acik)',
                                        color: stat.renkSinifi === 'birincil' ? 'var(--renk-birincil)' :
                                            stat.renkSinifi === 'ikincil' ? 'var(--renk-ikincil)' :
                                                'var(--renk-hata)'
                                    }}
                                >
                                    <Ikon size={24} />
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Araçlar */}
            <div className={styles.section}>
                <div className={styles.sectionHeader}>
                    <h2 className="baslik-3">Araçlarınız</h2>
                    <button className="btn btn-birincil" onClick={() => toggleForm('arac', true)}>
                        <Plus size={18} /> Yeni Araç Ekle
                    </button>
                </div>

                {araclar && araclar.length > 0 ? (
                    <div className={styles.aracGrid}>
                        {araclar.map((arac, index) => (
                            <div key={arac.id} className="animate-slide-in" style={{ animationDelay: `${index * 100}ms` }}>
                                <AracKarti arac={arac} />
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className={styles.emptyState}>
                        <Car className={styles.emptyIcon} size={64} />
                        <h3>Henüz araç eklenmemiş</h3>
                        <p>İlk aracınızı ekleyerek başlayın</p>
                        <button className="btn btn-birincil" onClick={() => toggleForm('arac', true)}>
                            İlk Aracı Ekle
                        </button>
                    </div>
                )}
            </div>

            {/* Grafikler */}
            {
                araclar && araclar.length > 0 && (
                    <div className={styles.section}>
                        <h2 className="baslik-3">Analiz ve İstatistikler</h2>

                        <div className={styles.grafiklerGrid}>
                            <div className={styles.grafikKart}>
                                <h3>Harcama Dağılımı</h3>
                                <HarcamaDagilimGrafik />
                            </div>

                            <div className={styles.grafikKart}>
                                <h3>Aylık Maliyet Eğilimi</h3>
                                <MaliyetEgilimGrafik aySayisi={6} />
                            </div>

                            <div className={styles.grafikKart}>
                                <h3>Bakım Takip</h3>
                                <BakimTakipGrafik aracId={araclar[0]?.id} />
                            </div>

                            <div className={styles.grafikKart}>
                                <h3>Araç Karşılaştırma</h3>
                                <AracKarsilastirmaGrafik />
                            </div>
                        </div>
                    </div>
                )
            }

            {/* Modallar */}
            <AracEkleFormu acik={formlar.arac} kapat={() => toggleForm('arac', false)} />
            <BakimEkleFormu acik={formlar.bakim} kapat={() => toggleForm('bakim', false)} />
            <HarcamaEkleFormu acik={formlar.harcama} kapat={() => toggleForm('harcama', false)} />
            <YakitEkleFormu acik={formlar.yakit} kapat={() => toggleForm('yakit', false)} />
        </div >
    )
}
