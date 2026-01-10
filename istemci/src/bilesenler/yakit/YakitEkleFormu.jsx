/**
 * Yakıt Ekleme Formu
 * Litre x Fiyat hesaplamalı
 */
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { yakitServisi, aracServisi } from '../../servisler/api'
import styles from '../Form.module.css'

const YAKIT_TURLERI = ['Benzin', 'Dizel', 'LPG', 'Elektrik']

// Zod Şeması
const yakitSema = z.object({
    arac_id: z.number({ required_error: 'Araç seçimi zorunludur' }),
    tarih: z.string().min(1, 'Tarih zorunludur'),
    km: z.number({ invalid_type_error: 'KM sayı olmalıdır' }).min(0, 'KM negatif olamaz'),
    litre: z.number({ invalid_type_error: 'Litre sayı olmalıdır' }).min(0.1, 'Geçerli litre giriniz'),
    fiyat: z.number({ invalid_type_error: 'Fiyat sayı olmalıdır' }).min(0.1, 'Birim fiyat giriniz'),
    yakit_turu: z.string().min(1, 'Yakıt türü seçiniz'),
    tam_depo: z.boolean(),
    istasyon: z.string().optional(),
})

export default function YakitEkleFormu({ acik, kapat, onSuccess }) {
    const queryClient = useQueryClient()

    const { data: araclar } = useQuery({
        queryKey: ['araclar'],
        queryFn: aracServisi.tumunuGetir,
        enabled: acik,
        staleTime: 1000 * 60,
    })

    const { register, handleSubmit, watch, setValue, formState: { errors }, reset } = useForm({
        resolver: zodResolver(yakitSema),
        defaultValues: {
            tarih: new Date().toISOString().split('T')[0],
            tam_depo: true,
            yakit_turu: 'Benzin',
        }
    })

    // Anlık Hesaplama için değerleri izle
    const litre = watch('litre')
    const fiyat = watch('fiyat')
    const toplamTutar = (litre && fiyat) ? (litre * fiyat).toFixed(2) : '0.00'

    // Araç değişince yakıt türünü güncelleme mantığı eklenebilir
    const secilenAracId = watch('arac_id')

    // Form submit
    const mutation = useMutation({
        mutationFn: yakitServisi.olustur,
        onSuccess: () => {
            queryClient.invalidateQueries(['yakit'])
            reset()
            kapat()
            if (onSuccess) onSuccess()
        }
    })

    const onSubmit = (data) => {
        mutation.mutate({
            ...data,
            arac_id: parseInt(data.arac_id),
            km: parseInt(data.km),
            litre: parseFloat(data.litre),
            fiyat: parseFloat(data.fiyat)
        })
    }

    if (!acik) return null

    return (
        <div className={styles.overlay} onClick={() => { reset(); kapat(); }}>
            <div className={styles.modal} onClick={e => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2>Yeni Yakıt Kaydı Ekle</h2>
                    <button onClick={() => { reset(); kapat(); }} className={styles.closeButton}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
                    {/* Araç ve Tarih */}
                    <div className={styles.row}>
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
                                        {arac.plaka} - {arac.marka} {!arac.aktif_mi ? '(Pasif)' : ''}
                                    </option>
                                ))}
                            </select>
                            {errors.arac_id && <span className={styles.errorMessage}>{errors.arac_id.message}</span>}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="tarih">Tarih *</label>
                            <input
                                id="tarih"
                                type="date"
                                {...register('tarih')}
                                className={errors.tarih ? styles.error : ''}
                            />
                        </div>
                    </div>

                    {/* KM ve Yakıt Türü */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="km">Güncel KM *</label>
                            <input
                                id="km"
                                type="number"
                                placeholder="50123"
                                {...register('km', { valueAsNumber: true })}
                                className={errors.km ? styles.error : ''}
                            />
                            {errors.km && <span className={styles.errorMessage}>{errors.km.message}</span>}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="yakit_turu">Yakıt Türü *</label>
                            <select
                                id="yakit_turu"
                                {...register('yakit_turu')}
                            >
                                {YAKIT_TURLERI.map(tur => (
                                    <option key={tur} value={tur}>{tur}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {/* Litre ve Fiyat */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="litre">Alınan Litre *</label>
                            <input
                                id="litre"
                                type="number"
                                step="0.01"
                                placeholder="45.5"
                                {...register('litre', { valueAsNumber: true })}
                                className={errors.litre ? styles.error : ''}
                            />
                            {errors.litre && <span className={styles.errorMessage}>{errors.litre.message}</span>}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="fiyat">Birim Fiyat (₺/Lt) *</label>
                            <input
                                id="fiyat"
                                type="number"
                                step="0.01"
                                placeholder="40.50"
                                {...register('fiyat', { valueAsNumber: true })}
                                className={errors.fiyat ? styles.error : ''}
                            />
                            {errors.fiyat && <span className={styles.errorMessage}>{errors.fiyat.message}</span>}
                        </div>
                    </div>

                    {/* Hesaplanan Toplam Tutar (Salt Okunur) */}
                    <div className={styles.field} style={{ background: 'var(--renk-yuzey-variant)', padding: '12px', borderRadius: '8px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <label style={{ margin: 0 }}>Toplam Tutar:</label>
                            <span style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--renk-birincil)' }}>
                                ₺{toplamTutar}
                            </span>
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="istasyon">İstasyon</label>
                            <input
                                id="istasyon"
                                type="text"
                                placeholder="Shell Maslak"
                                {...register('istasyon')}
                            />
                        </div>

                        <div className={styles.field} style={{ flexDirection: 'row', alignItems: 'center', paddingTop: '30px' }}>
                            <input
                                id="tam_depo"
                                type="checkbox"
                                {...register('tam_depo')}
                                style={{ width: '20px', height: '20px', margin: 0 }}
                            />
                            <label htmlFor="tam_depo" style={{ marginBottom: 0, cursor: 'pointer' }}>Depo Fullendi</label>
                        </div>
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
