# API key: '79f7a1995bb5c8006f7f6ce7c542ce51'
import requests, time, pyglet, pyowm

location = 'Castelldefels, ES'

owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')

def get_epoch_time():
    seconds = time.time()
    return round(seconds)

def weather(location):
    loc = owm.weather_at_place(location)
    weather = loc.get_weather()
    temperature = weather.get_temperature('celsius')['temp']
    return weather, temperature

def forecasting(location):
    three_hour_forecast = owm.three_hours_forecast(location)
    rain = three_hour_forecast.will_have_rain()
    fog = three_hour_forecast.will_have_fog()
    clouds = three_hour_forecast.will_have_clouds()
    return rain, fog, clouds

def get_sunup_sundw_time(location):
    loc = owm.weather_at_place(location)
    weather = loc.get_weather()
    #sunup = weather.get_sunrise_time(timeformat='iso')[0:19] # Prints time in GMT timezone
    #sundw = weather.get_sunset_time(timeformat='iso')[0:19] # Prints time in GMT timezone
    sunup = weather.get_sunrise_time() # Prints time in GMT timezone
    sundw = weather.get_sunset_time()  # Prints time in GMT timezone
    return sunup, sundw

def sat_vis():
    uri = '''https://api.sat24.com/animated/SP/visual/1/width=400%20height=291'''
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

def sat_ir():
    uri = '''https://api.sat24.com/animated/SP/infraPolair/1/width=800%20height=582'''
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

def show_gif():
    ag_file = 'sat.gif'
    animation = pyglet.resource.animation(ag_file)
    sprite = pyglet.sprite.Sprite(animation)

    win = pyglet.window.Window(width=sprite.width, height=sprite.height)

    green = 0, 1, 0, 1
    pyglet.gl.glClearColor(*green)
    @win.event
    def on_draw():
        win.clear()
        sprite.draw()
    pyglet.app.run()

def select_sat_freq(location):
    c_time = get_epoch_time()
    ss_time = get_sunup_sundw_time(location)[1]
    su_time = get_sunup_sundw_time(location)[0]
    if (ss_time - c_time) > 0:
        sat_vis()
    elif (su_time - c_time) > 0:
        sat_ir()


select_sat_freq(location)
show_gif()


