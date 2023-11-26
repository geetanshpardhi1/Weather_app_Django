from django.shortcuts import render
import requests
import datetime

def index(request):
    # api_key = open("/home/geetansh/API_KEY","r").read()
    api_key ='76b657ee31af664ffd4b74f957a85d0f'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat={}&lon={}&cnt=7&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'myapp/index.html', context)
    else:
        return render(request, 'myapp/index.html')

#this function requests through api for weather data
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    print(response)
    print(forecast_response)
    daily_forecasts = []
    for daily_data in forecast_response["list"]:
        daily_forecasts.append({
        "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
        "min_temp": round(daily_data["temp"]["min"] - 273.15, 2),
        "max_temp": round(daily_data["temp"]["max"] - 273.15, 2),
        "description": daily_data["weather"][0]["description"],
        "icon": daily_data["weather"][0]["icon"],
    })
    
    return weather_data, daily_forecasts