/**
 * Profil ve Ayarlar Sayfası
 * Kullanıcı bilgileri ve şifre değiştirme
 */
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { profilServisi } from '../servisler/api'
import { User, Shield, Key, Save, Mail, AlertCircle, Loader2 } from 'lucide-react'
import styles from './Ayarlar.module.css'

export default function Ayarlar() {
    const queryClient = useQueryClient()

    // Profil Form State
    const [profilForm, setProfilForm] = useState({ ad_soyad: '' })
    const [profilMesaj, setProfilMesaj] = useState({ tip: '', metin: '' })

    // Şifre Form State
    const [sifreForm, setSifreForm] = useState({ eski_sifre: '', yeni_sifre: '' })
    const [sifreMesaj, setSifreMesaj] = useState({ tip: '', metin: '' })

    // Kullanıcı Bilgilerini Getir
    const { data: kullanici, isLoading } = useQuery({
        queryKey: ['me'],
        queryFn: profilServisi.getir,
        staleTime: Infinity
    })

    // Bilgiler yüklenince form'u doldur
    useEffect(() => {
        if (kullanici) {
            setProfilForm({ ad_soyad: kullanici.ad_soyad })
        }
    }, [kullanici])

    // Profil Güncelleme
    const profilMutation = useMutation({
        mutationFn: profilServisi.guncelle,
        onSuccess: () => {
            queryClient.invalidateQueries(['me'])
            setProfilMesaj({ tip: 'basari', metin: 'Profil bilgileri güncellendi ✅' })
            setTimeout(() => setProfilMesaj({ tip: '', metin: '' }), 3000)
        },
        onError: (err) => {
            setProfilMesaj({ tip: 'hata', metin: err.response?.data?.detail || 'Güncelleme başarısız' })
        }
    })

    // Şifre Değiştirme
    const sifreMutation = useMutation({
        mutationFn: profilServisi.sifreDegistir,
        onSuccess: () => {
            setSifreForm({ eski_sifre: '', yeni_sifre: '' })
            setSifreMesaj({ tip: 'basari', metin: 'Şifreniz başarıyla değiştirildi ✅' })
            setTimeout(() => setSifreMesaj({ tip: '', metin: '' }), 3000)
        },
        onError: (err) => {
            setSifreMesaj({ tip: 'hata', metin: err.response?.data?.detail || 'Şifre değiştirilemedi' })
        }
    })

    const handleProfilSubmit = (e) => {
        e.preventDefault()
        if (!profilForm.ad_soyad) return
        profilMutation.mutate(profilForm)
    }

    const handleSifreSubmit = (e) => {
        e.preventDefault()
        if (!sifreForm.eski_sifre || !sifreForm.yeni_sifre) {
            setSifreMesaj({ tip: 'hata', metin: 'Lütfen tüm alanları doldurun' })
            return
        }
        if (sifreForm.yeni_sifre.length < 6) {
            setSifreMesaj({ tip: 'hata', metin: 'Yeni şifre en az 6 karakter olmalı' })
            return
        }
        sifreMutation.mutate(sifreForm)
    }

    if (isLoading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                <Loader2 className="animate-spin" size={32} color="var(--renk-birincil)" />
            </div>
        )
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Hesap Ayarları</h1>
                <p>Kişisel bilgilerinizi ve güvenliğinizi yönetin.</p>
            </div>

            <div className={styles.grid}>
                {/* Profil Kartı (Sol Panel) */}
                <div className={styles.profileCard}>
                    <div className={styles.avatar}>
                        <User size={48} />
                    </div>
                    <h2 className={styles.profileName}>{kullanici?.ad_soyad}</h2>
                    <p className={styles.profileEmail}>{kullanici?.email}</p>

                    <div className={styles.roleBadge}>
                        {kullanici?.rol === 'admin' ? (
                            <><Shield size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> Yönetici</>
                        ) : (
                            <><User size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> Müşteri</>
                        )}
                    </div>
                </div>

                {/* Ayarlar Formları (Sağ Panel) */}
                <div className={styles.settingsCard}>

                    {/* Profil Bilgileri */}
                    <div className={styles.section}>
                        <div className={styles.sectionTitle}>
                            <User size={20} />
                            Profil Bilgileri
                        </div>

                        {profilMesaj.metin && (
                            <div className={profilMesaj.tip === 'hata' ? styles.errorMessage : styles.successMessage}>
                                {profilMesaj.tip === 'hata' && <AlertCircle size={18} />}
                                {profilMesaj.metin}
                            </div>
                        )}

                        <form onSubmit={handleProfilSubmit}>
                            <div className={styles.formGroup}>
                                <label>Ad Soyad</label>
                                <input
                                    type="text"
                                    value={profilForm.ad_soyad}
                                    onChange={e => setProfilForm({ ...profilForm, ad_soyad: e.target.value })}
                                />
                            </div>

                            <div className={styles.formGroup}>
                                <label>E-posta Adresi</label>
                                <input
                                    type="email"
                                    value={kullanici?.email || ''}
                                    disabled
                                    title="E-posta adresi değiştirilemez"
                                />
                                <small style={{ color: 'var(--renk-metin-ikincil)', marginTop: 4, display: 'block' }}>
                                    Güvenlik nedeniyle e-posta adresi değiştirilemez.
                                </small>
                            </div>

                            <button
                                type="submit"
                                className={styles.button}
                                disabled={profilMutation.isPending || profilForm.ad_soyad === kullanici?.ad_soyad}
                            >
                                {profilMutation.isPending ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
                                Değişiklikleri Kaydet
                            </button>
                        </form>
                    </div>

                    {/* Şifre Değiştirme */}
                    <div className={styles.section}>
                        <div className={styles.sectionTitle}>
                            <Key size={20} />
                            Güvenlik ve Şifre
                        </div>

                        {sifreMesaj.metin && (
                            <div className={sifreMesaj.tip === 'hata' ? styles.errorMessage : styles.successMessage}>
                                {sifreMesaj.tip === 'hata' && <AlertCircle size={18} />}
                                {sifreMesaj.metin}
                            </div>
                        )}

                        <form onSubmit={handleSifreSubmit}>
                            <div className={styles.formGroup}>
                                <label>Mevcut Şifre</label>
                                <input
                                    type="password"
                                    value={sifreForm.eski_sifre}
                                    onChange={e => setSifreForm({ ...sifreForm, eski_sifre: e.target.value })}
                                    placeholder="••••••••"
                                />
                            </div>

                            <div className={styles.formGroup}>
                                <label>Yeni Şifre</label>
                                <input
                                    type="password"
                                    value={sifreForm.yeni_sifre}
                                    onChange={e => setSifreForm({ ...sifreForm, yeni_sifre: e.target.value })}
                                    placeholder="En az 6 karakter"
                                />
                            </div>

                            <button
                                type="submit"
                                className={styles.button}
                                disabled={sifreMutation.isPending}
                            >
                                {sifreMutation.isPending ? <Loader2 className="animate-spin" size={18} /> : <Shield size={18} />}
                                Şifreyi Güncelle
                            </button>
                        </form>
                    </div>

                </div>
            </div>
        </div>
    )
}
