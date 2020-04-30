import requests
from urllib.request import urlopen
import json
from pygeocoder import Geocoder

gc = Geocoder('AIzaSyAeegl5a8C2iHR4CUvcWIE1OOSfCHEnqZ0')

country_codes = {'Germany':'DE', 
                 'Spain':'SP', 
                 'France':'FR', 
                 'Italy':'IT', 
                 'Scandinavia':'SCAN', 
                 'Great Britain':'GB', 
                 'Poland':'PL', 
                 'Greece':'GR', 
                 'Turkey':'TU', 
                 'Russia':'RU', 
                 'Bosnia and Herzegovina':'BA', 
                 'Null':'BC', 
                 'Sweden':'SE', 
                 'Hungary':'HU', 
                 'United Kingdom':'UK'
                }

def get_country_code(lat, lon):
    results = gc.reverse_geocode(lat, lon)
    country = results.country
    if country and country in country_codes.keys():
        return country_codes[country]

def get_sat(lat, lon, chat_id='test_satellite_image'):
    country_code = get_country_code(lat, lon)
    if country_code:
        uri = 'https://api.sat24.com/animated/{}/visual/1/Romance%20Standard%20Time/2964777'.format(country_code)
        with open('{}.gif'.format(chat_id), 'wb') as f:
            f.write(requests.get(uri).content)
        return True
    else:
        return False
