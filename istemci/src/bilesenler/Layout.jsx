/**
 * Ana Layout Bileşeni
 * Sidebar + Header + Ana İçerik
 */
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import styles from './Layout.module.css'

export default function Layout() {
    const [sidebarAcik, setSidebarAcik] = useState(true)
    const [mobilMenuAcik, setMobilMenuAcik] = useState(false)

    return (
        <div className={styles.layout}>
            {/* Sidebar - Desktop */}
            <aside className={`${styles.sidebar} ${sidebarAcik ? styles.acik : styles.kapali}`}>
                <Sidebar
                    acik={sidebarAcik}
                    setAcik={setSidebarAcik}
                />
            </aside>

            {/* Sidebar - Mobil */}
            <div className={`${styles.sidebarMobil} ${mobilMenuAcik ? styles.acik : ''}`}>
                <div className={styles.overlay} onClick={() => setMobilMenuAcik(false)} />
                <div className={styles.sidebarContent}>
                    <Sidebar
                        acik={true}
                        setAcik={() => setMobilMenuAcik(false)}
                        mobilMenu
                    />
                </div>
            </div>

            {/* Ana İçerik */}
            <div className={`${styles.mainContent} ${sidebarAcik ? styles.sidebarAcik : styles.sidebarKapali}`}>
                <Header
                    mobilMenuAcik={mobilMenuAcik}
                    setMobilMenuAcik={setMobilMenuAcik}
                />

                <main style={{ flex: 1, padding: '24px', maxWidth: '1400px', margin: '0 auto', width: '100%' }}>
                    <Outlet />
                </main>
            </div>
        </div>
    )
}
