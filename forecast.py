import configparser

from pygeocoder import Geocoder
import pyowm

class Forecast:
    def __init__(self):
        # Read OpenWeatherMaps and Gogle Geocoding API_KEYS from 'config.ini'
        config = configparser.ConfigParser()
        config.read('config.ini')
        gc_key = config['API_KEYS']['geocoder']
        owm_key = config['API_KEYS']['owm']

        # Create owm and geoc objects and assign them to self.
        self.owm = pyowm.OWM(owm_key)
        self.geoc = Geocoder(gc_key)


    def generate_link(self, lat, lon):
        #Generate link with formatted coordinates for clearoutside.
        link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(round(lat,2), round(lon,2))

        return link
    

    def get_forecast(self, lat, lon):
        # Use reverse geolocation to find name of nearest city
        results = self.geoc.reverse_geocode(lat, lon)
        usr_city = results.city

        # Use owm object to get weather for the nearest city
        loc = self.owm.weather_at_place(usr_city)
        weather = loc.get_weather()

        #Temperature 
        temperature = weather.get_temperature('celsius')['temp']
        #Humidity
        humidity = weather.get_humidity()
        #Wind Speed
        wind = weather.get_wind()
        #Forecast over the next 3h.
        three_hour_forecast = self.owm.three_hours_forecast(usr_city)
        #Is it gonna rain?
        rain = three_hour_forecast.will_have_rain()
        #Are clouds gonna roll in?
        clouds = three_hour_forecast.will_have_clouds()

        return rain, clouds, temperature, humidity, wind


    def generate_text(self, lat, lon):
        # Get FORECAST from .get_forecast() method
        results = self.get_forecast(lat, lon)

        # Generate return TEXT for forecast
        if results[0] is True:
            return 'Looks like there is going to be some rain...'

        if results[0] is False and results[1] is True:
            return 'It shall be slightly cloudy!'

        else:
            return 'Looks like the weather is going to be pretty nice'

    def get_fc(self, lat, lon):
        # Generate TEXT and LINK from .generate_text() and .generate_link() methods
        text = self.generate_text(lat, lon)
        link = self.generate_link(lat, lon)
        
        return link, text