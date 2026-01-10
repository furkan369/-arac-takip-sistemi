/**
 * Ana Uygulama Bileşeni
 * Router ve Layout yönetimi
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './bilesenler/Layout'
import ProtectedRoute from './bilesenler/ProtectedRoute'
import GenelBakis from './sayfalar/GenelBakis'
import AracDetay from './sayfalar/AracDetay'
import Giris from './sayfalar/Giris'

import Kayit from './sayfalar/Kayit'
import Kullanicilar from './sayfalar/Kullanicilar'
import Ayarlar from './sayfalar/Ayarlar'

import { TemaSaglayici } from './context/TemaContext'

function App() {
  return (
    <TemaSaglayici>
      <BrowserRouter>
        <Routes>
          {/* Public Routes - Auth */}
          <Route path="/giris" element={<Giris />} />
          <Route path="/kayit" element={<Kayit />} />

          {/* Protected Routes - Dashboard */}
          <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/genel-bakis" replace />} />
            <Route path="genel-bakis" element={<GenelBakis />} />
            <Route path="araclar/:id" element={<AracDetay />} />

            <Route path="kullanicilar" element={<Kullanicilar />} />
            <Route path="ayarlar" element={<Ayarlar />} />
            {/* Diğer korumalı sayfalar buraya eklenecek */}
          </Route>
        </Routes>
      </BrowserRouter>
    </TemaSaglayici>
  )
}

export default App
