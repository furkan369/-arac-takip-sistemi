/**
 * Header Bileşeni - Üst başlık bar
 */
import { Menu, Bell, User } from 'lucide-react'
import styles from './Header.module.css'

export default function Header({ mobilMenuAcik, setMobilMenuAcik }) {
    return (
        <header className={styles.header}>
            <div className={styles.headerContent}>
                {/* Mobil Menü */}
                <button
                    onClick={() => setMobilMenuAcik(!mobilMenuAcik)}
                    className={styles.menuButton}
                >
                    <Menu size={24} />
                </button>

                <div style={{ flex: 1 }}></div>

                {/* Sağ Taraf */}
                <div className={styles.actions}>
                    {/* Bildirimler */}
                    <button className={styles.iconButton} title="Bildirimler">
                        <Bell size={20} />
                        <span className={styles.badge} />
                    </button>

                    {/* Profil */}
                    <button className={styles.profileButton} title="Profil">
                        <div className={styles.avatar}>
                            <User size={20} />
                        </div>
                        <div className={styles.profileInfo}>
                            <p>Kullanıcı</p>
                            <p>Yönetici</p>
                        </div>
                    </button>
                </div>
            </div>
        </header>
    )
}
