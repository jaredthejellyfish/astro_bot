import requests, ephem, os

#Clear working directory of any video or gif files.
def clean():
    try:
        os.remove('sat.mp4')
        os.remove('sat.gif')
    except:
        return "Neat dirs."

#Check if it's night or day.
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

#Pull visual band gif.
def sat_vis(region):
    #Pull visual light gif from Sat24
    uri = '''https://api.sat24.com/animated/{}/visual/1/width=400%20height=291'''.format(region)
    #Write pulled gif to the 'sat.gif' 
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

#Pull ir band gif.
def sat_ir(region):
    #Pull IR gif from Sat24
    uri = '''https://api.sat24.com/animated/{}/infraPolair/1/width=800%20height=582'''.format(region)
    #Write pulled gif to the 'sat.gif' 
    with open('sat.gif', 'wb') as f:
        f.write(requests.get(uri).content)

#Select satellite band according to the time of day.
def sat_img(emphem_city, region):
    tofd = get_nit_r_day(emphem_city)
    if tofd == 0:
        sat_ir(region)
    elif tofd == 1:
        sat_vis(region)

#Convert gif to mp4 file.
def sat_gif2mp4():
    os.system('ffmpeg -hide_banner -loglevel panic -r 5 -i sat.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" sat.mp4 -y')

#Pre-clear directory to avoid junk files.
clean()