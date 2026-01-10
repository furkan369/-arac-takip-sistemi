import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Car, Gauge, Calendar, Palette } from 'lucide-react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { aracServisi } from '../servisler/api'
import styles from './AracKarti.module.css'

export default function AracKarti({ arac }) {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const { id, plaka, marka, model, yil, renk, km, aktif_mi } = arac

    // Aktif/Pasif durumu değiştirme
    const toggleMutation = useMutation({
        mutationFn: (yeniDurum) => aracServisi.guncelle(id, { aktif_mi: yeniDurum }),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['araclar'] })
            queryClient.refetchQueries({ queryKey: ['araclar'] })
        },
        onError: (error) => {
            console.error('Toggle hatası:', error)
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ['araclar'] })
        }
    })

    const [logoHata, setLogoHata] = React.useState(false)

    // Marka ismini normalize et (Örn: "FIAT" -> "fiat", "Mercedes-Benz" -> "mercedes")
    const normalizeMarka = (marka) => {
        if (!marka) return ''
        return marka
            .toLowerCase()
            .replace(/ğ/g, 'g')
            .replace(/ü/g, 'u')
            .replace(/ş/g, 's')
            .replace(/ı/g, 'i')
            .replace(/ö/g, 'o')
            .replace(/ç/g, 'c')
            .replace(/[^a-z0-9]/g, '') // Boşluk ve özel karakterleri sil
    }

    const handleToggle = (e) => {
        e.stopPropagation()
        toggleMutation.mutate(!aktif_mi)
    }

    return (
        <div className={styles.aracKarti}>
            {/* Header */}
            <div className={styles.header}>
                <div className={styles.aracBilgi}>
                    <div className={styles.ikonKutusu}>
                        {marka && !logoHata ? (
                            <img
                                src={`https://cdn.simpleicons.org/${normalizeMarka(marka)}`}
                                alt={`${marka} Logo`}
                                onError={() => setLogoHata(true)}
                                style={{ width: 24, height: 24, objectFit: 'contain', filter: 'var(--logo-filter)' }}
                            />
                        ) : (
                            <Car size={24} />
                        )}
                    </div>
                    <div>
                        <h3 className={styles.markaModel}>{marka} {model}</h3>
                        <p className={styles.plaka}>{plaka}</p>
                    </div>
                </div>
                <button
                    onClick={handleToggle}
                    className={`${styles.rozet} ${aktif_mi ? styles.aktif : styles.pasif}`}
                    title={aktif_mi ? 'Pasif Yap' : 'Aktif Yap'}
                    disabled={toggleMutation.isPending}
                    style={{ border: 'none', cursor: 'pointer' }}
                >
                    {toggleMutation.isPending ? '...' : aktif_mi ? 'Aktif' : 'Pasif'}
                </button>
            </div>

            {/* Detaylar (Özet) */}
            <div className={styles.ozet}>
                <div className={styles.ozetItem}>
                    <div className={styles.ozetBaslik}>
                        <Gauge size={14} style={{ marginRight: 4, verticalAlign: 'middle' }} />
                        Kilometre
                    </div>
                    <div className={styles.ozetDeger}>
                        {km ? `${km.toLocaleString('tr-TR')} km` : '-'}
                    </div>
                </div>

                {yil && (
                    <div className={styles.ozetItem}>
                        <div className={styles.ozetBaslik}>
                            <Calendar size={14} style={{ marginRight: 4, verticalAlign: 'middle' }} />
                            Yıl
                        </div>
                        <div className={styles.ozetDeger}>{yil}</div>
                    </div>
                )}
            </div>

            {/* Actions */}
            <div className={styles.actions}>
                <button
                    className={styles.detayButon}
                    onClick={() => navigate(`/araclar/${id}`)}
                >
                    Detayları Gör
                </button>
            </div>
        </div>
    )
}
