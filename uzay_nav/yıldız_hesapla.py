from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time
from astropy import units as u
import sys


try:
    
    kullanici_enlem = input("Enlem (Latitude) giriniz: ")
    kullanici_boylam = input("Boylam (Longitude) giriniz: ")
    kullanici_yukseklik = input("Yükseklik (Metre) giriniz (Örn: 0): ")

   
    lat = float(kullanici_enlem)
    lon = float(kullanici_boylam)
    h = float(kullanici_yukseklik)

except ValueError:
   
    print("\nHATA: Lütfen geçerli sayısal değerler giriniz! (Örn: 41.5)")
    sys.exit() 


location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
time = Time.now()

print(f"\nHesaplamalar yapılıyor... (Zaman: {time.iso})")
print("-" * 40)


yildizlar_katalogu = {
    'Sirius': SkyCoord(ra='06h45m08s', dec='-16d42m58s', frame='icrs'),
    'Polaris (Kutup Yildizi)': SkyCoord(ra='02h31m49s', dec='+89d15m50s', frame='icrs'),
    'Betelgeuse': SkyCoord(ra='05h55m10s', dec='+07d24m25s', frame='icrs'),
    'Vega': SkyCoord(ra='18h36m56s', dec='+38d47m01s', frame='icrs'),
    'Antares': SkyCoord(ra='16h29m24s', dec='-26d25m55s', frame='icrs'),
    'Aldebaran': SkyCoord(ra='04h35m55s', dec='+16d30m33s', frame='icrs')
}


altaz_frame = AltAz(obstime=time, location=location)
gorunur_yildiz_sayisi = 0

for isim, koordinat in yildizlar_katalogu.items():
   
    yerel_konum = koordinat.transform_to(altaz_frame)
    alt = yerel_konum.alt.degree
    az = yerel_konum.az.degree
    
    if alt > 0:
        gorunur_yildiz_sayisi += 1
        print(f"★ {isim}")
        print(f"  Yükseklik (Alt): {alt:.2f}° | Yön (Az): {az:.2f}°")
        
       
        yon_tarifi = ""
        if 337.5 <= az or az < 22.5: yon_tarifi = "Kuzey"
        elif 22.5 <= az < 67.5: yon_tarifi = "Kuzey Doğu"
        elif 67.5 <= az < 112.5: yon_tarifi = "Doğu"
        elif 112.5 <= az < 157.5: yon_tarifi = "Güney Doğu"
        elif 157.5 <= az < 202.5: yon_tarifi = "Güney"
        elif 202.5 <= az < 247.5: yon_tarifi = "Güney Batı"
        elif 247.5 <= az < 292.5: yon_tarifi = "Batı"
        elif 292.5 <= az < 337.5: yon_tarifi = "Kuzey Batı"
        
        print(f"  Konum: {yon_tarifi} yönünde.\n")

if gorunur_yildiz_sayisi == 0:
    print("Şu an bulunduğunuz konumda bu listedeki yıldızların hiçbiri görünmüyor.")

print("-" * 40)

