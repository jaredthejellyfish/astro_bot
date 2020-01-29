import requests, time, pyowm, ephem, os, ffmpy


location = 'Castelldefels, ES'
emphem_city = 'Barcelona'

#OpenWeatherMaps API key
owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')

def get_epoch_time():
    #Get time
    seconds = time.time()
    #Return rounded time in seconds
    return round(seconds)

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

def get_nit_r_day(emphem_city):
    #Generate observer object with location
    observer = ephem.city(emphem_city)
    #Generate sun object with observer
    sun = ephem.Sun(observer)
    #Check if sun is currently up
    sun_is_up = observer.previous_rising(sun) > observer.previous_setting(sun)
    #Return boolean value depending on time of day
    if sun_is_up:
        return True
    else:
        return False

def sat_vis():
    #Pull visual light gif from Sat24
    uri = '''https://api.sat24.com/animated/SP/visual/1/width=400%20height=291'''
    #Write pulled gif to the 'sat.gif' 
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

def sat_ir():
    #Pull IR gif from Sat24
    uri = '''https://api.sat24.com/animated/SP/infraPolair/1/width=800%20height=582'''
    #Write pulled gif to the 'sat.gif' 
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

def sat_img(location,emphem_city):
    tod = get_nit_r_day(emphem_city)
    if tod == 0:
        sat_ir()
    elif tod == 1:
        sat_vis()

def sat_gif2mp4():
    os.system('ffmpeg -hide_banner -loglevel panic -r 5 -i sat.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" sat.mp4 -y')
    os.remove('sat.gif')

try:
    os.remove('sat.mp4')
    os.remove('sat.gif')
except:
    print("")

sat_img(location,emphem_city)
sat_gif2mp4()

