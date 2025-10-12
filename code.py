final code: ! pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com! streamlit run app.py & npx localtunnel --port 8501 file name:crop2.csv app code:import streamlit as st
import requests
import pandas as pd

# Define language translation dictionary
language_translations = {
    'English': {'title': 'Agriculture Recommendation System', 'location': 'Enter your location (State name)', 'crop': 'Select Crop Type',
                'get_recommendation': 'Get Recommendations', 'current_temp': 'Current Temperature', 'weather_desc': 'Weather Description',
                'soil_moisture': 'Soil Moisture', 'soil_temp': 'Soil Temperature', 'recommendations': 'Recommendations',
                'recommended_crop': 'Recommended Crop', 'fertilizer': 'Recommended Fertilizer', 'fertilizer_brand': 'Best & Cheap Fertilizer Brand',
                'mixture_field': 'Mixture Composition for Field', 'price_increase': 'Expected Price Value Increase',
                'acre_mixture': 'Mixture Composition per Acre'},
    
    'Hindi': {'title': 'कृषि अनुशंसा प्रणाली', 'location': 'अपना स्थान दर्ज करें (राज्य का नाम)', 'crop': 'फसल प्रकार चुनें',
              'get_recommendation': 'अनुशंसाएँ प्राप्त करें', 'current_temp': 'वर्तमान तापमान', 'weather_desc': 'मौसम विवरण',
              'soil_moisture': 'मिट्टी की नमी', 'soil_temp': 'मिट्टी का तापमान', 'recommendations': 'अनुशंसाएँ',
              'recommended_crop': 'अनुशंसित फसल', 'fertilizer': 'अनुशंसित उर्वरक', 'fertilizer_brand': 'सर्वश्रेष्ठ और सस्ता उर्वरक ब्रांड',
              'mixture_field': 'क्षेत्र के लिए मिश्रण संरचना', 'price_increase': 'अपेक्षित मूल्य वृद्धि', 'acre_mixture': 'एकड़ प्रति मिश्रण संरचना'},

    'Bengali': {'title': 'কৃষি সুপারিশ ব্যবস্থা', 'location': 'আপনার অবস্থান লিখুন (রাজ্যের নাম)', 'crop': 'ফসলের ধরন নির্বাচন করুন',
                'get_recommendation': 'প্রস্তাবনা পান', 'current_temp': 'বর্তমান তাপমাত্রা', 'weather_desc': 'আবহাওয়ার বিবরণ',
                'soil_moisture': 'মাটি আর্দ্রতা', 'soil_temp': 'মাটির তাপমাত্রা', 'recommendations': 'প্রস্তাবনা',
                'recommended_crop': 'প্রস্তাবিত ফসল', 'fertilizer': 'প্রস্তাবিত সার', 'fertilizer_brand': 'সেরা ও সস্তা সার ব্র্যান্ড',
                'mixture_field': 'ক্ষেত্রের জন্য মিশ্রণ সংমিশ্রণ', 'price_increase': 'প্রত্যাশিত মূল্য বৃদ্ধি', 'acre_mixture': 'একর প্রতি মিশ্রণ সংমিশ্রণ'},

    'Marathi': {'title': 'कृषी शिफारस प्रणाली', 'location': 'तुमचे स्थान प्रविष्ट करा (राज्याचे नाव)', 'crop': 'पिकाचा प्रकार निवडा',
                'get_recommendation': 'शिफारसी मिळवा', 'current_temp': 'सध्याचे तापमान', 'weather_desc': 'हवामानाचे वर्णन',
                'soil_moisture': 'मातीतील आर्द्रता', 'soil_temp': 'मातीचे तापमान', 'recommendations': 'शिफारसी',
                'recommended_crop': 'शिफारस केलेले पीक', 'fertilizer': 'शिफारस केलेले खत', 'fertilizer_brand': 'सर्वोत्तम आणि स्वस्त खत ब्रँड',
                'mixture_field': 'क्षेत्रासाठी मिश्रण संयोजन', 'price_increase': 'अपेक्षित किंमत वाढ', 'acre_mixture': 'एकर प्रति मिश्रण संयोजन'},

    'Telugu': {'title': 'వ్యవసాయ సిఫార్సు వ్యవస్థ', 'location': 'మీ స్థానం నమోదు చేయండి (రాష్ట్రం పేరు)', 'crop': 'పంట రకం ఎంచుకోండి',
               'get_recommendation': 'సిఫార్సులు పొందండి', 'current_temp': 'ప్రస్తుత ఉష్ణోగ్రత', 'weather_desc': 'వాతావరణ వివరణ',
               'soil_moisture': 'మట్టీ తేమ', 'soil_temp': 'మట్టి ఉష్ణోగ్రత', 'recommendations': 'సిఫార్సులు',
               'recommended_crop': 'సిఫార్సు చేసిన పంట', 'fertilizer': 'సిఫార్సు చేసిన ఎరువు', 'fertilizer_brand': 'మంచి మరియు చవకైన ఎరువు బ్రాండ్',
               'mixture_field': 'ఫీల్డ్ కోసం మిశ్రమం', 'price_increase': 'అంచనా ధర పెరుగుదల', 'acre_mixture': 'ఎకరానికి మిశ్రమం'},

    'Tamil': {'title': 'விவசாய பரிந்துரை அமைப்பு', 'location': 'உங்கள் இருப்பிடத்தை உள்ளிடுங்கள் (மாநிலத்தின் பெயர்)', 'crop': 'பயிர் வகையைத் தேர்ந்தெடுக்கவும்',
              'get_recommendation': 'பரிந்துரைகளைப் பெறுங்கள்', 'current_temp': 'தற்போதைய வெப்பநிலை', 'weather_desc': 'வானிலை விவரம்',
              'soil_moisture': 'மண்ணின் ஈரப்பதம்', 'soil_temp': 'மண்ணின் வெப்பநிலை', 'recommendations': 'பரிந்துரைகள்',
              'recommended_crop': 'பரிந்துரைக்கப்பட்ட பயிர்', 'fertilizer': 'பரிந்துரைக்கப்பட்ட உரம்', 'fertilizer_brand': 'சிறந்த மற்றும் மலிவு உரம் பிராண்ட்',
              'mixture_field': 'பயிர்க் களத்திற்கு கலவை', 'price_increase': 'எதிர்பார்க்கப்படும் விலை உயர்வு', 'acre_mixture': 'ஒரு ஏக்கருக்கு கலவை'},

    'Gujarati': {'title': 'કૃષિ ભલામણ પદ્ધતિ', 'location': 'તમારું સ્થાન દાખલ કરો (રાજ્યનું નામ)', 'crop': 'પાકનો પ્રકાર પસંદ કરો',
                'get_recommendation': 'ભલામણો મેળવો', 'current_temp': 'હાલનું તાપમાન', 'weather_desc': 'હવામાન વર્ણન',
                'soil_moisture': 'માટીની ભેજ', 'soil_temp': 'માટીની તાપમાન', 'recommendations': 'ભલામણો',
                'recommended_crop': 'ભલામણ કરેલ પાક', 'fertilizer': 'ભલામણ કરેલ ખાતર', 'fertilizer_brand': 'શ્રેષ્ઠ અને સસ્તું ખાતર બ્રાન્ડ',
                'mixture_field': 'ફિલ્ડ માટે મિશ્રણ સંયોજન', 'price_increase': 'અપેક્ષિત ભાવમાં વધારો', 'acre_mixture': 'એકર દીઠ મિશ્રણ'},

    'Urdu': {'title': 'زرعی سفارش نظام', 'location': 'اپنی لوکیشن درج کریں (ریاست کا نام)', 'crop': 'فصل کی قسم منتخب کریں',
             'get_recommendation': 'سفارشات حاصل کریں', 'current_temp': 'موجودہ درجہ حرارت', 'weather_desc': 'موسم کی تفصیل',
             'soil_moisture': 'مٹی کی نمی', 'soil_temp': 'مٹی کا درجہ حرارت', 'recommendations': 'سفارشات',
             'recommended_crop': 'سفارش کردہ فصل', 'fertilizer': 'سفارش کردہ کھاد', 'fertilizer_brand': 'بہترین اور سستی کھاد برانڈ',
             'mixture_field': 'میدان کے لیے مرکب', 'price_increase': 'متوقع قیمت میں اضافہ', 'acre_mixture': 'ایکڑ کے حساب سے مرکب'},

    'Kannada': {'title': 'ಕೃಷಿ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ', 'location': 'ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ (ರಾಜ್ಯದ ಹೆಸರು)', 'crop': 'ಪಿಕದ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
                'get_recommendation': 'ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ', 'current_temp': 'ಪ್ರಸ್ತುತ ತಾಪಮಾನ', 'weather_desc': 'ಹವಾಮಾನ ವಿವರಣೆ',
                'soil_moisture': 'ಮಣ್ಣಿನ ತೇವಾಂಶ', 'soil_temp': 'ಮಣ್ಣಿನ ತಾಪಮಾನ', 'recommendations': 'ಶಿಫಾರಸುಗಳು',
                'recommended_crop': 'ಶಿಫಾರಸು ಮಾಡಲಾದ ಪಿಕ', 'fertilizer': 'ಶಿಫಾರಸು ಮಾಡಲಾದ ರಸಗೊಬ್ಬರ', 'fertilizer_brand': 'ಅತ್ಯುತ್ತಮ ಮತ್ತು ಕಡಿಮೆ ಬೆಲೆಯ ರಸಗೊಬ್ಬರ ಬ್ರ್ಯಾಂಡ್',
                'mixture_field': 'ಕೇಂದ್ರಕ್ಕಾಗಿ ಮಿಶ್ರಣ', 'price_increase': 'ಅಪೇಕ್ಷಿತ ಬೆಲೆಯ ಏರಿಕೆ', 'acre_mixture': 'ಎಕರೆಗೆ ಮಿಶ್ರಣ'},

    'Odia': {'title': 'କୃଷି ସୁପାରିଶ ପ୍ରଣାଳୀ', 'location': 'ଆପଣଙ୍କର ସ୍ଥାନ ଦାଖଲ କରନ୍ତୁ (ରାଜ୍ୟର ନାମ)', 'crop': 'ପ୍ରକାର ବାଛନ୍ତୁ',
             'get_recommendation': 'ସୁପାରିଶଗୁଡ଼ିକ ପାଇଁ', 'current_temp': 'ସାମ୍ପ୍ରତିକ ତାପମାନ', 'weather_desc': 'ଆବହା ଗତିବିଧିର ବିବରଣୀ',
             'soil_moisture': 'ମାଟିର ଆର୍ଦ୍ରତା', 'soil_temp': 'ମାଟିର ତାପମାନ', 'recommendations': 'ସୁପାରିଶଗୁଡ଼ିକ',
             'recommended_crop': 'ସୁପାରିଶ କରାଯାଇଥିବା ପିକ', 'fertilizer': 'ସୁପାରିଶ କରାଯାଇଥିବା ଖାଦ', 'fertilizer_brand': 'ସର୍ବୋତ୍ତମ ଓ ସସ୍ତା ଖାଦ ବ୍ରାଣ୍ଡ',
             'mixture_field': 'ମିଶଣ ଗଠନ', 'price_increase': 'ଆଶା କରାଯାଇଥିବା ମୂଲ୍ୟ ବୃଦ୍ଧି', 'acre_mixture': 'ଏକର ପ୍ରତି ମିଶ୍ରଣ ଗଠନ'},

    'Malayalam': {'title': 'വിവസായ ശിപാരശാ സിസ്റ്റം', 'location': 'നിങ്ങളുടെ സ്ഥലം നൽകുക (സംസ്ഥാനത്തിന്റെ പേര്)', 'crop': 'വിളയുടെ തരം തിരഞ്ഞെടുക്കുക',
                 'get_recommendation': 'ശിപാരശകൾ നേടുക', 'current_temp': 'നിലവിലെ താപനില', 'weather_desc': 'കാലാവസ്ഥയുടെ വിവരണം',
                 'soil_moisture': 'മണ്ണിലെ ഈർപ്പം', 'soil_temp': 'മണ്ണിലെ താപനില', 'recommendations': 'ശിപാരശകൾ',
                 'recommended_crop': 'ശിപാരശ ചെയ്ത വിള', 'fertilizer': 'ശിപാരശ ചെയ്ത വളം', 'fertilizer_brand': 'മികച്ചതും വിലകുറഞ്ഞതും വളം ബ്രാൻഡ്',
                 'mixture_field': 'മിശ്രിതം', 'price_increase': 'പ്രതീക്ഷിക്കുന്ന വില വർധന', 'acre_mixture': 'ഒരു ഏക്കറിൽ മിശ്രിതം'}
}

# API keys (add your keys here)
AGRO_API_KEY = '3b595ff753f913b88f558e67c2dc78d7'
WEATHER_API_KEY = '7040ea904442a45d6950ba584410ce59'

# Load the crop data from CSV file (ensure the file is uploaded or use file_uploader for dynamic loading)
#crop_data = pd.read_csv('crop2.csv')
# Load the crop data from CSV file (specify encoding to avoid UnicodeDecodeError)
crop_data = pd.read_csv('crop2.csv', encoding='ISO-8859-1')


# Select Language
language = st.selectbox('Select Language', ['English', 'Hindi', 'Bengali', 'Marathi', 'Telugu', 'Tamil', 'Gujarati', 'Urdu', 'Kannada', 'Odia', 'Malayalam'])
lang_dict = language_translations.get(language, language_translations['English'])

# Title
st.title(lang_dict['title'])

# Input location (State)
location = st.text_input(lang_dict['location'])

# Fetch weather and soil data if location is provided
if location:
    try:
        # Fetch Weather Data
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_api_url)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            st.write(f"{lang_dict['current_temp']}: {weather_data['main']['temp']} °C")
            st.write(f"{lang_dict['weather_desc']}: {weather_data['weather'][0]['description']}")

            # Extract latitude and longitude from the weather data
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']

            # Fetch Soil Data
            soil_api_url = f"https://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
            soil_response = requests.get(soil_api_url)
            soil_data = soil_response.json()

            if soil_response.status_code == 200:
                st.write(f"{lang_dict['soil_moisture']}: {soil_data['moisture']} %")
                st.write(f"{lang_dict['soil_temp']}: {soil_data['t0']} °C")
            else:
                st.write("Error retrieving soil data.")
        else:
            st.write("Error retrieving weather data.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

# Crop selection
crop_options = crop_data['Recommended Crop'].unique()
selected_crop = st.selectbox(lang_dict['crop'], crop_options)

# Display recommendations when button is clicked
if st.button(lang_dict['get_recommendation']):
    # Filter the crop data based on the selected crop
    selected_data = crop_data[crop_data['Recommended Crop'] == selected_crop]

    if not selected_data.empty:
        # Display relevant information
        st.write(f"{lang_dict['recommended_crop']}: {selected_crop}")
        st.write(f"{lang_dict['fertilizer']}: {selected_data['Recommended Fertilizer'].values[0]}")
        st.write(f"{lang_dict['fertilizer_brand']}: {selected_data['Best & Cheap Fertilizer Brand'].values[0]}")
        st.write(f"{lang_dict['mixture_field']}: {selected_data['Mixture Composition for Field'].values[0]}")
        st.write(f"{lang_dict['price_increase']}: {selected_data['Expected Price Value Increase'].values[0]}")
        st.write(f"{lang_dict['acre_mixture']}: {selected_data['Mixture Composition per Acre'].values[0]}")
    else:
        st.write("No recommendations available for the selected crop.")
