from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

geolocator = Nominatim(user_agent="Mozilla/5.0")

def get_location(user_input):
    location_name = user_input

    location = geolocator.geocode(location_name)
    
    return location.latitude, location.longitude

def acronym(day):
    match day:
        case 'Monday':
            return 'Mon'
        case 'Tuesday':
            return 'Tue'
        case 'Wednesday':
            return 'Wed'
        case 'Thursday':
            return 'Thu'
        case 'Friday':
            return 'Fri'
        case 'Saturday':
            return 'Sat'
        case 'Sunday':
            return 'Sun'
        case _:
            return day

def day_time(lat, lon, utc_time):
    utc_time = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
    
    tf = TimezoneFinder()
    time_zone = tf.timezone_at(lat=lat, lng=lon)
    
    if time_zone is None:
        return 'Timezone Not Found'
    
    local_tz = pytz.timezone(time_zone)
    local_time = utc_time.astimezone(local_tz)
    
    day_of_week = local_time.strftime('%A')
    curr_time = local_time.strftime('%H:%M %Z')

    return [day_of_week, curr_time]

def weather_desc(weather_code):
    match weather_code:
        case 1000:
            return 'Clear'
        case 1100:
            return 'Mostly Clear'
        case 1101:
            return 'Partly Cloudy'
        case 1102:
            return 'Mostly Cloudy'
        case 1001:
            return 'Cloudy'
        case 2000:
            return 'Fog'
        case 2100:
            return 'Light Fog'
        case 4000:
            return 'Drizzle'
        case 4001:
            return 'Rain'
        case 4200:
            return 'Light Rain'
        case 4201:
            return 'Heavy Rain'
        case 5000:
            return 'Snow'
        case 5001:
            return 'Flurries'
        case 5100:
            return 'Light Snow'
        case 5101:
            return 'Heavy Snow'
        case 6000:
            return 'Freezing Drizzle'
        case 6001:
            return 'Freezing Rain'
        case 6200:
            return 'Light Freezing Rain'
        case 6201:
            return 'Heavy Freezing Rain'
        case 7000:
            return 'Ice Pellets'
        case 7101:
            return 'Heavy Ice Pellets'
        case 7102:
            return 'Light Ice Pellets'
        case 8000:
            return 'Thunderstorm'
        case _:
            return 'Unknown Weather Code'