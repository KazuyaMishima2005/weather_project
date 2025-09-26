import os
from flask import Flask, jsonify, request
from weather import get_weather_data, generate_recommendations

app = Flask(__name__)

# Получаем API-ключ из переменной окружения
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise EnvironmentError("Требуется переменная окружения OPENWEATHER_API_KEY")

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Параметр 'city' обязателен"}), 400

    data = get_weather_data(city, API_KEY)
    if not data:
        return jsonify({"error": "Город не найден или ошибка API"}), 404

    recommendations = generate_recommendations(data)
    return jsonify({
        "city": data["name"],
        "country": data["sys"]["country"],
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))