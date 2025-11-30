import streamlit as st
import requests
import pandas as pd

# --------------------------------------
# 🌈 BEAUTIFUL HIGH-CONTRAST BACKGROUND
# --------------------------------------

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    color: #000000;
}
h1, h2, h3, label, .stMarkdown, .stText {
    color: #003300 !important;
    font-weight: 700;
}
.info-box {
    padding: 15px;
    border-radius: 10px;
    background: #ffffffcc;
    color: #003300;
    border-left: 5px solid #006600;
    margin-bottom: 10px;
}
.section-title {
    color: #b30000;
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --------------------------------------
# 🌍 LANGUAGE TRANSLATIONS – 10 LANGUAGES
# --------------------------------------

language_translations = {
    'English': {'title': '🌾 Agriculture Recommendation System', 'location': '📍 Enter your location (State name)',
                'crop': '🌱 Select Crop Type', 'get_recommendation': '🔍 Get Recommendations',
                'current_temp': '🌡️ Current Temperature', 'weather_desc': '☁️ Weather Description',
                'soil_moisture': '💧 Soil Moisture', 'soil_temp': '🌡️ Soil Temperature',
                'recommendations': '📌 Recommendations', 'recommended_crop': '🌿 Recommended Crop',
                'fertilizer': '🧪 Recommended Fertilizer', 'fertilizer_brand': '🏷️ Best & Cheap Fertilizer Brand',
                'mixture_field': '🧱 Mixture Composition for Field', 'price_increase': '📈 Expected Price Value Increase',
                'acre_mixture': '🌾 Mixture Composition per Acre'},

    'Hindi': {'title': '🌾 कृषि अनुशंसा प्रणाली', 'location': '📍 अपना स्थान दर्ज करें (राज्य का नाम)',
              'crop': '🌱 फसल प्रकार चुनें', 'get_recommendation': '🔍 अनुशंसाएँ प्राप्त करें',
              'current_temp': '🌡️ वर्तमान तापमान', 'weather_desc': '☁️ मौसम विवरण',
              'soil_moisture': '💧 मिट्टी की नमी', 'soil_temp': '🌡️ मिट्टी का तापमान',
              'recommendations': '📌 अनुशंसाएँ', 'recommended_crop': '🌿 अनुशंसित फसल',
              'fertilizer': '🧪 अनुशंसित उर्वरक', 'fertilizer_brand': '🏷️ सर्वश्रेष्ठ और सस्ता उर्वरक ब्रांड',
              'mixture_field': '🧱 क्षेत्र मिश्रण', 'price_increase': '📈 अपेक्षित मूल्य वृद्धि',
              'acre_mixture': '🌾 एकड़ मिश्रण'},

    'Bengali': {'title': '🌾 কৃষি সুপারিশ ব্যবস্থা', 'location': '📍 আপনার অবস্থান লিখুন (রাজ্যের নাম)',
                'crop': '🌱 ফসলের ধরন নির্বাচন করুন', 'get_recommendation': '🔍 প্রস্তাবনা পান',
                'current_temp': '🌡️ বর্তমান তাপমাত্রা', 'weather_desc': '☁️ আবহাওয়ার বিবরণ',
                'soil_moisture': '💧 মাটি আর্দ্রতা', 'soil_temp': '🌡️ মাটির তাপমাত্রা',
                'recommendations': '📌 প্রস্তাবনা', 'recommended_crop': '🌿 প্রস্তাবিত ফসল',
                'fertilizer': '🧪 প্রস্তাবিত সার', 'fertilizer_brand': '🏷️ সেরা ও সস্তা সার ব্র্যান্ড',
                'mixture_field': '🧱 ক্ষেত্রের জন্য মিশ্রণ', 'price_increase': '📈 প্রত্যাশিত মূল্য বৃদ্ধি',
                'acre_mixture': '🌾 একর প্রতি মিশ্রণ'},

    'Telugu': {'title': '🌾 వ్యవసాయ సిఫార్సు వ్యవస్థ', 'location': '📍 మీ స్థలం నమోదు చేయండి (రాష్ట్రం పేరు)',
               'crop': '🌱 పంట రకం ఎంచుకోండి', 'get_recommendation': '🔍 సిఫార్సులు పొందండి',
               'current_temp': '🌡️ ప్రస్తుత ఉష్ణోగ్రత', 'weather_desc': '☁️ వాతావరణ వివరాలు',
               'soil_moisture': '💧 నేల తేమ', 'soil_temp': '🌡️ నేల ఉష్ణోగ్రత',
               'recommendations': '📌 సిఫార్సులు', 'recommended_crop': '🌿 సిఫార్సు చేసిన పంట',
               'fertilizer': '🧪 సిఫార్సు చేసిన ఎరువు', 'fertilizer_brand': '🏷️ ఉత్తమ మరియు చౌక ఎరువు బ్రాండ్',
               'mixture_field': '🧱 పొలం మిశ్రమం', 'price_increase': '📈 అంచనా ధర పెరుగుదల',
               'acre_mixture': '🌾 ఎకరం మిశ్రమం'},

    'Marathi': {'title': '🌾 कृषि शिफारस प्रणाली', 'location': '📍 आपले स्थान प्रविष्ट करा (राज्याचे नाव)',
                'crop': '🌱 पिकाचा प्रकार निवडा', 'get_recommendation': '🔍 शिफारसी मिळवा',
                'current_temp': '🌡️ सद्य तापमान', 'weather_desc': '☁️ हवामान वर्णन',
                'soil_moisture': '💧 मातीतील आर्द्रता', 'soil_temp': '🌡️ मातीचे तापमान',
                'recommendations': '📌 शिफारसी', 'recommended_crop': '🌿 शिफारस केलेले पीक',
                'fertilizer': '🧪 शिफारस खत', 'fertilizer_brand': '🏷️ उत्तम आणि स्वस्त खत ब्रँड',
                'mixture_field': '🧱 क्षेत्र मिश्रण', 'price_increase': '📈 अपेक्षित किंमत वाढ',
                'acre_mixture': '🌾 एकर मिश्रण'},

    'Tamil': {'title': '🌾 வேளாண்மை பரிந்துரை அமைப்பு', 'location': '📍 உங்கள் மாநிலத்தை உள்ளிடவும்',
              'crop': '🌱 பயிர் வகையைத் தேர்ந்தெடுக்கவும்', 'get_recommendation': '🔍 பரிந்துரைகளை பெறவும்',
              'current_temp': '🌡️ தற்போதைய வெப்பநிலை', 'weather_desc': '☁️ வானிலை விவரம்',
              'soil_moisture': '💧 மண்ணின் ஈரப்பதம்', 'soil_temp': '🌡️ மண் வெப்பநிலை',
              'recommendations': '📌 பரிந்துரைகள்', 'recommended_crop': '🌿 பரிந்துரைக்கப்பட்ட பயிர்',
              'fertilizer': '🧪 பரிந்துரைக்கப்பட்ட உரம்', 'fertilizer_brand': '🏷️ சிறந்த மற்றும் மலிவு உரம்',
              'mixture_field': '🧱 நிலத் கலவை', 'price_increase': '📈 எதிர்பார்க்கப்படும் விலை உயர்வு',
              'acre_mixture': '🌾 ஏக்கர் கலவை'},

    'Gujarati': {'title': '🌾 કૃષિ ભલામણ પ્રણાલી', 'location': '📍 તમારું રાજ્ય દાખલ કરો',
                 'crop': '🌱 પાકનો પ્રકાર પસંદ કરો', 'get_recommendation': '🔍 ભલામણ મેળવો',
                 'current_temp': '🌡️ વર્તમાન તાપમાન', 'weather_desc': '☁️ હવામાન વર્ણન',
                 'soil_moisture': '💧 જમીનની ભેજ', 'soil_temp': '🌡️ જમીનની ઉષ્ણતા',
                 'recommendations': '📌 ભલામણો', 'recommended_crop': '🌿 ભલામણ કરેલો પાક',
                 'fertilizer': '🧪 ભલામણ કરેલું ખાતર', 'fertilizer_brand': '🏷️ શ્રેષ્ઠ અને સસ્તુ ખાતર બ્રાન્ડ',
                 'mixture_field': '🧱 ખેતરનું મિશ્રણ', 'price_increase': '📈 અપેક્ષિત કિંમત વધારો',
                 'acre_mixture': '🌾 એકર મિશ્રણ'},

    'Kannada': {'title': '🌾 ಕೃಷಿ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ', 'location': '📍 ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ನಮೂದಿಸಿ',
                'crop': '🌱 ಬೆಳೆ ಪ್ರಕಾರ ಆಯ್ಕೆಮಾಡಿ', 'get_recommendation': '🔍 ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ',
                'current_temp': '🌡️ ಪ್ರಸ್ತುತ ತಾಪಮಾನ', 'weather_desc': '☁️ ಹವಾಮಾನ ವಿವರ',
                'soil_moisture': '💧 ಮಣ್ಣಿನ ತೇವಾಂಶ', 'soil_temp': '🌡️ ಮಣ್ಣಿನ ತಾಪಮಾನ',
                'recommendations': '📌 ಶಿಫಾರಸುಗಳು', 'recommended_crop': '🌿 ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ',
                'fertilizer': '🧪 ಶಿಫಾರಸು ಮಾಡಿದ ರಸಗುಳ್ಳಿಗಳು',
                'fertilizer_brand': '🏷️ ಉತ್ತಮ ಮತ್ತು ಅಗ್ಗದ ರಸಗುಳ್ಳಿಗಳ ಬ್ರ್ಯಾಂಡ್',
                'mixture_field': '🧱 ಹೊಲ ಮಿಶ್ರಣ', 'price_increase': '📈 ನಿರೀಕ್ಷಿತ ಬೆಲೆ ಏರಿಕೆ',
                'acre_mixture': '🌾 ಏಕರ್ ಮಿಶ್ರಣ'},

    'Malayalam': {'title': '🌾 കൃഷി ശുപാർശാ സംവിധാനം', 'location': '📍 നിങ്ങളുടെ സംസ്ഥാനം നൽകുക',
                  'crop': '🌱 വിളയിനം തിരഞ്ഞെടുക്കുക', 'get_recommendation': '🔍 ശുപാർശകൾ നേടുക',
                  'current_temp': '🌡️ നിലവിലെ താപനില', 'weather_desc': '☁️ കാലാവസ്ഥ വിവരണം',
                  'soil_moisture': '💧 മണ്ണിലെ ഈർപ്പം', 'soil_temp': '🌡️ മണ്ണിന്റെ ചൂട്',
                  'recommendations': '📌 ശുപാർശകൾ', 'recommended_crop': '🌿 ശുപാർശ ചെയ്യുന്ന വിള',
                  'fertilizer': '🧪 ശുപാർശ ചെയ്യുന്ന വളം',
                  'fertilizer_brand': '🏷️ മികച്ച & വില കുറഞ്ഞ വളം ബ്രാൻഡ്',
                  'mixture_field': '🧱 ഫീൽഡ് മിശ്രിതം', 'price_increase': '📈 പ്രതീക്ഷിക്കുന്ന വിലവർധന',
                  'acre_mixture': '🌾 ഏക്കറിന് മിശ്രിതം'},

    'Odia': {'title': '🌾 କୃଷି ସୁପାରିଶ ପ୍ରଣାଳୀ', 'location': '📍 ଆପଣଙ୍କର ରାଜ୍ୟ ଲେଖନ୍ତୁ',
             'crop': '🌱 ଫସଳ ପ୍ରକାର ବାଛନ୍ତୁ', 'get_recommendation': '🔍 ସୁପାରିଶ ପାଆନ୍ତୁ',
             'current_temp': '🌡️ ବର୍ତ୍ତମାନ ତାପମାନ', 'weather_desc': '☁️ ଆବହାବିବରଣୀ',
             'soil_moisture': '💧 ମାଟିର ଆର୍ଦ୍ରତା', 'soil_temp': '🌡️ ମାଟିର ତାପମାନ',
             'recommendations': '📌 ସୁପାରିଶ', 'recommended_crop': '🌿 ସୁପାରିଶ ନିତ ଫସଳ',
             'fertilizer': '🧪 ସୁପାରିଶ ସାର', 'fertilizer_brand': '🏷️ ଭଲ ଏବଂ ସସ୍ତା ସାର ବ୍ରାଣ୍ଡ',
             'mixture_field': '🧱 ଖେତର ମିଶ୍ରଣ', 'price_increase': '📈 ଅନୁମାନିତ ମୂଲ୍ୟ ବୃଦ୍ଧି',
             'acre_mixture': '🌾 ଏକର ମିଶ୍ରଣ'}
}

# --------------------------------------
# 🔑 API Keys
# --------------------------------------

AGRO_API_KEY = 'YOUR_AGRO_API_KEY'
WEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'

# --------------------------------------
# 📂 LOAD CSV
# --------------------------------------

crop_data = pd.read_csv("crop2.csv", encoding='ISO-8859-1')

# --------------------------------------
# 🌐 LANGUAGE SELECTOR
# --------------------------------------

language = st.selectbox("🌐 Choose Language / भाषा चुनें", list(language_translations.keys()))
lang = language_translations[language]

# --------------------------------------
# 🌾 TITLE
# --------------------------------------

st.markdown(f"<h1 style='text-align:center;'>{lang['title']}</h1>", unsafe_allow_html=True)

# --------------------------------------
# 📍 LOCATION INPUT
# --------------------------------------

location = st.text_input(lang['location'])

if location:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        w = requests.get(url).json()

        if "main" in w:
            st.markdown(f"<div class='info-box'><b>{lang['current_temp']}:</b> {w['main']['temp']}°C</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-box'><b>{lang['weather_desc']}:</b> {w['weather'][0]['description']}</div>", unsafe_allow_html=True)

            lat, lon = w['coord']['lat'], w['coord']['lon']

            soil_url = f"https://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
            s = requests.get(soil_url).json()

            if "moisture" in s:
                st.markdown(f"<div class='info-box'><b>{lang['soil_moisture']}:</b> {s['moisture']}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><b>{lang['soil_temp']}:</b> {s['t0']}°C</div>", unsafe_allow_html=True)

    except:
        st.error("⚠️ Invalid Location!")

# --------------------------------------
# 🌱 CROP SELECTION
# --------------------------------------

crop_options = crop_data["Recommended Crop"].unique()
selected_crop = st.selectbox(lang['crop'], crop_options)

# --------------------------------------
# 🔍 FINAL RECOMMENDATION
# --------------------------------------

if st.button(lang['get_recommendation']):
    row = crop_data[crop_data["Recommended Crop"] == selected_crop].iloc[0]

    st.markdown("<h2 class='section-title'>📌 Final Recommendations</h2>", unsafe_allow_html=True)

    st.markdown(f"<div class='info-box'><b>{lang['recommended_crop']}:</b> {selected_crop}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-box'><b>{lang['fertilizer']}:</b> {row['Recommended Fertilizer']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-box'><b>{lang['fertilizer_brand']}:</b> {row['Best & Cheap Fertilizer Brand']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-box'><b>{lang['mixture_field']}:</b> {row['Mixture Composition for Field']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-box'><b>{lang['price_increase']}:</b> {row['Expected Price Value Increase']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-box'><b>{lang['acre_mixture']}:</b> {row['Mixture Composition per Acre']}</div>", unsafe_allow_html=True)
