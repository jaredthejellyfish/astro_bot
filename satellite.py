import requests
from urllib.request import urlopen
import json

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

def getplace(lat, lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAeegl5a8C2iHR4CUvcWIE1OOSfCHEnqZ0&"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return town, country

def get_country_code(country):
    if country and country in country_codes.keys():
        return country_codes[country]

def get_sat(lat, lon, chat_id='test_satellite_image'):
    country = getplace(lat, lon)[1]
    country_code = get_country_code(country)
    if country_code:
        uri = 'https://api.sat24.com/animated/{}/visual/1/Romance%20Standard%20Time/2964777'.format(country_code)
        with open('{}.gif'.format(chat_id), 'wb') as f:
            f.write(requests.get(uri).content)
        return True
    else:
        return False
