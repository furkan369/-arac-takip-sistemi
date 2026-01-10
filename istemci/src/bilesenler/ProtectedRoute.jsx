/**
 * Protected Route Bileşeni
 * Token olmadan erişimi engeller
 */
import { Navigate } from 'react-router-dom';
import { authServisi } from '../servisler/api';

export default function ProtectedRoute({ children }) {
    // Token var mı kontrol et
    if (!authServisi.tokenVarMi()) {
        // Token yoksa login sayfasına yönlendir
        return <Navigate to="/giris" replace />;
    }

    // Token varsa children'ı render et
    return children;
}
