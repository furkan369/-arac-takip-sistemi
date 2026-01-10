/**
 * Araç Karşılaştırma - Sütun Grafik
 * Araçların toplam maliyetlerini karşılaştırır
 */
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { istatistikServisi } from '../../servisler/api'
import Yukleyici from '../Yukleyici'
import styles from './Grafikler.module.css'

export default function AracKarsilastirmaGrafik() {
    const { data: veriler, isLoading, isError } = useQuery({
        queryKey: ['arac-karsilastirma'],
        queryFn: istatistikServisi.aracKarsilastirma,
    })

    if (isLoading) return <Yukleyici />

    if (isError || !veriler || veriler.length === 0) {
        return (
            <div className={styles.bosVeri}>
                <p>🚗 Henüz karşılaştırma verisi yok</p>
            </div>
        )
    }

    return (
        <div className={styles.grafikKapsayici}>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={veriler} margin={{ top: 20, right: 30, left: 20, bottom: 70 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--renk-kenar)" />
                    <XAxis
                        dataKey="plaka"
                        angle={-45}
                        textAnchor="end"
                        height={80}
                        stroke="var(--renk-metin-ikincil)"
                    />
                    <YAxis
                        tickFormatter={(value) => `₺${(value / 1000).toFixed(0)}k`}
                        stroke="var(--renk-metin-ikincil)"
                    />
                    <Tooltip
                        formatter={(value, name) => {
                            const etiketler = {
                                'bakim': 'Bakım',
                                'harcama': 'Harcama',
                                'yakit': 'Yakıt',
                                'toplam': 'Toplam'
                            }
                            return [`₺${value.toLocaleString('tr-TR', { minimumFractionDigits: 2 })}`, etiketler[name] || name]
                        }}
                        contentStyle={{
                            background: 'var(--renk-yuzey)',
                            border: '1px solid var(--renk-kenar)',
                            borderRadius: 'var(--radius-medium)',
                            boxShadow: 'var(--golge-2)'
                        }}
                    />
                    <Legend
                        wrapperStyle={{ paddingTop: '10px' }}
                        formatter={(value) => {
                            const etiketler = {
                                'bakim': 'Bakım',
                                'harcama': 'Harcama',
                                'yakit': 'Yakıt'
                            }
                            return etiketler[value] || value
                        }}
                    />
                    <Bar dataKey="bakim" name="bakim" stackId="a" fill="var(--renk-birincil)" />
                    <Bar dataKey="harcama" name="harcama" stackId="a" fill="var(--renk-ikincil)" />
                    <Bar dataKey="yakit" name="yakit" stackId="a" fill="var(--renk-uyari)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
}
