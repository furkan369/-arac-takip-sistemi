/**
 * Harcama Ekleme Formu
 * Kategori bazlı harcama girişi
 */
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { harcamaServisi, aracServisi } from '../../servisler/api'
import styles from '../Form.module.css'

// Harcama Kategorileri
const KATEGORILER = [
    'Sigorta', 'Kasko', 'Vergi', 'Muayene',
    'Lastik', 'Aksesuar', 'Yıkama', 'Otopark',
    'Ceza', 'HGS/OGS', 'Diğer'
]

// Zod Validasyon Şeması
const harcamaSema = z.object({
    arac_id: z.number({ required_error: 'Lütfen bir araç seçiniz' }),
    kategori: z.string().min(1, 'Kategori seçimi zorunludur'),
    tarih: z.string().min(1, 'Tarih zorunludur'),
    tutar: z.number({ invalid_type_error: 'Geçerli bir tutar giriniz' })
        .min(0.01, 'Tutar 0\'dan büyük olmalıdır'),
    aciklama: z.string().max(255, 'Açıklama çok uzun').optional(),
})

export default function HarcamaEkleFormu({ acik, kapat, onSuccess }) {
    const queryClient = useQueryClient()

    const { data: araclar, isLoading: araclaryukleniyor } = useQuery({
        queryKey: ['araclar'],
        queryFn: aracServisi.tumunuGetir,
        enabled: acik, // Form açıldığında veri çek
        staleTime: 1000 * 60, // 1 dakika boyunca cache'de tut
    })

    const { register, handleSubmit, formState: { errors }, reset } = useForm({
        resolver: zodResolver(harcamaSema),
        defaultValues: {
            tarih: new Date().toISOString().split('T')[0],
            aciklama: '',
        }
    })

    const mutation = useMutation({
        mutationFn: harcamaServisi.olustur,
        onSuccess: () => {
            queryClient.invalidateQueries(['harcamalar'])
            reset()
            kapat()
            if (onSuccess) onSuccess()
        }
    })

    const onSubmit = (data) => {
        mutation.mutate({
            ...data,
            arac_id: parseInt(data.arac_id),
            tutar: parseFloat(data.tutar)
        })
    }

    if (!acik) return null

    return (
        <div className={styles.overlay} onClick={() => { reset(); kapat(); }}>
            <div className={styles.modal} onClick={e => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2>Yeni Harcama Ekle</h2>
                    <button onClick={() => { reset(); kapat(); }} className={styles.closeButton}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
                    <div className={styles.field}>
                        <label htmlFor="arac_id">Araç *</label>
                        <select
                            id="arac_id"
                            {...register('arac_id', { valueAsNumber: true })}
                            className={errors.arac_id ? styles.error : ''}
                        >
                            <option value="">Araç Seçiniz</option>
                            {araclar?.map(arac => (
                                <option key={arac.id} value={arac.id}>
                                    {arac.plaka} - {arac.marka} {arac.model} {!arac.aktif_mi ? '(Pasif)' : ''}
                                </option>
                            ))}
                        </select>
                        {errors.arac_id && <span className={styles.errorMessage}>{errors.arac_id.message}</span>}
                    </div>

                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="kategori">Kategori *</label>
                            <select
                                id="kategori"
                                {...register('kategori')}
                                className={errors.kategori ? styles.error : ''}
                            >
                                <option value="">Seçiniz</option>
                                {KATEGORILER.map(k => (
                                    <option key={k} value={k}>{k}</option>
                                ))}
                            </select>
                            {errors.kategori && <span className={styles.errorMessage}>{errors.kategori.message}</span>}
                        </div>

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
                    </div>

                    <div className={styles.field}>
                        <label htmlFor="tutar">Tutar (₺) *</label>
                        <input
                            id="tutar"
                            type="number"
                            step="0.01"
                            placeholder="0.00"
                            {...register('tutar', { valueAsNumber: true })}
                            className={errors.tutar ? styles.error : ''}
                        />
                        {errors.tutar && <span className={styles.errorMessage}>{errors.tutar.message}</span>}
                    </div>

                    <div className={styles.field}>
                        <label htmlFor="aciklama">Açıklama</label>
                        <textarea
                            id="aciklama"
                            rows={3}
                            placeholder="Harcama detayı..."
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
