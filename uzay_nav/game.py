import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Lost in Space - Gemi Oyunu", page_icon="🛸")

# --- CSS İLE YILDIZLI ARKA PLAN (ATMOSFER İÇİN) ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-attachment: fixed;
        background-size: cover;
    }
    /* Yazıları beyaz yapalım */
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🛸 Uzayda Kayıp: Star Tracker Simülasyonu")
st.markdown("""
**Durum Raporu:** Geminin navigasyon sistemi arızalandı. Konumumuzu bilmiyoruz.
**Görev:** Kameradan gelen yıldız görüntüsünü analiz et ve hangi takımyıldızına baktığımızı bul.
""")

# --- 1. VERİTABANI: BİLİNEN YILDIZ DESENLERİ ---
# Bir Geomatikçi olarak elimizdeki referans haritalar bunlardır.
# (X, Y) koordinatları basit matrisler olarak tanımladık.
takimyildizlar = {
    "Orion (Avcı)": np.array([[1, 5], [3, 5], [2, 5], [1, 2], [3, 2], [2, 3.5]]), 
    "Cassiopeia (Kraliçe - W Şekli)": np.array([[1, 4], [2, 1], [3, 3], [4, 1], [5, 4]]),
    "Ursa Major (Büyükayı - Cezve)": np.array([[1, 4], [3, 4], [4, 3], [5, 2.5], [6, 3], [6, 5], [4, 5]]),
    "Triangulum (Üçgen)": np.array([[2, 1], [4, 1], [3, 4]]),
    "Crux (Güney Haçı)": np.array([[2, 5], [2, 1], [0.5, 3.5], [3.5, 3]]),
    "Ursa Minor (Küçük Ayı)": np.array([[1, 3], [2, 3.5], [3, 3.2], [4, 3], [4.5, 2], [5.5, 2], [5.5, 3]]), 
    "Scorpius (Akrep)": np.array([[1, 5], [1.5, 4], [2, 3], [3, 2], [4, 1.5], [5, 1.5], [6, 2], [6.5, 3], [5.5, 3.5]]), 
    "Leo (Aslan)": np.array([[1, 3], [2, 4], [3, 3.5], [3.5, 2.5], [5, 2.5], [6, 3.5], [4, 4], [2.5, 5]]), 
    "Cygnus (Kuğu - Kuzey Haçı)": np.array([[3, 1], [3, 3], [3, 5], [1, 4], [5, 4]]), 
    "Pegasus (Kanatlı At - Kare)": np.array([[2, 2], [2, 5], [5, 5], [5, 2], [6, 6], [1, 6]]) 
}

# --- 2. OYUN MOTORU (SESSION STATE) ---

if 'hedef_yildiz_adi' not in st.session_state:
    st.session_state['hedef_yildiz_adi'] = None
    st.session_state['kamera_goruntusu'] = None

# --- 3. SOL MENÜ: KONTROL PANELİ ---
st.sidebar.header("🕹️ Kontrol Paneli")
tara_butonu = st.sidebar.button("Kamerayı Çalıştır ve Tara 📸")

if tara_butonu:
    
    secilen_isim = random.choice(list(takimyildizlar.keys()))
    orijinal_koordinatlar = takimyildizlar[secilen_isim]
    
    
    hata_payi = np.random.normal(0, 0.15, orijinal_koordinatlar.shape)
    
   
    st.session_state['hedef_yildiz_adi'] = secilen_isim
    st.session_state['kamera_goruntusu'] = orijinal_koordinatlar + hata_payi
    st.sidebar.success("Görüntü alındı! Analiz ediliyor...")

# --- 4. GÖRSELLEŞTİRME VE OYUN ALANI ---
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state['kamera_goruntusu'] is not None:
        st.subheader("📷 Sensör Görüntüsü")
        
        # Grafik çizimi
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Uzay teması (Simsiyah arka plan)
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        # Yıldızları çiz
        x = st.session_state['kamera_goruntusu'][:, 0]
        y = st.session_state['kamera_goruntusu'][:, 1]
        ax.scatter(x, y, color='white', s=150, marker='*', edgecolors='cyan')
        
        # Eksenleri gizle (Uzayda x-y ekseni çizgisi görünmez)
        ax.axis('off')
        
        # Ekrana bas
        st.pyplot(fig)
    else:
        st.info("Simülasyonu başlatmak için sol menüden 'Kamerayı Çalıştır' butonuna basınız.")

with col2:
    if st.session_state['kamera_goruntusu'] is not None:
        st.subheader("🧩 Eşleştirme")
        st.write("Bu desen veritabanındaki hangi takımyıldıza benziyor?")
        
        # Kullanıcı tahmini
        tahmin = st.radio("Seçenekler:", list(takimyildizlar.keys()))
        
        onayla = st.button("Rotayı Onayla ✅")
        
        if onayla:
            dogru_cevap = st.session_state['hedef_yildiz_adi']
            
            if tahmin == dogru_cevap:
                st.balloons()
                st.success(f"BAŞARILI! 🎉\nDoğru konum: {dogru_cevap}")
                st.write("Navigasyon sistemi kilitlendi. Güvenli yolculuklar!")
            else:
                st.error("EŞLEŞME HATASI! ❌")
                st.write(f"Sistem konumu doğrulayamadı. Doğru cevap: **{dogru_cevap}** olacaktı.")
                st.warning("Tekrar denemek için kamerayı yeniden çalıştırın.")