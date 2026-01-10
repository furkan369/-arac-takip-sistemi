/**
 * Araç Ekleme Formu - Material 3 Outlined Text Fields
 * Zod validasyon ile Türkçe hata mesajları
 */
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { aracServisi } from '../../servisler/api'
import styles from './AracEkleFormu.module.css'

// Zod Validasyon Şeması - Türkçe hata mesajları
const aracSema = z.object({
    plaka: z.string()
        .min(1, 'Plaka zorunludur')
        .min(7, 'Plaka en az 7 karakter olmalıdır')
        .max(20, 'Plaka en fazla 20 karakter olabilir')
        .regex(/^[0-9]{2}[A-Z]{1,3}[0-9]{1,4}$/, 'Geçerli bir plaka giriniz (örn: 34ABC123)'),

    marka: z.string()
        .min(1, 'Marka zorunludur')
        .min(2, 'Marka en az 2 karakter olmalıdır')
        .max(50, 'Marka en fazla 50 karakter olabilir'),

    model: z.string()
        .min(1, 'Model zorunludur')
        .min(2, 'Model en az 2 karakter olmalıdır')
        .max(50, 'Model en fazla 50 karakter olabilir'),

    yil: z.number({
        required_error: 'Model yılı zorunludur',
        invalid_type_error: 'Geçerli bir yıl giriniz',
    })
        .int('Yıl tam sayı olmalıdır')
        .min(1900, 'Yıl 1900\'den büyük olmalıdır')
        .max(new Date().getFullYear() + 1, `Yıl ${new Date().getFullYear() + 1}\'den küçük olmalıdır`),

    renk: z.string().optional(),
    km: z.number().int().min(0, 'Kilometre negatif olamaz').optional(),
    sase_no: z.string().max(50, 'Şase numarası en fazla 50 karakter olabilir').optional(),
    motor_no: z.string().max(50, 'Motor numarası en fazla 50 karakter olabilir').optional(),
    notlar: z.string().max(500, 'Notlar en fazla 500 karakter olabilir').optional(),
})

export default function AracEkleFormu({ acik, kapat, onSuccess }) {
    const queryClient = useQueryClient()

    const {
        register,
        handleSubmit,
        formState: { errors },
        reset,
    } = useForm({
        resolver: zodResolver(aracSema),
        defaultValues: {
            plaka: '',
            marka: '',
            model: '',
            yil: new Date().getFullYear(),
            renk: '',
            km: 0,
            sase_no: '',
            motor_no: '',
            notlar: '',
        },
    })

    // Mutation - API'ye veri gönderme
    const mutation = useMutation({
        mutationFn: aracServisi.olustur,
        onSuccess: () => {
            queryClient.invalidateQueries(['araclar'])
            reset()
            kapat()
            if (onSuccess) onSuccess()
        },
    })

    const onSubmit = (data) => {
        // Yıl'ı number'a çevir
        const formData = {
            ...data,
            yil: parseInt(data.yil),
            km: data.km ? parseInt(data.km) : 0,
        }
        mutation.mutate(formData)
    }

    const formKapat = () => {
        reset()
        kapat()
    }

    if (!acik) return null

    return (
        <div className={styles.overlay} onClick={formKapat}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div className={styles.header}>
                    <h2>Yeni Araç Ekle</h2>
                    <button onClick={formKapat} className={styles.closeButton}>
                        <X size={24} />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
                    {/* Plaka ve Marka */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="plaka">Plaka *</label>
                            <input
                                id="plaka"
                                type="text"
                                placeholder="34ABC123"
                                {...register('plaka')}
                                className={errors.plaka ? styles.error : ''}
                            />
                            {errors.plaka && (
                                <span className={styles.errorMessage}>{errors.plaka.message}</span>
                            )}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="marka">Marka *</label>
                            <input
                                id="marka"
                                type="text"
                                placeholder="Toyota"
                                {...register('marka')}
                                className={errors.marka ? styles.error : ''}
                            />
                            {errors.marka && (
                                <span className={styles.errorMessage}>{errors.marka.message}</span>
                            )}
                        </div>
                    </div>

                    {/* Model ve Yıl */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="model">Model *</label>
                            <input
                                id="model"
                                type="text"
                                placeholder="Corolla"
                                {...register('model')}
                                className={errors.model ? styles.error : ''}
                            />
                            {errors.model && (
                                <span className={styles.errorMessage}>{errors.model.message}</span>
                            )}
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="yil">Model Yılı *</label>
                            <input
                                id="yil"
                                type="number"
                                placeholder="2024"
                                {...register('yil', { valueAsNumber: true })}
                                className={errors.yil ? styles.error : ''}
                            />
                            {errors.yil && (
                                <span className={styles.errorMessage}>{errors.yil.message}</span>
                            )}
                        </div>
                    </div>

                    {/* Renk ve Kilometre */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="renk">Renk</label>
                            <input
                                id="renk"
                                type="text"
                                placeholder="Beyaz"
                                {...register('renk')}
                            />
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="km">Kilometre</label>
                            <input
                                id="km"
                                type="number"
                                placeholder="0"
                                {...register('km', { valueAsNumber: true })}
                                className={errors.km ? styles.error : ''}
                            />
                            {errors.km && (
                                <span className={styles.errorMessage}>{errors.km.message}</span>
                            )}
                        </div>
                    </div>

                    {/* Şase ve Motor No */}
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <label htmlFor="sase_no">Şase Numarası</label>
                            <input
                                id="sase_no"
                                type="text"
                                placeholder="JTDBL40E289123456"
                                {...register('sase_no')}
                            />
                        </div>

                        <div className={styles.field}>
                            <label htmlFor="motor_no">Motor Numarası</label>
                            <input
                                id="motor_no"
                                type="text"
                                placeholder="1NZ1234567"
                                {...register('motor_no')}
                            />
                        </div>
                    </div>

                    {/* Notlar */}
                    <div className={styles.field}>
                        <label htmlFor="notlar">Notlar</label>
                        <textarea
                            id="notlar"
                            rows={3}
                            placeholder="Ek bilgiler..."
                            {...register('notlar')}
                            className={errors.notlar ? styles.error : ''}
                        />
                        {errors.notlar && (
                            <span className={styles.errorMessage}>{errors.notlar.message}</span>
                        )}
                    </div>

                    {/* API Hata Mesajı */}
                    {mutation.isError && (
                        <div className={styles.apiError}>
                            {mutation.error.message}
                        </div>
                    )}

                    {/* Butonlar */}
                    <div className={styles.actions}>
                        <button
                            type="button"
                            onClick={formKapat}
                            className="btn btn-ikincil"
                            disabled={mutation.isPending}
                        >
                            İptal
                        </button>
                        <button
                            type="submit"
                            className="btn btn-birincil"
                            disabled={mutation.isPending}
                        >
                            {mutation.isPending ? 'Kaydediliyor...' : 'Kaydet'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
