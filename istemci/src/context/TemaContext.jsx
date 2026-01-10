import { createContext, useContext, useEffect, useState } from 'react';

const TemaContext = createContext();

export function TemaSaglayici({ children }) {
    // Varsayılan tema: Sistem tercihi veya localStorage
    const [tema, setTema] = useState(() => {
        const kaydedilenTema = localStorage.getItem('tema');
        if (kaydedilenTema) {
            return kaydedilenTema;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'koyu' : 'acik';
    });

    useEffect(() => {
        // Root elemente class ekle/çıkar
        const root = window.document.documentElement;

        if (tema === 'koyu') {
            root.classList.add('dark');
        } else {
            root.classList.remove('dark');
        }

        // Tercihi kaydet
        localStorage.setItem('tema', tema);
    }, [tema]);

    const temaDegistir = () => {
        setTema(prev => prev === 'acik' ? 'koyu' : 'acik');
    };

    return (
        <TemaContext.Provider value={{ tema, temaDegistir }}>
            {children}
        </TemaContext.Provider>
    );
}

export function useTema() {
    return useContext(TemaContext);
}
