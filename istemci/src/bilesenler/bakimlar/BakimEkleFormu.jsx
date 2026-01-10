/**
 * Bakım Ekleme Formu - Material 3
 * Zod validasyon ile Türkçe hata mesajları
 */
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { bakimServisi, aracServisi } from '../../servisler/api'
import styles from '../Form.module.css'

// Zod Şeması
const bakimSema = z.object({
    arac_id: z.number({ required_error: 'Araç seçimi zorunludur' }),
    bakim_turu: z.string().min(1, 'Bakım türü zorunludur'),
    tarih: z.string().min(1, 'Tarih zorunludur'),
    km: z.number().int().min(0, 'Kilometre negatif olamaz'),
    tutar: z.number().min(0, 'Tutar negatif olamaz').optional(),
    servis_yeri: z.string().optional(),
    aciklama: z.string().max(500, 'Açıklama en fazla 500 karakter olabilir').optional(),
    sonraki_bakim_km: z.number().int().min(0).optional(),
})

export default function BakimEkleFormu({ acik, kapat, onSuccess }) {
    const queryClient = useQueryClient()

    // Araçları çek
    const { data: araclar } = useQuery({
        queryKey: ['araclar'],
        queryFn: aracServisi.tumunuGetir,
        enabled: acik,
        staleTime: 1000 * 60,
    })

    const { register, handleSubmit, formState: { errors }, reset } = useForm({
        resolver: zodResolver(bakimSema),
        defaultValues: {
            tarih: new Date().toISOString().split('T')[0],
            km: 0,
            tutar: 0,
        },
    })

    const mutation = useMutation({
        mutationFn: bakimServisi.olustur,
        onSuccess: () => {
            queryClient.invalidateQueries(['bakimlar'])
            reset()
            kapat()
            if (onSuccess) onSuccess()
        },
    })

    const onSubmit = (data) => {
        const formData = {
            ...data,
            arac_id: parseInt(data.arac_id),
            km: parseInt(data.km),
            tutar: data.tutar ? parseFloat(data.tutar) : undefined,
            sonraki_bakim_km: data.sonraki_bakim_km ? parseInt(data.sonraki_bakim_km) : undefined,
        }
        mutation.mutate(formData)
    }

    if (!acik) return null

    return (
        <div className={styles.overlay} onClick={() => { reset(); kapat(); }}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2>Yeni Bakım Kaydı Ekle</h2>
                    <button onClick={() => { reset(); kapat(); }} className={styles.closeButton}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="arac_id">Araç *</label>
                            <select
                                id="arac_id"
                                {...register('arac_id', { valueAsNumber: true })}
                                className={errors.arac_id ? styles.error : ''}
                            >
                                <option value="">Araç Seçin</option>
                                {araclar?.map(arac => (
                                    <option key={arac.id} value={arac.id}>
                                        {arac.plaka} - {arac.marka} {arac.model}
                                    </option>
                                ))}
                            </select>
                            {errors.arac_id && <span className={styles.errorMessage}>{errors.arac_id.message}</span>}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="bakim_turu">Bakım Türü *</label>
                            <input
                                id="bakim_turu"
                                type="text"
                                placeholder="Yağ Değişimi"
                                {...register('bakim_turu')}
                                className={errors.bakim_turu ? styles.error : ''}
                            />
                            {errors.bakim_turu && <span className={styles.errorMessage}>{errors.bakim_turu.message}</span>}
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="tarih">Tarih *</label>
                            <input
                                id="tarih"
                                type="date"
                                {...register('tarih')}
                                className={errors.tarih ? styles.error : ''}
                            />
                            {errors.tarih && <span className={styles.errorMessage}>{errors.tarih.message}</span>}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="km">Kilometre *</label>
                            <input
                                id="km"
                                type="number"
                                placeholder="50000"
                                {...register('km', { valueAsNumber: true })}
                                className={errors.km ? styles.error : ''}
                            />
                            {errors.km && <span className={styles.errorMessage}>{errors.km.message}</span>}
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="tutar">Tutar (₺)</label>
                            <input
                                id="tutar"
                                type="number"
                                step="0.01"
                                placeholder="500.00"
                                {...register('tutar', { valueAsNumber: true })}
                            />
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="servis_yeri">Servis Yeri</label>
                            <input
                                id="servis_yeri"
                                type="text"
                                placeholder="ABC Oto Servis"
                                {...register('servis_yeri')}
                            />
                        </div>
                    </div>

                    <div className={styles.field}>
                        <label htmlFor="sonraki_bakim_km">Sonraki Bakım KM</label>
                        <input
                            id="sonraki_bakim_km"
                            type="number"
                            placeholder="60000"
                            {...register('sonraki_bakim_km', { valueAsNumber: true })}
                        />
                    </div>

                    <div className={styles.field}>
                        <label htmlFor="aciklama">Açıklama</label>
                        <textarea
                            id="aciklama"
                            rows={3}
                            placeholder="Bakım detayları..."
                            {...register('aciklama')}
                        />
                    </div>

                    {mutation.isError && (
                        <div className={styles.apiError}>{mutation.error.message}</div>
                    )}

                    <div className={styles.actions}>
                        <button type="button" onClick={() => { reset(); kapat(); }} className="btn btn-ikincil">
                            İptal
                        </button>
                        <button type="submit" className="btn btn-birincil" disabled={mutation.isPending}>
                            {mutation.isPending ? 'Kaydediliyor...' : 'Kaydet'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
