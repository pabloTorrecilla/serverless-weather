import requests
import logging

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str, latitude: float, longitude: float) -> dict:
    """
    Consulta la API de Open-Meteo y devuelve los datos meteorológicos actuales.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Europe/Madrid"
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        return {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": data["current"]["temperature_2m"],
            "humidity_percent": data["current"]["relative_humidity_2m"],
            "wind_speed_kmh": data["current"]["wind_speed_10m"],
            "timestamp": data["current"]["time"]
        }

    except requests.exceptions.Timeout:
        logging.error("Timeout al conectar con Open-Meteo")
        raise
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error HTTP de Open-Meteo: {e}")
        raise
    except Exception as e:
        logging.error(f"Error inesperado consultando Open-Meteo: {e}")
        raise
