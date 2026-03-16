import azure.functions as func
import datetime
import json
import logging
import os

from services.weather_service import get_weather

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 */15 * * * *",
    arg_name="timer",
    run_on_startup=True
)
def weather_collector(timer: func.TimerRequest) -> None:
    """
    Azure Function con Timer trigger.
    Se ejecuta cada 15 minutos y guarda datos meteorológicos en Blob Storage.
    """
    logging.info("WeatherCollector: iniciando ejecución")

    # Configuración desde variables de entorno
    city = os.environ.get("CITY_NAME", "Valencia")
    latitude = float(os.environ.get("CITY_LATITUDE", "39.4699"))
    longitude = float(os.environ.get("CITY_LONGITUDE", "-0.3763"))

    # Consultar la API meteorológica
    weather_data = get_weather(city, latitude, longitude)
    logging.info(f"Datos obtenidos: {weather_data['temperature_c']}°C en {city}")

    # Guardar en Blob Storage
    from azure.storage.blob import BlobServiceClient

    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = os.environ.get("WEATHER_CONTAINER_NAME", "weather-data")

    blob_name = f"weather_{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')}.json"

    blob_service = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service.get_container_client(container_name)

    container_client.upload_blob(
        name=blob_name,
        data=json.dumps(weather_data, indent=2),
        overwrite=True
    )

    logging.info(f"Datos guardados en Blob Storage: {blob_name}")
