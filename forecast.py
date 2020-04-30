import pyowm, requests
from geopy.geocoders import Nominatim
import certifi, ssl, geopy.geocoders

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

#OpenWeatherMaps API key
owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')




def generate_link(lat, lon):
    #Generate link with formatted coordinates for clearoutside.
    link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(lat, lon)
    return link

