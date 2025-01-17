from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import requests
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load models
model_1_data = joblib.load('model_1.pkl')
model_2_data = joblib.load('model_2.pkl')
model_3_data = joblib.load('model_3.pkl')

# Accuracy and predictions
accuracy_1 = model_1_data['accuracy']
accuracy_2 = model_2_data['accuracy']
accuracy_3 = model_3_data['accuracy']
predictions_1 = model_1_data['predictions']
predictions_2 = model_2_data['predictions']
predictions_3 = model_3_data['predictions']

# Weather fetching functions
def fetch_weatherbit_data(city_name):
    api_key = '57cac8d74936472e8650390b011cc6aa'
    url = f"http://api.weatherbit.io/v2.0/current?city={city_name}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": data['data'][0]['temp'],
            "feels_like": data['data'][0]['app_temp']
        }
    else:
        raise Exception("WeatherBit API request failed")

def fetch_openweathermap_data(city_name):
    api_key = '33cb808325c68f009bd043f19e5f591f'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": round(data['main']['temp'] - 273.15, 2),
            "feels_like": round(data['main']['feels_like'] - 273.15, 2)
        }
    else:
        raise Exception("OpenWeatherMap API request failed")

def fetch_weatherapi_data(city_name):
    api_key = 'c0b407bf72e34543a8765220241109'
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": data['current']['temp_c'],
            "feels_like": data['current']['feelslike_c']
        }
    else:
        raise Exception("WeatherAPI request failed")

# Function to fetch Model 3 predictions
def fetch_model3_prediction(api_url):
    response = requests.get(api_url + '/predict')
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": np.round(data['Random_Forest']['predictions'][0][0]).tolist(),
            "feels_like": np.round(data['Random_Forest']['predictions'][0][1]).tolist()
        }
    else:
        raise Exception("Failed to fetch Model 3 predictions")

# Model predictions endpoint
@app.route('/predict', methods=['GET'])
def predict():
    try:
        response = {
            "Multiple_Regression": {
                "accuracy": accuracy_1,
                "predictions": np.round(((predictions_1[0])-32)*(5/9)).tolist()
            },
            "Multivariate_Regression": {
                "accuracy": accuracy_2,
                "predictions": np.round(((predictions_2[0])-32)*(5/9)).tolist()
            },
            "Random_Forest": {
                "accuracy": accuracy_3,
                "predictions": np.round(((predictions_3[0])-32)*(5/9)).tolist()
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/compare/<city_name>', methods=['GET'])
def compare_weather(city_name):
    try:
        weatherbit_data = fetch_weatherbit_data(city_name)
        openweathermap_data = fetch_openweathermap_data(city_name)
        weatherapi_data = fetch_weatherapi_data(city_name)

        # Fetch Model 3 predictions
        model3_data = fetch_model3_prediction('http://localhost:5000')  

        # Calculate differences
        comparisons = {
            'WeatherBit': {
                'temp': weatherbit_data['temp'],
                'feels_like': weatherbit_data['feels_like']
            },
            'OpenWeatherMap': {
                'temp': openweathermap_data['temp'],
                'feels_like': openweathermap_data['feels_like'],
                'temp_diff': (weatherbit_data['temp'] - openweathermap_data['temp'])**2,
                'feels_like_diff': (weatherbit_data['feels_like'] - openweathermap_data['feels_like'])**2
            },
            'WeatherAPI': {
                'temp': weatherapi_data['temp'],
                'feels_like': weatherapi_data['feels_like'],
                'temp_diff': (weatherbit_data['temp'] - weatherapi_data['temp'])**2,
                'feels_like_diff': (weatherbit_data['feels_like'] - weatherapi_data['feels_like'])**2
            },
            'Random_Forest': {
                'temp': model3_data['temp'],
                'feels_like': model3_data['feels_like'],
                'temp_diff': (weatherbit_data['temp'] - model3_data['temp'])**2,
                'feels_like_diff': (weatherbit_data['feels_like'] - model3_data['feels_like'])**2
            }
        }

        return jsonify(comparisons)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
