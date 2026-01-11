import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'Vibe Araç Takip',
        short_name: 'Vibe',
        description: 'Akıllı Araç Bakım ve Masraf Takip Sistemi',
        theme_color: '#4F46E5',
        background_color: '#F8FAFC',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        orientation: 'portrait',
        icons: [
          {
            src: 'pwa-icon.png',
            sizes: '512x512', // Şimdilik tek boyut geneli karşılar
            type: 'image/png'
          },
          {
            src: 'pwa-icon.png',
            sizes: '192x192',
            type: 'image/png'
          }
        ]
      }
    })
  ],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'https://arac-takip-backend.onrender.com',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
