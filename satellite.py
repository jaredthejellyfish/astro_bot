import configparser
import requests
import time
import os

from pygeocoder import Geocoder
import pyowm


class Satellite:
    def __init__(self):
        # Read OpenWeatherMaps and Gogle Geocoding API_KEYS from 'config.ini'
        config = configparser.ConfigParser()
        config.read('config.ini')
        gc_key = config['API_KEYS']['geocoder']
        owm_key = config['API_KEYS']['owm']

        # Create owm and geoc objects and assign them to self.
        self.owm = pyowm.OWM(owm_key)
        self.geoc = Geocoder(gc_key)

        # Country codes dicionary for SAT24
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
        # Get country name by reverse geocoding
        results = self.geoc.reverse_geocode(lat, lon)
        country = results.country

        # Match country name to country code from COUNTRY_CODES
        if country and country in self.country_codes.keys():
            return self.country_codes[country]


    def down_sat(self, lat, lon, freq, chat_id='test_satellite_image'):
        # Get country code using .get_country_code() method
        country_code = self.get_country_code(lat, lon)

        # Download current SAT24 image and wite it to temp file named CHAT_ID
        if country_code:
            try:
                # Form URL using passed in details (COUNTRY_CODE, FREQ)
                uri = 'https://api.sat24.com/animated/{}/{}/1/Romance%20Standard%20Time/'.format(country_code, freq)
                # Download file from URL and name it CHAT_ID
                with open('{}.gif'.format(chat_id), 'wb') as f:
                    f.write(requests.get(uri).content)
            except:
                # Set ERROR flag in case of failure to download file from SAT24
                return True
        else:
            # Retrun ERROR flag in case of no country code having been generated
            return True


    def get_sat(self, lat, lon, chat_id='test_satellite_image'):
        # Gets time of day from .day_or_night()
        time_od = self.day_or_night(lat, lon)

        # Set error flag if location cannot be gaged
        if time_od == None:
            return True, '0'

        # Get DAY sat image from .down_sat() method
        if time_od == True:
            # Set ERROR flag accordingly to .down_sat() output
            error = self.down_sat(lat, lon, 'visual', chat_id)
            # Get forecast text from .sat_fc()
            fc = self.sat_fc(lat, lon)
            return error, fc

        # Get NIGHT sat image from .down_sat() method
        elif time_od == False:
            # Set ERROR flag accordingly to .down_sat() output
            error = self.down_sat(lat, lon, 'infraPolair', chat_id)
            # Get forecast text from .sat_fc()
            fc = self.sat_fc(lat, lon)
            return error, fc

        # Set ERROR flag if no time of day could be selected
        else:
            return True, '0'


    def day_or_night(self, lat, lon):
        # Use reverse geolocation to find name of nearest city
        results = self.geoc.reverse_geocode(lat, lon)
        self.city = results.city

        try:
            # Use owm object to get weather for the nearest city
            city = self.owm.weather_at_place(self.city)
            weather = city.get_weather()
        except:
            return None
            
        # Return TRUE if time.time() is between SUNSIE and SUNSET (daytime) 
        if int(time.time()) > weather.get_sunrise_time(timeformat='unix') and int(time.time()) < weather.get_sunset_time(timeformat='unix'):
            return True
        else:
            return False


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


    def sat_fc(self, lat, lon):
        # Get forecasted values from .get_forecast() method
        rain, clouds, temperature, humidity, wind = self.get_forecast(lat, lon)

        # Form forecast string to be returned to the user, variable values are bolded in HTML (<b>{}</b>)
        fc = 'Looks like it will '
        if rain == True:
            fc += 'rain in {}.\n'.format(self.city)

        if clouds == True and rain == False:
            fc += 'be cloudy in {}.\n'.format(self.city)

        elif rain is not True and clouds is not False:
            fc += 'be clear in {}!\n'.format(self.city)

        fc += 'The current themperature is <b>{}ºC</b> and the humidity is <b>{}%</b>.\n'.format(temperature, humidity)
        
        if 'deg' in wind.keys():
            if wind['speed'] > 5:
                fc += 'There might be some shaking caused by the wind, the current wind speed is <b>{}m/s</b> and its heading is <b>{}º</b>.'.format(wind['speed'], wind['deg'])
            else:
                fc += 'There shouldn\'t be much shaking caused by the wind, the current wind speed is <b>{}m/s</b> and its heading is <b>{}º</b>.'.format(wind['speed'], wind['deg'])
        else:
            fc += 'Looks like there is no wind.'

        return fc


    def cleanup(self, chat_id):
        # Clean directory after use of the image
        os.remove(str(chat_id) + '.gif')