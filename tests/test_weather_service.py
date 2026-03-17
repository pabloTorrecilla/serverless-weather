import pytest
from unittest.mock import patch, Mock
from services.weather_service import get_weather


MOCK_RESPONSE = {
    "current": {
        "temperature_2m": 22.5,
        "relative_humidity_2m": 65,
        "wind_speed_10m": 12.3,
        "time": "2026-03-16T12:00"
    }
}


def test_get_weather_returns_correct_structure():
    """Verifica que get_weather devuelve la estructura de datos correcta."""
    with patch("services.weather_service.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = MOCK_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_weather("Valencia", 39.4699, -0.3763)

        assert result["city"] == "Valencia"
        assert result["temperature_c"] == 22.5
        assert result["humidity_percent"] == 65
        assert result["wind_speed_kmh"] == 12.3


def test_get_weather_uses_correct_coordinates():
    """Verifica que get_weather pasa las coordenadas correctas a la API."""
    with patch("services.weather_service.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = MOCK_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        get_weather("Valencia", 39.4699, -0.3763)

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["params"]["latitude"] == 39.4699
        assert call_kwargs["params"]["longitude"] == -0.3763


def test_get_weather_raises_on_timeout():
    """Verifica que get_weather propaga el error cuando la API no responde."""
    import requests as req
    with patch("services.weather_service.requests.get") as mock_get:
        mock_get.side_effect = req.exceptions.Timeout()

        with pytest.raises(req.exceptions.Timeout):
            get_weather("Valencia", 39.4699, -0.3763)
            