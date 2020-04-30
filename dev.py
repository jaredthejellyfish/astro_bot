from pygeocoder import Geocoder
import configparser
import requests
from pprint import pprint

config = configparser.ConfigParser()
config.read('config.ini')

gc_key = config['API_KEYS']['geocoder']
owm_key = config['API_KEYS']['owm']

gc = Geocoder(gc_key)
results = gc.reverse_geocode(41.28610, 1.98241)

city = results.city

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, owm_key)

res = requests.get(url)

data = res.json()

temp = data['main']['temp']
wind_speed = data['wind']['speed']

latitude = data['coord']['lat']
longitude = data['coord']['lon']

description = data['weather'][0]['description']

print('Temperature : {} degree celcius'.format(temp))
print('Wind Speed : {} m/s'.format(wind_speed))
print('Description : {}'.format(description))