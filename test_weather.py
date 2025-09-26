import unittest
from unittest.mock import patch, Mock
import requests
from weather import get_weather_data, generate_recommendations

class TestWeather(unittest.TestCase):

    @patch('weather.requests.get')
    def test_get_weather_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Moscow",
            "sys": {"country": "RU"},
            "main": {"temp": 18.5, "humidity": 65},
            "weather": [{"description": "облачно"}]
        }
        mock_get.return_value = mock_response

        result = get_weather_data("Moscow", "fake_key")
        self.assertIsNotNone(result)
        self.assertEqual(result["main"]["temp"], 18.5)

    @patch('weather.requests.get')
    def test_get_weather_data_failure_network(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection failed")
        result = get_weather_data("Moscow", "fake_key")
        self.assertIsNone(result)

    @patch('weather.requests.get')
    def test_get_weather_data_failure_http_404(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_weather_data("NonExistentCityXYZ", "fake_key")
        self.assertIsNone(result)

    def test_generate_recommendations_rainy_cold(self):
        data = {
            "main": {"temp": -2.3, "humidity": 85},
            "weather": [{"description": "умеренный дождь"}],
            "sys": {"country": "RU"}
        }
        rec = generate_recommendations(data)
        self.assertTrue(rec["take_umbrella"])
        self.assertTrue(rec["wear_warm"])
        self.assertFalse(rec["wear_light"])
        self.assertFalse(rec["good_for_walk"])

    def test_generate_recommendations_sunny_warm(self):
        data = {
            "main": {"temp": 28.0, "humidity": 40},
            "weather": [{"description": "ясно"}],
            "sys": {"country": "ES"}
        }
        rec = generate_recommendations(data)
        self.assertFalse(rec["take_umbrella"])
        self.assertFalse(rec["wear_warm"])
        self.assertTrue(rec["wear_light"])
        self.assertFalse(rec["good_for_walk"])  # >25°C — не идеально для прогулки

    def test_generate_recommendations_perfect_walk(self):
        data = {
            "main": {"temp": 20.0, "humidity": 60},
            "weather": [{"description": "небольшая облачность"}],
            "sys": {"country": "DE"}
        }
        rec = generate_recommendations(data)
        self.assertFalse(rec["take_umbrella"])
        self.assertFalse(rec["wear_warm"])
        self.assertFalse(rec["wear_light"])
        self.assertTrue(rec["good_for_walk"])


if __name__ == '__main__':
    unittest.main()