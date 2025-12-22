import streamlit as st
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time
from astropy import units as u
import pandas as pd # Tablo gösterimi için (opsiyonel ama şık durur)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Geomatik Uzay Navigasyonu", page_icon="⭐")

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
             background-attachment: fixed;
             background-size: cover;
         }}
         /* Yazıları Okunur Yapmak İçin Beyaz Renk ve Gölge Verelim */
         h1, h2, h3, h4, h5, h6, p, label {{
             color: white !important;
             text-shadow: 2px 2px 4px #000000;
         }}
         /* Sidebar (Sol Menü) Ayarları */
         section[data-testid="stSidebar"] {{
             background-color: rgba(0, 0, 0, 0.5); /* Yarı saydam siyah */
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()



# --- BAŞLIK VE AÇIKLAMA ---
st.title("🌌 Yıldız Navigasyon Sistemi")
st.write("Bulunduğunuz konuma göre gökyüzündeki parlak yıldızların koordinatlarını hesaplayan web arayüzü.")

# --- 1. KULLANICI GİRİŞİ (SOL MENÜ - SIDEBAR) ---
st.sidebar.header("📍 Konum Bilgileri")
st.sidebar.info("Lütfen koordinatları ondalık derece cinsinden giriniz.")

# input yerine st.number_input kullanıyoruz
lat = st.sidebar.number_input("Enlem (Latitude)", value=41.0082, step=0.0001, format="%.4f")
lon = st.sidebar.number_input("Boylam (Longitude)", value=28.9784, step=0.0001, format="%.4f")
h = st.sidebar.number_input("Yükseklik (Metre)", value=0, step=1)

# Hesapla Butonu
hesapla_butonu = st.sidebar.button("Yıldızları Hesapla 🚀")

# --- 2. HESAPLAMA MOTORU ---
if hesapla_butonu:
    # Konum ve Zamanı Ayarla
    try:
        location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
        time = Time.now()
        
        st.success(f"Hesaplama Zamanı (UTC): {time.iso}")
        st.write("---")

        # Yıldız Kataloğu
        yildizlar_katalogu = {
            'Sirius': SkyCoord(ra='06h45m08s', dec='-16d42m58s', frame='icrs'),
            'Polaris (Kutup Yildizi)': SkyCoord(ra='02h31m49s', dec='+89d15m50s', frame='icrs'),
            'Betelgeuse': SkyCoord(ra='05h55m10s', dec='+07d24m25s', frame='icrs'),
            'Vega': SkyCoord(ra='18h36m56s', dec='+38d47m01s', frame='icrs'),
            'Antares': SkyCoord(ra='16h29m24s', dec='-26d25m55s', frame='icrs'),
            'Aldebaran': SkyCoord(ra='04h35m55s', dec='+16d30m33s', frame='icrs')
        }

        altaz_frame = AltAz(obstime=time, location=location)
        
        # Sonuçları toplamak için boş bir liste
        sonuc_listesi = []

        for isim, koordinat in yildizlar_katalogu.items():
            yerel_konum = koordinat.transform_to(altaz_frame)
            alt = yerel_konum.alt.degree
            az = yerel_konum.az.degree
            
            # Yön Tarifi
            yon_tarifi = ""
            if 337.5 <= az or az < 22.5: yon_tarifi = "Kuzey"
            elif 22.5 <= az < 67.5: yon_tarifi = "Kuzey Doğu"
            elif 67.5 <= az < 112.5: yon_tarifi = "Doğu"
            elif 112.5 <= az < 157.5: yon_tarifi = "Güney Doğu"
            elif 157.5 <= az < 202.5: yon_tarifi = "Güney"
            elif 202.5 <= az < 247.5: yon_tarifi = "Güney Batı"
            elif 247.5 <= az < 292.5: yon_tarifi = "Batı"
            elif 292.5 <= az < 337.5: yon_tarifi = "Kuzey Batı"

            # Sadece Ufuk Üstü
            durum = "Görünür" if alt > 0 else "Ufuk Altında"
            
            # Listeye ekle (Görünse de görünmese de ekleyelim, tabloda filtreleriz)
            if alt > 0:
                sonuc_listesi.append({
                    "Yıldız Adı": isim,
                    "Yükseklik (Alt)": f"{alt:.2f}°",
                    "Semt Açısı (Az)": f"{az:.2f}°",
                    "Yön": yon_tarifi,
                    "Durum": "✅ GÖRÜNÜR"
                })

        # --- 3. SONUÇLARI GÖSTERME ---
        if len(sonuc_listesi) > 0:
            st.subheader("🔭 Görülebilir Yıldızlar Listesi")
            # Listeyi şık bir tabloya (DataFrame) çevirip gösteriyoruz
            df = pd.DataFrame(sonuc_listesi)
            st.table(df)
            
            # Harita Bonusu: Geomatikçi olduğun için basit bir harita da koyalım
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
            st.caption("Konumunuz harita üzerinde işaretlendi.")
            
        else:
            st.warning("Şu an bu listedeki yıldızların hiçbiri ufkun üzerinde değil.")
            
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")

else:
    st.info("Hesaplama yapmak için sol taraftaki 'Yıldızları Hesapla' butonuna basınız.")