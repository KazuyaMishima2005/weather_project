import requests
from typing import Dict, Optional

API_KEY = "e5ddeefb71500c6442ab1ade1aa0f76e"  # будет переопределяться через переменную окружения
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city: str, api_key: str) -> Optional[Dict]:
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def generate_recommendations(weather_data: dict) -> dict:
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description'].lower()
    humidity = weather_data['main']['humidity']

    recommendations = {
        "temperature": round(temp, 1),
        "description": description,
        "humidity": humidity,
        "take_umbrella": "дождь" in description or "ливень" in description,
        "wear_warm": temp < 0,
        "wear_light": temp > 25,
        "good_for_walk": 15 <= temp <= 25 and not ("дождь" in description)
    }
    return recommendations