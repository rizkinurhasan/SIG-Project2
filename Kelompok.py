import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import xml.etree.ElementTree as ET

# Fungsi untuk mengambil data prakiraan cuaca dari API BMKG (XML)
def get_weather_forecast_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        st.error(f"Gagal mengambil data prakiraan cuaca dari {url}")
        return None

# Fungsi untuk membuat peta prakiraan cuaca
def create_weather_forecast_map(weather_data):
    # Tentukan lokasi awal peta
    m = folium.Map(location=[-7.5, 110], zoom_start=7)  # Lokasi tengah Jawa

    # Tambahkan marker untuk setiap lokasi prakiraan cuaca
    if weather_data:
        for area in weather_data.findall('.//area'):
            latitude = float(area.get('latitude'))
            longitude = float(area.get('longitude'))
            description = ""
            temperature = ""

            for parameter in area.findall('parameter'):
                if parameter.get('id') == 't':
                    temperature = parameter.find('timerange/value').text
                if parameter.get('id') == 'weather':
                    description = parameter.find('timerange/value').text

            folium.Marker(
                location=[latitude, longitude],
                popup=f"Temperature: {temperature}°C\nDescription: {description}",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

    return m

# Streamlit app
st.title("Peta Prakiraan Cuaca BMKG")

# URL API BMKG
urls = [
    "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml",
    "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml",
    "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml"
]

weather_data_list = [get_weather_forecast_data(url) for url in urls]

if all(weather_data_list):
    # Buat peta prakiraan cuaca
    weather_map = folium.Map(location=[-7.5, 150], zoom_start=50)  # Lokasi tengah Jawa

    for weather_data in weather_data_list:
        weather_map = create_weather_forecast_map(weather_data)

    # Tampilkan peta menggunakan streamlit-folium
    st_folium(weather_map, width=900, height=700)


    
