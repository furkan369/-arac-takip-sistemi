/**
 * Bakım Takip Göstergesi - Kadran Grafik
 * Bakıma kalan KM'yi gösterir
 */
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { istatistikServisi } from '../../servisler/api'
import Yukleyici from '../Yukleyici'
import styles from './Grafikler.module.css'

export default function BakimTakipGrafik({ aracId }) {
    const { data: veri, isLoading, isError } = useQuery({
        queryKey: ['bakim-takip', aracId],
        queryFn: () => istatistikServisi.bakimTakip(aracId),
        enabled: !!aracId,
    })

    if (isLoading) return <Yukleyici />

    if (isError || !veri || veri.hata) {
        return (
            <div className={styles.bosVeri}>
                <p>🔧 Bakım takip verisi yüklenemedi</p>
            </div>
        )
    }

    // Kadran verisi (yarım daire)
    const kadranVerisi = [
        { name: 'Tamamlanan', value: veri.oran },
        { name: 'Kalan', value: 100 - veri.oran }
    ]

    // Durum rengini belirle
    const durumRengi = {
        'normal': '#4CAF50',  // Yeşil
        'uyari': '#FFA500',   // Turuncu
        'tehlike': '#FF6B6B'  // Kırmızı
    }[veri.durum] || '#4CAF50'

    const RENKLER = [durumRengi, '#E0E0E0']

    return (
        <div className={styles.grafikKapsayici}>
            <div className={styles.kadranKapsayici}>
                <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                        <Pie
                            data={kadranVerisi}
                            cx="50%"
                            cy="70%"
                            startAngle={180}
                            endAngle={0}
                            innerRadius={60}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                            stroke="none"
                        >
                            {kadranVerisi.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={RENKLER[index]} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>

                {/* Merkez Bilgi */}
                <div className={styles.kadranMerkez}>
                    <div className={styles.kadranDeger} style={{ color: durumRengi }}>
                        {veri.kalan_km.toLocaleString('tr-TR')}
                    </div>
                    <div className={styles.kadranEtiket}>KM Kaldı</div>
                </div>

                {/* Detay Bilgileri */}
                <div className={styles.kadranDetay}>
                    <div className={styles.detayItem}>
                        <span>Mevcut KM:</span>
                        <strong>{veri.mevcut_km.toLocaleString('tr-TR')}</strong>
                    </div>
                    <div className={styles.detayItem}>
                        <span>Sonraki Bakım:</span>
                        <strong>{veri.sonraki_bakim_km.toLocaleString('tr-TR')}</strong>
                    </div>
                    <div className={styles.detayItem}>
                        <span>Durum:</span>
                        <strong style={{ color: durumRengi }}>
                            {veri.durum === 'normal' ? '✓ Normal' :
                                veri.durum === 'uyari' ? '⚠ Yaklaşıyor' :
                                    '⚠ Acil!'}
                        </strong>
                    </div>
                </div>
            </div>
        </div>
    )
}
