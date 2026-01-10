# 🚗 Akıllı Araç Takip Sistemi

Modern araç takip, bakım ve harcama yönetim sistemi.

## 🛠️ Teknolojiler

**Frontend:**
- React + Vite
- React Router
- React Query (TanStack Query)
- Axios

**Backend:**
- FastAPI
- SQLAlchemy
- MySQL/PostgreSQL
- JWT Authentication

## 🚀 Kurulum

### Backend
```bash
cd VibeUyg
pip install -r requirements.txt
python -m uvicorn sunucu.ana:uygulama --reload --port 8000
```

### Frontend
```bash
cd istemci
npm install
npm run dev
```

## 📝 Özellikler

✅ Kullanıcı yönetimi (JWT Auth)
✅ Araç kayıt ve takip
✅ Bakım kayıtları
✅ Harcama takibi
✅ Yakıt takibi
✅ İstatistikler ve grafikler
✅ Dark mode

## 🌐 Deploy

Frontend: Vercel
Backend: Railway
Database: Railway PostgreSQL
