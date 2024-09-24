from geopy.geocoders import Nominatim
from datetime import datetime

geolocator = Nominatim(user_agent="Mozilla/5.0")

location_name = "New York City"

location = geolocator.geocode(location_name)

print(f"Location: {location.address}")
print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")

print(datetime.today().strftime("%A"))