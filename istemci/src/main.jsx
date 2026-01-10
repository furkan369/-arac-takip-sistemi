/**
 * Ana Giriş Noktası
 * React Query Provider ile sarmalanmış uygulama
 */
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App.jsx'
import './index.css'

// React Query client oluştur
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // Pencere odağında otomatik yenileme kapalı
      retry: 1, // Hata durumunda 1 kez tekrar dene
      staleTime: 5 * 60 * 1000, // 5 dakika fresh data
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)
