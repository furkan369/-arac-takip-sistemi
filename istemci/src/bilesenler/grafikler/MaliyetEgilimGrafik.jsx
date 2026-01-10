/**
 * Aylık Harcama Trendi - Çizgi Grafik
 * Zaman bazlı maliyet eğilimini gösterir
 */
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { istatistikServisi } from '../../servisler/api'
import Yukleyici from '../Yukleyici'
import styles from './Grafikler.module.css'

export default function MaliyetEgilimGrafik({ aracId = null, aySayisi = 6 }) {
    const { data: veriler, isLoading, isError } = useQuery({
        queryKey: ['aylik-harcama', aracId, aySayisi],
        queryFn: () => istatistikServisi.aylikHarcama(aracId, aySayisi),
    })

    if (isLoading) return <Yukleyici />

    if (isError || !veriler || veriler.length === 0) {
        return (
            <div className={styles.bosVeri}>
                <p>📈 Henüz aylık harcama verisi yok</p>
            </div>
        )
    }

    //Format ay görüntüleme
    const ayFormatla = (ayStr) => {
        const [yil, ay] = ayStr.split('-')
        const ayIsimleri = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
        return `${ayIsimleri[parseInt(ay) - 1]} ${yil.slice(2)}`
    }

    return (
        <div className={styles.grafikKapsayici}>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={veriler} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--renk-kenar)" />
                    <XAxis
                        dataKey="ay"
                        tickFormatter={ayFormatla}
                        stroke="var(--renk-metin-ikincil)"
                    />
                    <YAxis
                        stroke="var(--renk-metin-ikincil)"
                        tickFormatter={(value) => `₺${value.toLocaleString('tr-TR')}`}
                    />
                    <Tooltip
                        formatter={(value) => [`₺${value.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}`, 'Toplam Harcama']}
                        labelFormatter={ayFormatla}
                        contentStyle={{
                            background: 'var(--renk-yuzey)',
                            border: '1px solid var(--renk-kenar)',
                            borderRadius: 'var(--radius-medium)',
                            boxShadow: 'var(--golge-2)'
                        }}
                    />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="tutar"
                        name="Aylık Harcama"
                        stroke="var(--renk-birincil)"
                        strokeWidth={3}
                        dot={{ fill: 'var(--renk-birincil)', r: 5 }}
                        activeDot={{ r: 8 }}
                        animationDuration={1000}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}
