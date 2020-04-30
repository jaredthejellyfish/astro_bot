from pygeocoder import Geocoder
import pyowm
import requests
import configparser

class Forecast:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        gc_key = config['API_KEYS']['geocoder']
        owm_key = config['API_KEYS']['owm']

        self.gc = Geocoder(gc_key)
        self.owm = pyowm.OWM(owm_key)

    def generate_link(self, lat, lon):
        #Generate link with formatted coordinates for clearoutside.
        link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(lat, lon)
        return link

   