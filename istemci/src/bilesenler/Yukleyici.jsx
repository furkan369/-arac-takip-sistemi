/**
 * Yükleyici (Loading) Bileşeni
 * Veri yüklenirken gösterilir
 */
import styles from './Yukleyici.module.css'

export default function Yukleyici({ metin = 'Yükleniyor...' }) {
    return (
        <div className={styles.container}>
            <div className={styles.spinner}></div>
            <p className={styles.metin}>{metin}</p>
        </div>
    )
}
