import pyowm

#OpenWeatherMaps API key
owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')

location = 'Castelldefels, ES'

def forecasting(location):
    #Current forecast.
    loc = owm.weather_at_place(location)
    weather = loc.get_weather()
    #Temperature 
    temperature = weather.get_temperature('celsius')['temp']
    #Humidity
    humidity = weather.get_humidity()
    #Wind Speed
    wind_speed = weather.get_wind()

    #Forecast over the next 3h.
    three_hour_forecast = owm.three_hours_forecast(location)
    #Is it gonna rain?
    rain = three_hour_forecast.will_have_rain()
    #Are clouds gonna roll in?
    clouds = three_hour_forecast.will_have_clouds()

    #Return all collected values.
    return rain, clouds, temperature, humidity, wind_speed