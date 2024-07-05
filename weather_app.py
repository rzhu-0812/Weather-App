import requests
import os
from geopy.geocoders import Nominatim
import customtkinter as ctk
from PIL import Image

geolocator = Nominatim(user_agent='geoapiExercises')

user_input = ''
units = 'metric'
api_key = 'API KEY'
city_location = ''
coordinates = ''

location_info = {
    'country': '',
    'city': '',
    'weather': '',
    'temp': '',
    'humidity': '',
    'air_pressure': '',
    'wind_speed': '',
    'wind_deg': '',
    'icon_code': ''
}

wind_direction_img = {
    'N': 'N.png',
    'NE': 'NE.png',
    'E': 'E.png',
    'SE': 'SE.png',
    'S': 'S.png',
    'SW': 'SW.png',
    'W': 'S.png',
    'NW': 'NW.png'
}

def get_weather_info():
    try:
        weather_data = requests.get(
            f'https://api.tomorrow.io/v4/weather/forecast?location={coordinates}&apikey={api_key}&units={units}')
        weather_data.raise_for_status()
        data = weather_data.json()


        return ''

    except requests.exceptions.HTTPError as err:
        if weather_data.status_code == 401:
            return 'Invalid API key'
        elif weather_data.status_code == 404:
            return 'No City Found'
        else:
            return f'HTTP error: {err}'
    except requests.exceptions.ConnectionError:
        return 'Connection error'
    except requests.exceptions.Timeout:
        return 'Timeout error'
    except requests.exceptions.RequestException as err:
        return f'Error: {err}'

def getWindDirection(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    return directions[round(deg / 45) % 8] 

def getWeatherImage():
    global location_info

    response = requests.get(f'http://openweathermap.org/img/wn/{location_info['icon_code']}@2x.png')
    icon_img = Image.open(BytesIO(response.content))
    ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(75, 75))
    
    weather_icon.configure(image=ctk_img)

def getWindImage():
    global location_info

    cardinal_direction = getWindDirection(location_info['wind_deg'])
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images/Wind_Direction")
    icon_img = Image.open(os.path.join(image_path, wind_direction_img[cardinal_direction]))
    ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(50, 50))

    wind_icon.configure(image=ctk_img)

def getPressureImage():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images")
    icon_img = Image.open(os.path.join(image_path, 'pressure.png'))
    ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(50, 50))

    pressure_icon.configure(image=ctk_img)

def getHumidityImage():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images")
    icon_img = Image.open(os.path.join(image_path, 'humidity.png'))
    ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(50, 50))

    humidity_icon.configure(image=ctk_img)

def outputData():
    global location_info, units, city_location

    city_label.configure(text=f'{city_location}')

    temp_frame.configure(fg_color='gray86')
    wind_frame.configure(fg_color='gray86')
    pressure_frame.configure(fg_color='gray86')
    humidity_frame.configure(fg_color='gray86')

    getWeatherImage()
    getWindImage()
    getPressureImage()
    getHumidityImage()

    pressure_label.configure(text=f'{location_info['air_pressure']}hPa')
    humidity_label.configure(text=f'{location_info['humidity']}%')

    if units == 'metric':
        temp_label.configure(text=f'{location_info['temp']}°C')
        wind_speed.configure(text=f'{location_info['wind_speed']}m/s {getWindDirection(location_info['wind_deg'])}')
    else:
        temp_label.configure(text=f'{location_info['temp']}°F')
        wind_speed.configure(text=f'{location_info['wind_speed']}mph {getWindDirection(location_info['wind_deg'])}')

def getCityInfo(user_location):
    global geolocator, coordinates, city_location

    location = geolocator.geocode(user_location)
    coordinates = f'{location.latitude}, {location.longitude}'

    location = geolocator.reverse((location.latitude, location.longitude), exactly_one=True)
    city_location = location.address
    
def retrieveInput():
    global user_input

    user_input = entry.get()
    weather_data = get_weather_info()

    getCityInfo(user_input)

    if weather_data:
        error_label.configure(text=weather_data)

        city_label.configure(text='')
        temp_label.configure(text='')
        wind_speed.configure(text='')
        pressure_label.configure(text='')
        humidity_label.configure(text='')

        temp_frame.configure(fg_color='transparent')
        wind_frame.configure(fg_color='transparent')
        pressure_frame.configure(fg_color='transparent')
        humidity_frame.configure(fg_color='transparent')

        weather_icon.configure(image=None)
        wind_icon.configure(image=None)
        pressure_icon.configure(image=None)
        humidity_icon.configure(image=None)
    else:
        error_label.configure(text='')
        outputData()

def changeUnits(value):
    global units, location_info

    if 'Metric' in value:
        units = 'metric'
    else:
        units = 'imperial'
    
    if not all(value == '' for value in location_info.values()):
        retrieveInput()

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('600x300')
root.title('CustomTkinter Weather App')

entry = ctk.CTkEntry(root, width=225, placeholder_text='Enter Location: city, state, country')
entry.place(x=10, y=5)

submit = ctk.CTkButton(root, text='Submit', width=75, command=retrieveInput)
submit.place(x=240, y=5)

units_selection = ctk.CTkSegmentedButton(root, values=['Metric: °C, m/s', 'Imperial: °F, mph'], command=changeUnits)
units_selection.place(x=350, y=5)
units_selection.set('Metric: °C, m/s')

error_label = ctk.CTkLabel(root, text='', font=('Microsoft JhengHei UI', 25, 'bold'))
error_label.place(x=10, y=50)

city_label = ctk.CTkLabel(root, text='', font=('Microsoft JhengHei UI', 25, 'bold'))
city_label.place(x=10, y=50)

temp_frame = ctk.CTkFrame(root, width=225, height=70, corner_radius=10, fg_color='transparent')
temp_frame.place(x=10, y=100)

wind_frame = ctk.CTkFrame(root, width=225, height=70, corner_radius=10, fg_color='transparent')
wind_frame.place(x=10, y=175)

pressure_frame = ctk.CTkFrame(root, width=225, height=70, corner_radius=10, fg_color='transparent')
pressure_frame.place(x=240, y=100)

humidity_frame = ctk.CTkFrame(root, width=225, height=70, corner_radius=10, fg_color='transparent')
humidity_frame.place(x=240, y=175)

weather_icon = ctk.CTkLabel(temp_frame, text='')
weather_icon.place(x=0, y=-2)

wind_icon = ctk.CTkLabel(wind_frame, text='')
wind_icon.place(x=10, y=10)

pressure_icon = ctk.CTkLabel(pressure_frame, text='')
pressure_icon.place(x=10, y=10)

humidity_icon = ctk.CTkLabel(humidity_frame, text='')
humidity_icon.place(x=10, y=10)

temp_label = ctk.CTkLabel(temp_frame, text='', font=('Yu Gothic UI Light', 25))
temp_label.place(x=75, y=15)

wind_speed = ctk.CTkLabel(wind_frame, text='', font=('Yu Gothic UI Light', 25))
wind_speed.place(x=75, y=15)

pressure_label = ctk.CTkLabel(pressure_frame, text='', font=('Yu Gothic UI Light', 25))
pressure_label.place(x=75, y=15)

humidity_label = ctk.CTkLabel(humidity_frame, text='', font=('Yu Gothic UI Light', 25))
humidity_label.place(x=75, y=15)

root.mainloop()
