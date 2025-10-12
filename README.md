🌾Crop Optimization App
Overview

The Crop Optimization App is a data-driven mobile solution designed to empower farmers with real-time insights to maximize crop yields. The app integrates weather data, soil fertility information, and a comprehensive crop database to provide personalized fertilizer recommendations, optimal application methods, and crop management suggestions.

This project leverages Python, Streamlit, and external APIs to deliver a user-friendly, multilingual web interface for farmers.

Features

🌦️ Real-time weather updates including temperature, humidity, and forecasts

🌱 Soil fertility data including moisture and temperature

🌾 Crop recommendations based on soil and weather conditions

🧪 Personalized fertilizer suggestions with optimal mixing ratios

🌐 Multilingual support: English, Hindi, Bengali, Marathi, Telugu, Tamil, Gujarati, Urdu, Kannada, Odia, Malayalam

📊 Interactive frontend built with Streamlit

Installation & Setup

Clone the repository

git clone https://github.com/your-username/agritech.git
cd agritech


Install dependencies

pip install -r requirements.txt


Add API keys
Create a file named .env or use environment variables:

export WEATHER_API_KEY=your_openweathermap_key
export AGRO_API_KEY=your_agromonitoring_key


Run the app

streamlit run app.py

File Structure
agritech/
├── app.py                  # Main Streamlit app
├── crop2.csv               # Crop and fertilizer data
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignore unnecessary files

How to Use

Select your preferred language

Enter your location (state name)

Choose a crop type

Click Get Recommendations

View weather, soil, and fertilizer suggestions

Technologies Used

Python

Streamlit

Pandas

Requests (API calls)

OpenWeatherMap API

AgroMonitoring API
