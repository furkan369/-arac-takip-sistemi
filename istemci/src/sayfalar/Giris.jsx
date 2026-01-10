/**
 * Login Sayfası
 * VibeUI 2.0 Split Screen Tasarım
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authServisi } from '../servisler/api';
import { LogIn, Mail, Lock, Car, ArrowRight } from 'lucide-react';
import styles from './Auth.module.css';

export default function Giris() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [sifre, setSifre] = useState('');
    const [hata, setHata] = useState('');

    const girisMutation = useMutation({
        mutationFn: () => authServisi.giris(email, sifre),
        onSuccess: () => {
            // alert('Giriş başarılı! Yönlendiriliyor...'); // Debug - Başarılı olunca rahatsız etmesin
            navigate('/genel-bakis');
        },
        onError: (error) => {
            const mesaj = error.message || 'Giriş başarısız.';
            // alert('HATA: ' + mesaj); // Telefondan hatayı görmek için
            setHata(mesaj);
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setHata('');

        // alert('Giriş butonuna basıldı. İşleniyor...'); // Debug

        if (!email || !sifre) {
            setHata('Lütfen tüm alanları doldurun');
            return;
        }
        girisMutation.mutate();
    };

    return (
        <div className={styles.authContainer}>
            {/* Sol Panel - Vitrin */}
            <div className={styles.authLeft}>
                <div className={styles.brandArea}>
                    <div className={styles.brandLogo}>
                        <Car size={32} color="white" />
                    </div>
                    <h1 className={styles.heroTitle}>Kontrol Sende.</h1>
                    <p className={styles.heroDescription}>
                        Araç bakım, yakıt ve harcamalarınızı tek yerden, zahmetsizce yönetin.
                        Vibe ile filonuzun hakimi olun.
                    </p>
                </div>
            </div>

            {/* Sağ Panel - Form */}
            <div className={styles.authRight}>
                <div className={styles.authCard}>
                    <div className={styles.authHeader}>
                        <h1>Tekrar Hoş Geldiniz</h1>
                        <p>Hesabınıza giriş yaparak devam edin.</p>
                    </div>

                    <form onSubmit={handleSubmit} className={styles.authForm}>
                        <div className={styles.formGroup}>
                            <label htmlFor="email">E-posta Adresi</label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="ornek@sirket.com"
                                disabled={girisMutation.isPending}
                                autoFocus
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="sifre">Şifre</label>
                            <input
                                id="sifre"
                                type="password"
                                value={sifre}
                                onChange={(e) => setSifre(e.target.value)}
                                placeholder="••••••••"
                                disabled={girisMutation.isPending}
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
                            disabled={girisMutation.isPending}
                        >
                            {girisMutation.isPending ? 'Giriş yapılıyor...' : 'Giriş Yap'}
                            {!girisMutation.isPending && <ArrowRight size={20} />}
                        </button>

                        <div className={styles.authFooter}>
                            Hesabınız yok mu?
                            <Link to="/kayit" className={styles.link}>
                                Hemen Kayıt Olun
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
