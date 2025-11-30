import streamlit as st
import requests
import pandas as pd

# ---------------------------
#  🌍  LANGUAGE TRANSLATIONS 
# ---------------------------

language_translations = {
    'English': {'title': '🌾 Agriculture Recommendation System', 'location': '📍 Enter your location (State name)',
                'crop': '🌱 Select Crop Type', 'get_recommendation': '🔍 Get Recommendations', 'current_temp': '🌡️ Current Temperature',
                'weather_desc': '☁️ Weather Description', 'soil_moisture': '💧 Soil Moisture', 'soil_temp': '🌡️ Soil Temperature',
                'recommendations': '📌 Recommendations', 'recommended_crop': '🌿 Recommended Crop', 'fertilizer': '🧪 Recommended Fertilizer',
                'fertilizer_brand': '🏷️ Best & Cheap Fertilizer Brand', 'mixture_field': '🧱 Mixture Composition for Field',
                'price_increase': '📈 Expected Price Value Increase', 'acre_mixture': '🌾 Mixture Composition per Acre'},

    'Hindi': {'title': '🌾 कृषि अनुशंसा प्रणाली', 'location': '📍 अपना स्थान दर्ज करें (राज्य का नाम)',
              'crop': '🌱 फसल प्रकार चुनें', 'get_recommendation': '🔍 अनुशंसाएँ प्राप्त करें', 'current_temp': '🌡️ वर्तमान तापमान',
              'weather_desc': '☁️ मौसम विवरण', 'soil_moisture': '💧 मिट्टी की नमी', 'soil_temp': '🌡️ मिट्टी का तापमान',
              'recommendations': '📌 अनुशंसाएँ', 'recommended_crop': '🌿 अनुशंसित फसल', 'fertilizer': '🧪 अनुशंसित उर्वरक',
              'fertilizer_brand': '🏷️ सर्वश्रेष्ठ और सस्ता उर्वरक ब्रांड', 'mixture_field': '🧱 क्षेत्र के लिए मिश्रण संरचना',
              'price_increase': '📈 अपेक्षित मूल्य वृद्धि', 'acre_mixture': '🌾 एकड़ प्रति मिश्रण संरचना'},

    'Bengali': {'title': '🌾 কৃষি সুপারিশ ব্যবস্থা', 'location': '📍 আপনার অবস্থান লিখুন (রাজ্যের নাম)',
                'crop': '🌱 ফসলের ধরন নির্বাচন করুন', 'get_recommendation': '🔍 প্রস্তাবনা পান',
                'current_temp': '🌡️ বর্তমান তাপমাত্রা', 'weather_desc': '☁️ আবহাওয়ার বিবরণ', 'soil_moisture': '💧 মাটি আর্দ্রতা',
                'soil_temp': '🌡️ মাটির তাপমাত্রা', 'recommendations': '📌 প্রস্তাবনা', 'recommended_crop': '🌿 প্রস্তাবিত ফসল',
                'fertilizer': '🧪 প্রস্তাবিত সার', 'fertilizer_brand': '🏷️ সেরা ও সস্তা সার ব্র্যান্ড',
                'mixture_field': '🧱 ক্ষেত্রের জন্য মিশ্রণ', 'price_increase': '📈 প্রত্যাশিত মূল্য বৃদ্ধি',
                'acre_mixture': '🌾 একর প্রতি মিশ্রণ'},

    # ⭐ NEW LANGUAGES ADDED ⭐
    'Punjabi': {'title': '🌾 ਖੇਤੀ ਸਿਫ਼ਾਰਿਸ਼ ਪ੍ਰਣਾਲੀ', 'location': '📍 ਆਪਣਾ ਸੂਬਾ ਲਿਖੋ',
                'crop': '🌱 ਫਸਲ ਦੀ ਕਿਸਮ ਚੁਣੋ', 'get_recommendation': '🔍 ਸਿਫ਼ਾਰਸ਼ਾਂ ਪ੍ਰਾਪਤ ਕਰੋ',
                'current_temp': '🌡️ ਮੌਜੂਦਾ ਤਾਪਮਾਨ', 'weather_desc': '☁️ ਮੌਸਮ ਦਾ ਵੇਰਵਾ', 'soil_moisture': '💧 ਮਿੱਟੀ ਦੀ ਨਮੀ',
                'soil_temp': '🌡️ ਮਿੱਟੀ ਦਾ ਤਾਪਮਾਨ', 'recommendations': '📌 ਸਿਫ਼ਾਰਸ਼ਾਂ', 'recommended_crop': '🌿 ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਫਸਲ',
                'fertilizer': '🧪 ਸਿਫ਼ਾਰਸ਼ ਕੀਤਾ ਖਾਦ', 'fertilizer_brand': '🏷️ ਚੰਗਾ ਅਤੇ ਸਸਤਾ ਖਾਦ ਬ੍ਰਾਂਡ',
                'mixture_field': '🧱 ਖੇਤ ਲਈ ਮਿਸ਼ਰਣ', 'price_increase': '📈 ਉਮੀਦ ਕੀਤੀ ਕੀਮਤ ਵਿੱਚ ਵਾਧਾ',
                'acre_mixture': '🌾 ਇੱਕ ਏਕੜ ਲਈ ਮਿਸ਼ਰਣ'},

    'Assamese': {'title': '🌾 কৃষি পৰামৰ্শ প্ৰণালী', 'location': '📍 আপোনাৰ অৱস্থান লিখক',
                 'crop': '🌱 ফলৰ প্ৰকাৰ নিৰ্বাচন কৰক', 'get_recommendation': '🔍 পৰামৰ্শ লওক',
                 'current_temp': '🌡️ বৰ্তমান তাপমাত্ৰা', 'weather_desc': '☁️ বতাহৰ বিৱৰণ',
                 'soil_moisture': '💧 মাটিৰ আর্দ্ৰতা', 'soil_temp': '🌡️ মাটিৰ তাপমাত্ৰা',
                 'recommended_crop': '🌿 পৰামৰ্শ দিয়া ফল', 'fertilizer': '🧪 পৰামৰ্শ দিয়া সাৰ',
                 'fertilizer_brand': '🏷️ উত্তম আৰু সস্তা সাৰ ব্রাণ্ড', 'mixture_field': '🧱 ক্ষেত্ৰৰ মিশ্ৰণ',
                 'price_increase': '📈 সম্ভাৱ্য মূল্য বৃদ্ধি', 'acre_mixture': '🌾 একেকৰ মিশ্ৰণ'},

    'Konkani': {'title': '🌾 कृषी शिफारस प्रणाली', 'location': '📍 तुमचो राज्य नाव दियात',
                'crop': '🌱 पीक प्रकार निवडात', 'get_recommendation': '🔍 शिफारस मेळो',
                'current_temp': '🌡️ सद्या तापमान', 'weather_desc': '☁️ हवामान वर्णन',
                'soil_moisture': '💧 माती ओलावा', 'soil_temp': '🌡️ माती तापमान',
                'recommended_crop': '🌿 शिफारस पीक', 'fertilizer': '🧪 शिफारस खत',
                'fertilizer_brand': '🏷️ उत्तम आणी स्वस्त खत ब्रँड', 'mixture_field': '🧱 क्षेत्र मिश्रण',
                'price_increase': '📈 अपेक्षित भाव वाढ', 'acre_mixture': '🌾 एकर मिश्रण'},

    'Sanskrit': {'title': '🌾 कृषि अनुशंसा प्रणाली', 'location': '📍 राज्यनाम लिखत',
                 'crop': '🌱 कृषि-प्रकारं चिनोतु', 'get_recommendation': '🔍 अनुशंसाः प्राप्नु',
                 'current_temp': '🌡️ वर्तमानतापमानम्', 'weather_desc': '☁️ मौसमवर्णनम्',
                 'soil_moisture': '💧 भूमेः आर्द्रता', 'soil_temp': '🌡️ भूमेः तापमानम्',
                 'recommended_crop': '🌿 अनुशंसितं धान्यम्', 'fertilizer': '🧪 अनुशंसितः उर्वरकः',
                 'fertilizer_brand': '🏷️ उत्तमः सः सुलभः उर्वरकब्राण्डः',
                 'mixture_field': '🧱 क्षेत्रस्य मिश्रणम्', 'price_increase': '📈 मूल्यवृद्धिः',
                 'acre_mixture': '🌾 एकैकरे मिश्रणम्'}
}

# ---------------------------
#  🔑 API KEYS
# ---------------------------

AGRO_API_KEY = 'YOUR_AGRO_API_KEY'
WEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'

# ---------------------------
#  📂 LOAD CROP CSV
# ---------------------------

crop_data = pd.read_csv('crop2.csv', encoding='ISO-8859-1')

# ---------------------------
#  🌐 LANGUAGE SELECTION
# ---------------------------

language = st.selectbox(
    '🌐 Choose Language / भाषा चुनें',
    list(language_translations.keys())
)

lang = language_translations[language]

# ---------------------------
#  🌾 TITLE
# ---------------------------

st.markdown(f"<h1 style='color:#2e8b57;text-align:center;'>{lang['title']}</h1>", unsafe_allow_html=True)

# ---------------------------
#  📍 LOCATION INPUT
# ---------------------------

location = st.text_input(lang['location'])

if location:
    try:
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        w = requests.get(weather_api_url).json()

        if "main" in w:
            st.success(f"{lang['current_temp']}: **{w['main']['temp']}°C**")
            st.info(f"{lang['weather_desc']}: **{w['weather'][0]['description']}**")

            lat = w['coord']['lat']
            lon = w['coord']['lon']

            soil_api_url = f"https://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
            s = requests.get(soil_api_url).json()

            if "moisture" in s:
                st.warning(f"{lang['soil_moisture']}: **{s['moisture']}%**")
                st.warning(f"{lang['soil_temp']}: **{s['t0']}°C**")
        else:
            st.error("⚠️ Invalid location!")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ---------------------------
#  🌱 CROP SELECTION
# ---------------------------

crop_options = crop_data['Recommended Crop'].unique()
selected_crop = st.selectbox(lang['crop'], crop_options)

# ---------------------------
#  🔍 SHOW RECOMMENDATIONS
# ---------------------------

if st.button(lang['get_recommendation']):
    data = crop_data[crop_data['Recommended Crop'] == selected_crop]

    if not data.empty:
        d = data.iloc[0]

        st.subheader(lang['recommendations'])

        st.write(f"✅ **{lang['recommended_crop']}:** {selected_crop}")
        st.write(f"🧪 **{lang['fertilizer']}:** {d['Recommended Fertilizer']}")
        st.write(f"🏷️ **{lang['fertilizer_brand']}:** {d['Best & Cheap Fertilizer Brand']}")
        st.write(f"🧱 **{lang['mixture_field']}:** {d['Mixture Composition for Field']}")
        st.write(f"📈 **{lang['price_increase']}:** {d['Expected Price Value Increase']}")
        st.write(f"🌾 **{lang['acre_mixture']}:** {d['Mixture Composition per Acre']}")
    else:
        st.error("❌ No data found for this crop.")
