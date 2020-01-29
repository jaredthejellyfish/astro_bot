import pyowm, requests
from geopy.geocoders import Nominatim
import certifi, ssl, geopy.geocoders

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

#OpenWeatherMaps API key
owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')

def basic_forecast(usr_city):
    #Current forecast.
    loc = owm.weather_at_place(usr_city)
    weather = loc.get_weather()
    #Temperature 
    temperature = weather.get_temperature('celsius')['temp']
    #Humidity
    humidity = weather.get_humidity()
    #Wind Speed
    wind_speed = weather.get_wind()

    #Forecast over the next 3h.
    three_hour_forecast = owm.three_hours_forecast(usr_city)
    #Is it gonna rain?
    rain = three_hour_forecast.will_have_rain()
    #Are clouds gonna roll in?
    clouds = three_hour_forecast.will_have_clouds()

    #Return all collected values.
    return rain, clouds, temperature, humidity, wind_speed

def generate_coords(usr_city):
    geolocator = Nominatim(user_agent='domesticmexican')
    location = geolocator.geocode(usr_city)
    city_lat = round(location.latitude, 2)
    city_lon = round(location.longitude, 2)
    return city_lat, city_lon

def generate_link(usr_city):
    coords = generate_coords(usr_city)
    link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(coords[0], coords[1])
    return link
