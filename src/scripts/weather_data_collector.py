import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

def get_weather_data(lat, lon, timestamp):
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        weather_data = {
            "temperature": data.get("current", {}).get("temp"),
            "humidity": data.get("current", {}).get("humidity"),
            "weather_conditions": data.get("current", {}).get("weather", [{}])[0].get("description"),
            "timestamp": timestamp
        }
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados climáticos: {e}")
        return None
