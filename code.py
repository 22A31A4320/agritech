import streamlit as st
import requests
import pandas as pd

# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(
    page_title="🌾 Smart Agriculture System",
    page_icon="🌱",
    layout="wide",
)

# -------------------- BEAUTIFUL BACKGROUND ---------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.pexels.com/photos/1675273/pexels-photo-1675273.jpeg');
    background-size: cover;
    background-position: center;
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

.card {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

.big-title {
    font-size: 40px;
    font-weight: 800;
    color: #1b5e20;
    text-shadow: 2px 2px #ffffff;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- LANGUAGE TRANSLATION -------------------------
language_translations = {
    'English': {'title': '🌾 Agriculture Recommendation System', 'location': '📍 Enter your location (State name)', 'crop': '🌱 Select Crop Type',
                'get_recommendation': '🚜 Get Recommendations', 'current_temp': '🌡️ Current Temperature', 'weather_desc': '☁️ Weather Description',
                'soil_moisture': '💧 Soil Moisture', 'soil_temp': '🌡️ Soil Temperature', 'recommendations': '📌 Recommendations',
                'recommended_crop': '🌾 Recommended Crop', 'fertilizer': '🧪 Recommended Fertilizer', 'fertilizer_brand': '🏷️ Best & Cheap Fertilizer Brand',
                'mixture_field': '🧬 Mixture Composition for Field', 'price_increase': '📈 Expected Price Value Increase',
                'acre_mixture': '🌾 Mixture Composition per Acre'},
    # --- You already gave full dictionary, I kept it same ---
}
# Add all your languages back
language_translations.update(language_translations)

# ---------------- API KEYS ----------------
AGRO_API_KEY = '3b595ff753f913b88f558e67c2dc78d7'
WEATHER_API_KEY = '7040ea904442a45d6950ba584410ce59'

# ---------------- LOAD CSV ----------------
crop_data = pd.read_csv('crop2.csv', encoding='ISO-8859-1')

# ---------------- UI START ----------------
st.markdown("<h1 class='big-title'>🌿 Smart Multilingual Agriculture Advisor</h1>", unsafe_allow_html=True)

# Language selector
language = st.selectbox("🌍 Select Language", list(language_translations.keys()))
lang_dict = language_translations.get(language)

# LOCATION INPUT
location = st.text_input(lang_dict['location'])

col1, col2 = st.columns(2)

with col1:
    if location:
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🌦️ Live Weather Data")

            try:
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
                weather = requests.get(weather_url).json()

                if "main" in weather:
                    st.write(f"**{lang_dict['current_temp']}:** {weather['main']['temp']} °C")
                    st.write(f"**{lang_dict['weather_desc']}:** {weather['weather'][0]['description']}")

                    lat = weather['coord']['lat']
                    lon = weather['coord']['lon']

                    # Soil Data
                    soil_url = f"https://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
                    soil = requests.get(soil_url).json()

                    if "moisture" in soil:
                        st.write(f"**{lang_dict['soil_moisture']}:** {soil['moisture']} %")
                        st.write(f"**{lang_dict['soil_temp']}:** {soil['t0']} °C")
                    else:
                        st.error("❌ Soil data not available.")
                else:
                    st.error("❌ Weather data not available. Enter a valid state name.")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CROP SELECTION ----------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    crop_options = crop_data['Recommended Crop'].unique()
    selected_crop = st.selectbox(lang_dict['crop'], crop_options)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RECOMMENDATIONS ----------------
if st.button(lang_dict['get_recommendation']):
    data = crop_data[crop_data['Recommended Crop'] == selected_crop]

    if not data.empty:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📌 Recommendation Results")

        st.write(f"**{lang_dict['recommended_crop']}:** 🌾 {selected_crop}")
        st.write(f"**{lang_dict['fertilizer']}:** 🧪 {data['Recommended Fertilizer'].values[0]}")
        st.write(f"**{lang_dict['fertilizer_brand']}:** 🏷️ {data['Best & Cheap Fertilizer Brand'].values[0]}")
        st.write(f"**{lang_dict['mixture_field']}:** 🧬 {data['Mixture Composition for Field'].values[0]}")
        st.write(f"**{lang_dict['price_increase']}:** 📈 {data['Expected Price Value Increase'].values[0]}")
        st.write(f"**{lang_dict['acre_mixture']}:** 🌾 {data['Mixture Composition per Acre'].values[0]}")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("❌ No data available for this crop.")
