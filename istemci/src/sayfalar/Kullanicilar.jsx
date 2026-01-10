/**
 * Kullanıcı Yönetimi Sayfası (Sadece Admin)
 * Müşteri listesi, ekleme ve silme işlemleri
 */
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { kullaniciServisi } from '../servisler/api'
import {
    Users, UserPlus, Trash2, Search, X, Loader2, Shield, User, AlertCircle
} from 'lucide-react'
import styles from './Kullanicilar.module.css'

export default function Kullanicilar() {
    const queryClient = useQueryClient()
    const [aramaMetni, setAramaMetni] = useState('')
    const [modalAcik, setModalAcik] = useState(false)

    // Form State
    const [formData, setFormData] = useState({
        ad_soyad: '',
        email: '',
        sifre: '',
        rol: 'kullanici' // Varsayılan rol
    })
    const [formHata, setFormHata] = useState('')

    // Kullanıcıları Getir
    const { data: kullanicilar = [], isLoading } = useQuery({
        queryKey: ['kullanicilar'],
        queryFn: kullaniciServisi.tumunuGetir,
        staleTime: 5000 // 5 saniye cache
    })

    // Kullanıcı Ekle Mutation
    const ekleMutation = useMutation({
        mutationFn: kullaniciServisi.olustur,
        onSuccess: () => {
            queryClient.invalidateQueries(['kullanicilar'])
            modalKapat()
            alert('Kullanıcı başarıyla oluşturuldu! ✅')
        },
        onError: (err) => {
            setFormHata(err.response?.data?.detail || 'Kullanıcı oluşturulurken bir hata oluştu')
        }
    })

    // Kullanıcı Sil Mutation
    const silMutation = useMutation({
        mutationFn: kullaniciServisi.sil,
        onSuccess: () => {
            queryClient.invalidateQueries(['kullanicilar'])
        },
        onError: (err) => {
            alert(err.response?.data?.detail || 'Kullanıcı silinemedi')
        }
    })

    // Filtreleme
    const filtrelenmisKullanicilar = kullanicilar.filter(k =>
        k.ad_soyad.toLowerCase().includes(aramaMetni.toLowerCase()) ||
        k.email.toLowerCase().includes(aramaMetni.toLowerCase())
    )

    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        setFormHata('')

        if (!formData.ad_soyad || !formData.email || !formData.sifre) {
            setFormHata('Lütfen tüm zorunlu alanları doldurun')
            return
        }

        if (formData.sifre.length < 6) {
            setFormHata('Şifre en az 6 karakter olmalıdır')
            return
        }

        ekleMutation.mutate(formData)
    }

    const modalKapat = () => {
        setModalAcik(false)
        setFormData({ ad_soyad: '', email: '', sifre: '', rol: 'kullanici' })
        setFormHata('')
    }

    const silOnayla = (id, ad_soyad) => {
        if (window.confirm(`${ad_soyad} kullanıcısını silmek istediğinize emin misiniz? Bu işlem geri alınamaz!`)) {
            silMutation.mutate(id)
        }
    }

    return (
        <div className={styles.container}>
            {/* Header */}
            <div className={styles.header}>
                <div className={styles.title}>
                    <h1>Kullanıcı Yönetimi</h1>
                    <p>Müşterileri görüntüleyin, ekleyin veya yönetin.</p>
                </div>
                <button
                    onClick={() => setModalAcik(true)}
                    className={styles.addButton}
                >
                    <UserPlus size={20} />
                    Yeni Kullanıcı Ekle
                </button>
            </div>

            {/* Arama ve Tablo Kartı */}
            <div className={styles.card}>
                {/* Arama Bar */}
                <div style={{ padding: '16px', borderBottom: '1px solid var(--renk-outline-variant)' }}>
                    <div style={{
                        display: 'flex', alignItems: 'center', gap: '8px',
                        background: 'var(--renk-yuzey)', padding: '8px 12px',
                        borderRadius: 'var(--radius-lg)', border: '1px solid var(--renk-outline)',
                        maxWidth: '300px'
                    }}>
                        <Search size={18} color="var(--renk-metin-ikincil)" />
                        <input
                            type="text"
                            placeholder="İsim veya e-posta ara..."
                            value={aramaMetni}
                            onChange={(e) => setAramaMetni(e.target.value)}
                            style={{ border: 'none', background: 'transparent', outline: 'none', width: '100%' }}
                        />
                    </div>
                </div>

                {/* Tablo */}
                <div className={styles.tableContainer}>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th>Kullanıcı</th>
                                <th>E-posta</th>
                                <th>Rol</th>
                                <th>Durum</th>
                                <th>Kayıt Tarihi</th>
                                <th style={{ textAlign: 'right' }}>İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            {isLoading ? (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '40px' }}>
                                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}>
                                            <Loader2 className="animate-spin" size={20} />
                                            Yükleniyor...
                                        </div>
                                    </td>
                                </tr>
                            ) : filtrelenmisKullanicilar.length === 0 ? (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '40px', color: 'var(--renk-metin-ikincil)' }}>
                                        Kullanıcı bulunamadı.
                                    </td>
                                </tr>
                            ) : (
                                filtrelenmisKullanicilar.map((kullanici) => (
                                    <tr key={kullanici.id}>
                                        <td>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                                <div style={{
                                                    width: '32px', height: '32px', borderRadius: '50%',
                                                    background: 'var(--renk-yuzey-variant)', display: 'flex',
                                                    alignItems: 'center', justifyContent: 'center'
                                                }}>
                                                    <User size={16} />
                                                </div>
                                                <span style={{ fontWeight: 500 }}>{kullanici.ad_soyad}</span>
                                            </div>
                                        </td>
                                        <td>{kullanici.email}</td>
                                        <td>
                                            <span className={`${styles.badge} ${kullanici.rol === 'admin' ? styles.admin : styles.kullanici}`}>
                                                {kullanici.rol === 'admin' ? (
                                                    <><Shield size={12} style={{ marginRight: 4 }} /> Admin</>
                                                ) : (
                                                    <><User size={12} style={{ marginRight: 4 }} /> Müşteri</>
                                                )}
                                            </span>
                                        </td>
                                        <td>
                                            {kullanici.aktif_mi ? (
                                                <span style={{ color: 'var(--renk-basari)', fontSize: '12px', fontWeight: 600 }}>AKTİF</span>
                                            ) : (
                                                <span style={{ color: 'var(--renk-metin-ikincil)', fontSize: '12px' }}>PASİF</span>
                                            )}
                                        </td>
                                        <td>
                                            {new Date(kullanici.olusturulma_tarihi).toLocaleDateString('tr-TR')}
                                        </td>
                                        <td style={{ textAlign: 'right' }}>
                                            <button
                                                onClick={() => silOnayla(kullanici.id, kullanici.ad_soyad)}
                                                className={styles.deleteButton}
                                                title="Sil"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Yeni Kullanıcı Modal */}
            {modalAcik && (
                <div className={styles.modalOverlay} onClick={modalKapat}>
                    <div className={styles.modal} onClick={e => e.stopPropagation()}>
                        <div className={styles.modalHeader}>
                            <h2>Yeni Kullanıcı Ekle</h2>
                            <button onClick={modalKapat} className={styles.closeButton}>
                                <X size={20} />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit}>
                            <div className={styles.modalBody}>
                                {formHata && (
                                    <div className={styles.errorMessage}>
                                        <AlertCircle size={18} />
                                        {formHata}
                                    </div>
                                )}

                                <div className={styles.formGroup}>
                                    <label>Ad Soyad</label>
                                    <input
                                        type="text"
                                        name="ad_soyad"
                                        value={formData.ad_soyad}
                                        onChange={handleInputChange}
                                        placeholder="Örn: Ahmet Yılmaz"
                                        autoFocus
                                    />
                                </div>

                                <div className={styles.formGroup}>
                                    <label>E-posta Adresi</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        placeholder="ornek@sirket.com"
                                    />
                                </div>

                                <div className={styles.formGroup}>
                                    <label>Şifre</label>
                                    <input
                                        type="text"
                                        name="sifre"
                                        value={formData.sifre}
                                        onChange={handleInputChange}
                                        placeholder="Güvenli bir şifre belirleyin"
                                    />
                                </div>

                                <div className={styles.formGroup}>
                                    <label>Rol</label>
                                    <select
                                        name="rol"
                                        value={formData.rol}
                                        onChange={handleInputChange}
                                    >
                                        <option value="kullanici">Müşteri (Standart)</option>
                                        <option value="admin">Yönetici (Admin)</option>
                                    </select>
                                </div>
                            </div>

                            <div className={styles.modalFooter}>
                                <button type="button" onClick={modalKapat} className={styles.cancelButton}>
                                    İptal
                                </button>
                                <button
                                    type="submit"
                                    className={styles.submitButton}
                                    disabled={ekleMutation.isPending}
                                >
                                    {ekleMutation.isPending ? 'Ekleniyor...' : 'Kullanıcıyı Ekle'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
}
