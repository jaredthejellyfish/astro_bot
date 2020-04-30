import requests
from urllib.request import urlopen
import json
from pygeocoder import Geocoder
import configparser
import pyowm
import time

class Satellite:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        gc_key = config['API_KEYS']['geocoder']
        owm_key = config['API_KEYS']['owm']
        self.owm = pyowm.OWM(owm_key)
        self.gc = Geocoder(gc_key)
        self.country_codes = {'Germany':'DE', 
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

    def get_country_code(self, lat, lon):
        results = self.gc.reverse_geocode(lat, lon)
        country = results.country
        if country and country in self.country_codes.keys():
            return self.country_codes[country]

    def down_sat_vis(self, lat, lon, chat_id='test_satellite_image'):
        country_code = self.get_country_code(lat, lon)
        if country_code:
            uri = 'https://api.sat24.com/animated/{}/visual/1/Romance%20Standard%20Time/2964777'.format(country_code)
            with open('{}.gif'.format(chat_id), 'wb') as f:
                f.write(requests.get(uri).content)
            return True
        else:
            return False

    def down_sat_ir(self, lat, lon, chat_id='test_satellite_image'):
        country_code = self.get_country_code(lat, lon)
        if country_code:
            uri = 'https://api.sat24.com/animated/{}/infraPolair/1/Romance%20Standard%20Time/2964777'.format(country_code)
            with open('{}.gif'.format(chat_id), 'wb') as f:
                f.write(requests.get(uri).content)
            return True
        else:
            return False

    def get_sat(self, lat, lon, chat_id='test_satellite_image'):
        if self.day_or_night(lat, lon) == True:
            status = self.down_sat_vis(lat, lon, chat_id)
            fc = self.sat_fc(lat, lon)
            return status, fc

        if self.day_or_night(lat, lon) == False:
            status = self.down_sat_ir(lat, lon, chat_id)
            fc = self.sat_fc(lat, lon)
            return status, fc

    def day_or_night(self, lat, lon):
        results = self.gc.reverse_geocode(lat, lon)
        city = results.city
        city = self.owm.weather_at_place(city)
        weather = city.get_weather()
        if int(time.time()) > weather.get_sunrise_time(timeformat='unix') and int(time.time()) < weather.get_sunset_time(timeformat='unix'):
            return True
        elif int(time.time()) > weather.get_sunrise_time(timeformat='unix') and int(time.time()) > weather.get_sunset_time(timeformat='unix'):
            return False

    def get_3h_forecast(self, lat, lon):
        results = self.gc.reverse_geocode(lat, lon)
        usr_city = results.city
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
        #Return all collected values.
        return rain, clouds, temperature, humidity, wind

    def sat_fc(self, lat, lon):
        rain, clouds, temperature, humidity, wind = self.get_3h_forecast(lat, lon)
        #fc = 'Looks like it will {}. The current temperature is {}ºC and the humidity is {}%. {}, the wind speed is {}.'
        fc = 'Looks like it will '
        if rain == True:
            fc += 'rain.\n'
        if clouds == True:
            fc += 'be cloudy.\n'
        else:
            fc += 'be clear!\n'
        fc += 'The current themperature is {}ºC and the humidity is {}%.\n'.format(temperature, humidity)
        if wind['speed'] > 5:
            fc += 'There might be some shaking caused by the wind, the current wind speed is {}m/s and the heading is {}º.'.format(wind['speed'], wind['deg'])
        return fc