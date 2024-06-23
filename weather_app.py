import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

user_input = input("Enter city: ")

try:
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
    weather_data.raise_for_status()
    data = weather_data.json()

    if data['cod'] == '404':
        print("No City Found")
    else:
        weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        temp = round(data['main']['temp'])
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        print(f"Weather in {user_input}: {weather} ({description})")
        print(f"Temperature: {temp}ºF")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} mph")
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except requests.exceptions.ConnectionError as err:
    print(f"Error connecting: {err}")
except requests.exceptions.Timeout as err:
    print(f"Timeout error: {err}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
