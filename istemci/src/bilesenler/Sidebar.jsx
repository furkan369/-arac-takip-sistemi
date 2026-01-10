/**
 * Sidebar Bileşeni - Sol menü navigasyonu
 */
import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
    LayoutDashboard, Car, Wrench, Receipt, Fuel, Bell,
    ChevronLeft, ChevronRight, LogOut, Users, Settings,
    Moon, Sun
} from 'lucide-react'
import { useTema } from '../context/TemaContext'
import styles from './Sidebar.module.css'

export default function Sidebar({ acik, setAcik, mobilMenu = false }) {
    const location = useLocation()
    const navigate = useNavigate()
    const { tema, temaDegistir } = useTema()

    const menuler = [
        { isim: 'Genel Bakış', yol: '/genel-bakis', ikon: LayoutDashboard },
        { isim: 'Bakımlar', yol: '/bakimlar', ikon: Wrench },
        { isim: 'Harcamalar', yol: '/harcamalar', ikon: Receipt },
        { isim: 'Yakıt Takibi', yol: '/yakit', ikon: Fuel },
        { isim: 'Hatırlatıcılar', yol: '/hatirlaticilar', ikon: Bell },
        { isim: 'Ayarlar', yol: '/ayarlar', ikon: Settings },
    ]

    // Admin menüsü
    const rol = localStorage.getItem('rol')
    if (rol === 'admin') {
        menuler.splice(1, 0, { isim: 'Kullanıcılar', yol: '/kullanicilar', ikon: Users })
    }

    const aktifMi = (yol) => location.pathname === yol

    const cikisYap = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('rol')
        // Temayı silme, kalsın
        navigate('/giris')
    }

    return (
        <div className={styles.sidebar}>
            {/* Logo ve Başlık */}
            <div className={styles.logoSection}>
                {acik ? (
                    <>
                        <div className={styles.logoContent}>
                            <div className={styles.logoIcon}>
                                <Car size={24} color="white" />
                            </div>
                            <div className={styles.logoText}>
                                <h1>Araç Takip</h1>
                                <p>Yönetim Sistemi</p>
                            </div>
                        </div>
                        {!mobilMenu && (
                            <button onClick={() => setAcik(false)} className={styles.toggleButton}>
                                <ChevronLeft size={20} />
                            </button>
                        )}
                    </>
                ) : (
                    <button onClick={() => setAcik(true)} className={styles.toggleButton}>
                        <ChevronRight size={20} />
                    </button>
                )}
            </div>

            {/* Menü */}
            <nav className={styles.menu}>
                {menuler.map((menu) => {
                    const Ikon = menu.ikon
                    const aktif = aktifMi(menu.yol)

                    return (
                        <Link
                            key={menu.yol}
                            to={menu.yol}
                            className={`${styles.menuItem} ${aktif ? styles.aktif : ''} ${!acik ? styles.kapali : ''}`}
                            title={!acik ? menu.isim : ''}
                        >
                            <Ikon size={20} />
                            {acik && <span>{menu.isim}</span>}
                            {aktif && acik && <div className={styles.aktifGosterge} />}
                        </Link>
                    )
                })}
            </nav>

            {/* Tema Değiştirici */}
            <div style={{ padding: '0 12px 12px 12px', marginTop: 'auto' }}>
                <button
                    onClick={temaDegistir}
                    className={`${styles.menuItem} ${!acik ? styles.kapali : ''}`}
                    style={{
                        background: 'transparent',
                        border: '1px solid var(--renk-outline-variant)',
                        cursor: 'pointer',
                        width: '100%',
                        color: 'var(--renk-metin-birincil)',
                        justifyContent: acik ? 'flex-start' : 'center'
                    }}
                    title={!acik ? (tema === 'acik' ? 'Koyu Mod' : 'Aydınlık Mod') : ''}
                >
                    {tema === 'acik' ? <Moon size={20} /> : <Sun size={20} />}
                    {acik && <span>{tema === 'acik' ? 'Koyu Mod' : 'Aydınlık Mod'}</span>}
                </button>
            </div>

            {/* Çıkış Butonu */}
            <div style={{ padding: '0 12px 12px 12px', position: 'relative', zIndex: 999 }}>
                <div
                    onClick={cikisYap}
                    className={`${styles.menuItem} ${!acik ? styles.kapali : ''}`}
                    style={{
                        color: '#ff4d4d',
                        cursor: 'pointer',
                        border: '1px solid rgba(255, 77, 77, 0.2)',
                        backgroundColor: 'rgba(255, 77, 77, 0.05)',
                        position: 'relative',
                        zIndex: 1000,
                        justifyContent: acik ? 'flex-start' : 'center'
                    }}
                    title={!acik ? "Çıkış Yap" : ''}
                >
                    <LogOut size={20} />
                    {acik && <span style={{ fontWeight: 600 }}>Çıkış Yap</span>}
                </div>
            </div>

            {/* Footer */}
            {acik && (
                <div className={styles.footer}>
                    <p>Versiyon 2.0.0</p>
                    <p>© 2026 Vibe Araç</p>
                </div>
            )}
        </div>
    )
}
