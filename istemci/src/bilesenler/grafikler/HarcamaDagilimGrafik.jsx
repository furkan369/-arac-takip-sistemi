/**
 * Harcama Dağılımı - Pasta Grafik
 * Kategori bazlı harcama dağılımını gösterir
 */
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { istatistikServisi } from '../../servisler/api'
import Yukleyici from '../Yukleyici'
import styles from './Grafikler.module.css'

// Material 3 Renk Paleti
const RENKLER = [
    '#6750A4', // Birincil
    '#00A896', // İkincil
    '#FF6B6B', // Hata
    '#FFA500', // Uyarı
    '#4CAF50', // Başarı
    '#9C27B0', // Mor
    '#3F51B5', // İndigo
    '#00BCD4', // Cyan
]

export default function HarcamaDagilimGrafik({ aracId = null }) {
    const { data: veriler, isLoading, isError } = useQuery({
        queryKey: ['kategori-dagilim', aracId],
        queryFn: () => istatistikServisi.kategoriDagilim(aracId),
    })

    if (isLoading) return <Yukleyici />

    if (isError || !veriler || veriler.length === 0) {
        return (
            <div className={styles.bosVeri}>
                <p>📊 Henüz harcama verisi yok</p>
            </div>
        )
    }

    // Özel etiket renderlama
    const ozelEtiketRender = (value, entry) => {
        const data = entry.payload || {};
        return `${data.kategori || 'N/A'}: ₺${(data.tutar || 0).toLocaleString('tr-TR', { minimumFractionDigits: 2 })}`;
    }

    return (
        <div className={styles.grafikKapsayici}>
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={veriler}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={(entry) => `%${entry.oran}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="tutar"
                        animationDuration={800}
                        animationBegin={0}
                    >
                        {veriler.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={RENKLER[index % RENKLER.length]}
                            />
                        ))}
                    </Pie>
                    <Tooltip
                        formatter={(value) => `₺${value.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}`}
                        contentStyle={{
                            background: 'var(--renk-yuzey)',
                            border: '1px solid var(--renk-kenar)',
                            borderRadius: 'var(--radius-medium)',
                            boxShadow: 'var(--golge-2)'
                        }}
                    />
                    <Legend
                        formatter={ozelEtiketRender}
                        wrapperStyle={{ paddingTop: '20px' }}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    )
}
