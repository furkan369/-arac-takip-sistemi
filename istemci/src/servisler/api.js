/**
 * API Servisi
 * Axios instance ve tüm API istekleri
 */
import axios from 'axios';

// Axios instance oluştur
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 saniye
});

// İstek interceptor - Token ekleme
api.interceptors.request.use(
    (config) => {
        // Local storage'dan token al
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Yanıt interceptor - Türkçe hata mesajları ve 401 handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        let hataMesaji = 'Bir hata oluştu';

        if (error.response) {
            // Sunucu yanıt verdi ama hata kodu döndü
            switch (error.response.status) {
                case 400:
                    hataMesaji = error.response.data.detail || 'Geçersiz istek';
                    break;
                case 401:
                    hataMesaji = 'Oturum süreniz doldu. Lütfen tekrar giriş yapın';
                    // Token sil ve login'e yönlendir
                    localStorage.removeItem('access_token');
                    if (window.location.pathname !== '/giris' && window.location.pathname !== '/kayit') {
                        window.location.href = '/giris';
                    }
                    break;
                case 403:
                    hataMesaji = 'Bu işlem için yetkiniz yok';
                    break;
                case 404:
                    hataMesaji = 'İstenen kayıt bulunamadı';
                    break;
                case 500:
                    hataMesaji = 'Sunucu hatası. Lütfen daha sonra tekrar deneyin';
                    break;
                default:
                    hataMesaji = error.response.data.detail || 'Beklenmeyen bir hata oluştu';
            }
        } else if (error.request) {
            // İstek gönderildi ama yanıt alınamadı
            hataMesaji = 'Sunucuya bağlanılamıyor. İnternet bağlantınızı kontrol edin';
        }

        error.message = hataMesaji;
        return Promise.reject(error);
    }
);

// Araç servisleri
export const aracServisi = {
    /**
     * Tüm araçları getir
     */
    tumunuGetir: async (params = {}) => {
        const response = await api.get('/araclar', { params });
        return response.data;
    },

    /**
     * Tek bir araç getir
     */
    getir: async (id) => {
        const response = await api.get(`/araclar/${id}`);
        return response.data;
    },

    /**
     * İlişkili verilerle detaylı araç kaydı getir
     */
    detayGetir: async (id) => {
        const response = await api.get(`/araclar/${id}/detay`);
        return response.data;
    },

    /**
     * Yeni araç oluştur
     */
    olustur: async (veri) => {
        const response = await api.post('/araclar', veri);
        return response.data;
    },

    /**
     * Araç güncelle
     */
    guncelle: async (id, veri) => {
        const response = await api.put(`/araclar/${id}`, veri);
        return response.data;
    },

    /**
     * Araç sil
     */
    sil: async (id) => {
        const response = await api.delete(`/araclar/${id}`);
        return response.data;
    },

    /**
     * Kilometre güncelle
     */
    kilometreGuncelle: async (id, km) => {
        const response = await api.patch(`/araclar/${id}/kilometre`, { km });
        return response.data;
    },

    /**
     * Araç sayısı
     */
    sayiGetir: async () => {
        const response = await api.get('/araclar/istatistik/sayim');
        return response.data;
    },
};

// Bakım servisleri
export const bakimServisi = {
    tumunuGetir: async (aracId) => {
        const response = await api.get(`/bakimlar/arac/${aracId}`);
        return response.data;
    },

    olustur: async (veri) => {
        const response = await api.post('/bakimlar', veri);
        return response.data;
    },

    toplamMaliyet: async (aracId) => {
        const response = await api.get(`/bakimlar/arac/${aracId}/toplam-maliyet`);
        return response.data;
    },
};

// Harcama servisleri
export const harcamaServisi = {
    tumunuGetir: async (aracId, kategori = null) => {
        const params = kategori ? { kategori } : {};
        const response = await api.get(`/harcamalar/arac/${aracId}`, { params });
        return response.data;
    },

    olustur: async (veri) => {
        const response = await api.post('/harcamalar', veri);
        return response.data;
    },

    toplamHarcama: async (aracId) => {
        const response = await api.get(`/harcamalar/arac/${aracId}/toplam`);
        return response.data;
    },

    kategoriAnalizi: async (aracId) => {
        const response = await api.get(`/harcamalar/arac/${aracId}/kategori-analizi`);
        return response.data;
    },
};

// Yakıt servisleri
export const yakitServisi = {
    tumunuGetir: async (aracId) => {
        const response = await api.get(`/yakit/arac/${aracId}`);
        return response.data;
    },

    olustur: async (veri) => {
        const response = await api.post('/yakit', veri);
        return response.data;
    },

    tuketimAnalizi: async (aracId) => {
        const response = await api.get(`/yakit/arac/${aracId}/tuketim-analizi`);
        return response.data;
    },

    istasyonAnalizi: async (aracId) => {
        const response = await api.get(`/yakit/arac/${aracId}/istasyon-analizi`);
        return response.data;
    },
};

// İstatistik servisleri
export const istatistikServisi = {
    aylikHarcama: async (aracId = null, aySayisi = 6) => {
        const params = { ay_sayisi: aySayisi };
        if (aracId) params.arac_id = aracId;
        const response = await api.get('/istatistikler/aylik-harcama', { params });
        return response.data;
    },

    kategoriDagilim: async (aracId = null) => {
        const params = {};
        if (aracId) params.arac_id = aracId;
        const response = await api.get('/istatistikler/kategori-dagilim', { params });
        return response.data;
    },

    yakitTuketim: async (aracId, aySayisi = 12) => {
        const response = await api.get('/istatistikler/yakit-tuketim', {
            params: { arac_id: aracId, ay_sayisi: aySayisi }
        });
        return response.data;
    },

    aracKarsilastirma: async () => {
        const response = await api.get('/istatistikler/arac-karsilastirma');
        return response.data;
    },

    bakimTakip: async (aracId) => {
        const response = await api.get(`/istatistikler/bakim-takip/${aracId}`);
        return response.data;
    },
};

// Authentication servisleri
export const authServisi = {
    /**
     * Kullanıcı kaydı
     */
    kayit: async (email, adSoyad, sifre) => {
        const response = await api.post('/auth/kayit', {
            email,
            ad_soyad: adSoyad,
            sifre
        });
        return response.data;
    },

    /**
     * Kullanıcı girişi
     */
    giris: async (email, sifre) => {
        const response = await api.post('/auth/giris', { email, sifre });
        if (response.data.access_token) {
            // Token'ı localStorage'a kaydet
            localStorage.setItem('access_token', response.data.access_token);
            if (response.data.rol) {
                localStorage.setItem('rol', response.data.rol);
            }
        }
        return response.data;
    },

    /**
     * Çıkış yap
     */
    cikis: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('rol');
        window.location.href = '/giris';
    },

    /**
     * Token var mı kontrol et
     */
    tokenVarMi: () => {
        return !!localStorage.getItem('access_token');
    },

    /**
     * Token al
     */
    tokenAl: () => {
        return localStorage.getItem('access_token');
    }
};

// Admin Kullanıcı Yönetimi Servisleri
export const kullaniciServisi = {
    tumunuGetir: async () => {
        const response = await api.get('/kullanicilar');
        return response.data;
    },

    olustur: async (veri) => {
        const response = await api.post('/kullanicilar', veri);
        return response.data;
    },

    sil: async (id) => {
        const response = await api.delete(`/kullanicilar/${id}`);
        return response.data;
    }
};

// Profil Servisleri
export const profilServisi = {
    getir: async () => {
        const response = await api.get('/auth/me');
        return response.data;
    },

    guncelle: async (veri) => {
        const response = await api.put('/auth/me', veri);
        return response.data;
    },

    sifreDegistir: async (veri) => {
        const response = await api.put('/auth/sifre-degistir', veri);
        return response.data;
    }
};

export default api;
