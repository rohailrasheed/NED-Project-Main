# -*- coding: utf-8 -*-
"""Weather Temperature Fetcher.ipynb"""

import requests
import json

# OpenWeatherMap API Fetch
def fetch_openweathermap(city_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    
    temp = round(((data['main']['temp']) - 273.15), 2)
    feels_like = round(((data['main']['feels_like']) - 273.15), 2)
    
    return {"source": "OpenWeatherMap", "temp": temp, "feels_like": feels_like}

# WeatherAPI Fetch
def fetch_weatherapi(city_name, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=no"
    response = requests.get(url)
    data = response.json()
    
    temp = data['current']['temp_c']
    feels_like = data['current']['feelslike_c']
    
    return {"source": "WeatherAPI", "temp": temp, "feels_like": feels_like}

# WeatherBit API Fetch
def fetch_weatherbit(city_name, api_key):
    url = f"http://api.weatherbit.io/v2.0/current?city={city_name}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    temp = data['data'][0]['temp']
    feels_like = data['data'][0]['app_temp']
    
    return {"source": "WeatherBit", "temp": temp, "feels_like": feels_like}

# Fetch Model 3 predictions (assuming API endpoint is available)
def fetch_model3_prediction(api_url):
    response = requests.get(api_url + '/predict')  # Modify if the path is different
    data = response.json()
    
    # Fetch the first prediction for both temp and feels_like
    model3_temp = data['Random Forest']['predictions'][0][0] # Fetch single prediction
    model3_feels_like = data['Random Forest']['predictions'][0][1]  # Adjust based on your actual data structure
    
    return {"source": "Random Forest", "temp": model3_temp, "feels_like": model3_feels_like}

# Define API keys
openweathermap_api_key = '33cb808325c68f009bd043f19e5f591f'
weatherapi_key = 'c0b407bf72e34543a8765220241109'
weatherbit_api_key = '57cac8d74936472e8650390b011cc6aa'
model3_api_url = 'http://localhost:5000'

city_name = "Pakistan"

# Fetch temperatures from all APIs
openweathermap_data = fetch_openweathermap(city_name, openweathermap_api_key)
weatherapi_data = fetch_weatherapi(city_name, weatherapi_key)
weatherbit_data = fetch_weatherbit(city_name, weatherbit_api_key)
model3_data = fetch_model3_prediction(model3_api_url)

# Compile results
results = [openweathermap_data, weatherapi_data, weatherbit_data, model3_data]

# Comparison through Mean Square Method
comp_temp_openweathermap = (weatherbit_data['temp'] - openweathermap_data['temp'])**2
comp_app_openweathermap = (weatherbit_data['feels_like'] - openweathermap_data['feels_like'])**2

comp_temp_weatherapi = (weatherbit_data['temp'] - weatherapi_data['temp'])**2
comp_app_weatherapi = (weatherbit_data['feels_like'] - weatherapi_data['feels_like'])**2

comp_temp_model3 = (weatherbit_data['temp'] - model3_data['temp'])**2
comp_app_model3 = (weatherbit_data['feels_like'] - model3_data['feels_like'])**2

# Print results
for result in results:
    print(f"Source: {result['source']}")
    print(f"Temperature: {result['temp']} °C")
    print(f"Feels Like: {result['feels_like']} °C")

