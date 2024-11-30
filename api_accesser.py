import requests
import utils

API_KEY = 'YjO0i7bzzeNZyuCYjO6EiMHpMOT7MxiZ' # ADD API KEY HERE

def curr_weather(units, user_input):
    lat, lon = utils.get_location(user_input)
    
    try:
        realtime = requests.get(
            f'https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&units={units}&apikey={API_KEY}')
        realtime.raise_for_status()
        r_data = realtime.json()
        
        forecast = requests.get(
            f'https://api.tomorrow.io/v4/weather/forecast?location={lat},{lon}&timesteps=1d&units={units}&apikey={API_KEY}')
        forecast.raise_for_status()
        f_data = forecast.json()
        
        r_values = r_data['data']['values']
        curr_day = f_data['timelines']['daily'][0]['values']
        day_1 = f_data['timelines']['daily'][1]['values']
        day_2 = f_data['timelines']['daily'][2]['values']
        day_3 = f_data['timelines']['daily'][3]['values']
        day_4 = f_data['timelines']['daily'][4]['values']
        day_5 = f_data['timelines']['daily'][5]['values']
        
        info = {
            'curr_day': {
                'date_time': utils.day_time(lat, lon, r_data['data']['time']),
                'desc': utils.weather_desc(r_values['weatherCode']),
                'humidity': round(r_values['humidity']),
                'pressure': round(r_values['pressureSurfaceLevel'], 1),
                'rain_chance': r_values['precipitationProbability'],
                'sunrise': curr_day['sunriseTime'],
                'sunset': curr_day['sunsetTime'],
                'temp': round(r_values['temperatureApparent']),
                'weather_code': r_values['weatherCode'],
                'wind_dir': r_values['windDirection'],
                'wind_speed': round(r_values['windSpeed'], 2),
                'uv_index': r_values['uvIndex'],
                'visibility': round(r_values['visibility'], 1),
            },
            'day_1': {
                'date': utils.acronym(utils.day_time(lat, lon, f_data['timelines']['daily'][1]['time'])[0]),
                'temp_min': round(day_1['temperatureMin']),
                'temp_max': round(day_1['temperatureMax']),
                'weather_code': day_1['weatherCodeMax'],
            },
            'day_2': {
                'date': utils.acronym(utils.day_time(lat, lon, f_data['timelines']['daily'][2]['time'])[0]),
                'temp_min': round(day_2['temperatureMin']),
                'temp_max': round(day_2['temperatureMax']),
                'weather_code': day_2['weatherCodeMax'],
            },
            'day_3': {
                'date': utils.acronym(utils.day_time(lat, lon, f_data['timelines']['daily'][3]['time'])[0]),
                'temp_min': round(day_3['temperatureMin']),
                'temp_max': round(day_3['temperatureMax']),
                'weather_code': day_3['weatherCodeMax'],
            },
            'day_4': {
                'date': utils.acronym(utils.day_time(lat, lon, f_data['timelines']['daily'][4]['time'])[0]),
                'temp_min': round(day_4['temperatureMin']),
                'temp_max': round(day_4['temperatureMax']),
                'weather_code': day_4['weatherCodeMax'],
            },
            'day_5': {
                'date': utils.acronym(utils.day_time(lat, lon, f_data['timelines']['daily'][5]['time'])[0]),
                'temp_min': round(day_5['temperatureMin']),
                'temp_max': round(day_5['temperatureMax']),
                'weather_code': day_5['weatherCodeMax'],
            },
            'lon': lon,
            'lat': lat
        }
        
        return info
    
    except requests.exceptions.HTTPError as err:
        if realtime.status_code == 401 or forecast.status_code == 401:
            return 'Invalid API key'
        elif realtime.status_code == 404 or forecast.status_code == 401:
            return 'No City Found'
        else:
            return f'HTTP error: {err}'
    except requests.exceptions.ConnectionError:
        return 'Connection error'
    except requests.exceptions.Timeout:
        return 'Timeout error'
    except requests.exceptions.RequestException as err:
        return f'Error: {err}'

print(curr_weather('imperial', 'Hong kong china'))