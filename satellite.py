# API key: '79f7a1995bb5c8006f7f6ce7c542ce51'
import requests, time, pyglet, pyowm, ephem

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
    return rain, clouds, fog

def get_nit_r_day():
    observer = ephem.city('Barcelona') # <-- put your city here
    sun = ephem.Sun(observer)
    sun_is_up = observer.previous_rising(sun) > observer.previous_setting(sun)
    if sun_is_up:
        return 1
    else:
        return 0

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

def sat_img(location):
    tod = get_nit_r_day()
    if tod == 0:
        sat_ir()
    elif tod == 1:
        sat_vis()

sat_img(location)
show_gif()



#print('There is going to be', forecasting(location)[0], 'rain')
#print('There are going to be', forecasting(location)[1], 'clouds')
#print('There is going to be', forecasting(location)[2], 'fog')