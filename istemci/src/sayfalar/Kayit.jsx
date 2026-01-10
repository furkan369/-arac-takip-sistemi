/**
 * Register Sayfası
 * VibeUI 2.0 Split Screen Tasarım
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authServisi } from '../servisler/api';
import { UserPlus, Mail, Lock, User, Car, ArrowRight } from 'lucide-react';
import styles from './Auth.module.css';

export default function Kayit() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [adSoyad, setAdSoyad] = useState('');
    const [sifre, setSifre] = useState('');
    const [sifreTekrar, setSifreTekrar] = useState('');
    const [hata, setHata] = useState('');

    const kayitMutation = useMutation({
        mutationFn: () => authServisi.kayit(email, adSoyad, sifre),
        onSuccess: async () => {
            try {
                await authServisi.giris(email, sifre);
                navigate('/genel-bakis');
            } catch (error) {
                navigate('/giris');
            }
        },
        onError: (error) => {
            setHata(error.message || 'Kayıt başarısız. Lütfen tekrar deneyin.');
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setHata('');

        if (!email || !adSoyad || !sifre || !sifreTekrar) {
            setHata('Lütfen tüm alanları doldurun');
            return;
        }
        if (sifre.length < 6) {
            setHata('Şifre en az 6 karakter olmalıdır');
            return;
        }
        if (sifre !== sifreTekrar) {
            setHata('Şifreler eşleşmiyor');
            return;
        }
        if (!email.includes('@')) {
            setHata('Geçerli bir e-posta adresi girin');
            return;
        }

        kayitMutation.mutate();
    };

    return (
        <div className={styles.authContainer}>
            {/* Sol Panel - Vitrin */}
            <div className={styles.authLeft}>
                <div className={styles.brandArea}>
                    <div className={styles.brandLogo}>
                        <Car size={32} color="white" />
                    </div>
                    <h1 className={styles.heroTitle}>Aramıza Katıl.</h1>
                    <p className={styles.heroDescription}>
                        Binlerce mutlu kullanıcıya katılın ve araç masraflarınızı kontrol altına almaya bugün başlayın.
                    </p>
                </div>
            </div>

            {/* Sağ Panel - Form */}
            <div className={styles.authRight}>
                <div className={styles.authCard}>
                    <div className={styles.authHeader}>
                        <h1>Hesap Oluştur</h1>
                        <p>Hızlıca kayıt olun ve sistemi kullanmaya başlayın.</p>
                    </div>

                    <form onSubmit={handleSubmit} className={styles.authForm}>
                        <div className={styles.formGroup}>
                            <label htmlFor="adSoyad">Ad Soyad</label>
                            <input
                                id="adSoyad"
                                type="text"
                                value={adSoyad}
                                onChange={(e) => setAdSoyad(e.target.value)}
                                placeholder="Adınız Soyadınız"
                                disabled={kayitMutation.isPending}
                                autoFocus
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="email">E-posta Adresi</label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="ornek@sirket.com"
                                disabled={kayitMutation.isPending}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="sifre">Şifre</label>
                            <input
                                id="sifre"
                                type="password"
                                value={sifre}
                                onChange={(e) => setSifre(e.target.value)}
                                placeholder="En az 6 karakter"
                                disabled={kayitMutation.isPending}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="sifreTekrar">Şifre Tekrar</label>
                            <input
                                id="sifreTekrar"
                                type="password"
                                value={sifreTekrar}
                                onChange={(e) => setSifreTekrar(e.target.value)}
                                placeholder="Şifrenizi doğrulayın"
                                disabled={kayitMutation.isPending}
                            />
                        </div>

                        {hata && (
                            <div className={styles.errorMessage}>
                                {hata}
                            </div>
                        )}

                        <button
                            type="submit"
                            className={styles.submitButton}
                            disabled={kayitMutation.isPending}
                        >
                            {kayitMutation.isPending ? 'Oluşturuluyor...' : 'Hesap Oluştur'}
                            {!kayitMutation.isPending && <UserPlus size={20} />}
                        </button>

                        <div className={styles.authFooter}>
                            Zaten hesabınız var mı?
                            <Link to="/giris" className={styles.link}>
                                Giriş Yapın
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
