from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram.ext as telegram
from forecast import generate_link, basic_forecast
from satellite import sat_img, sat_gif2mp4, clean
from astrometry import upload, check_status
import logging, os, requests, json, time

#Initial text for when the bot is initialised with /start
start_text = '''
Hey!

Welocme to AstroPlan, a bot designed to make you astronomy planning journey esier. 

These are the current commands you can currently use: 
•   /sat (region) (name of city) - Pulls cloud images from a satellite.
•   /fc (name of city) - Generates a forecast for that city.
'''

#City for ephemeris, it sucks.
emphem_city = 'Barcelona'

#Solving status global var
solving = 0

#Telegram bot token 
bot_token = '965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s'

#Initialization of the updater object
updater = Updater(token=bot_token, use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Initialization of the dispatcher
dispatcher = updater.dispatcher

#Bot initialized with /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)

#Generation of forecast url and submission to user.
def forecast(update, context):
    usr_city = context.args
    try:
        stringreturn = "Forecast for {} coming right up!".format(" ".join(usr_city).title())
        url = generate_link(usr_city)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=stringreturn)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city name.")

#Generation and upload of Satellite images for user.
def satellite(update, context):
    try:
        usr_city = " ".join(context.args[1:])
        region_code = "".join(context.args[0])
        caption_text = basic_forecast(usr_city)
        sat_img(emphem_city, region_code) 
        sat_gif2mp4()
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('sat.mp4', 'rb'), caption=caption_text)
        clean()
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city or region name.")

#Unknown command handling.
def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I haven't been programmed to understand that command.")

#Normal text (no "/"") detection and handling.
def not_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="My master hasn't taught me how to read normal text, please send a command.")

#Astrometry upload, solving, and result fetching.
def platesolve_image(update, context):
    global solving
    if solving == 1:
        try:
            file_id = str(update.message.document.file_id)
            upload(file_id, bot_token)
            check_status()
        except:
            pass

        try:
            photo_id = str(update.message.photo[-1].file_id)
            upload(photo_id, bot_token)
            print(photo_id)
            
        except :
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your file is too large :(")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Send a command before uploading a picture")
    solving = 0

#Enabler for image detection and upload.
def platesolve(update, context):
    global solving
    solving = 1
    
#Handler for forecast.
fc_handler = CommandHandler('fc', forecast)
dispatcher.add_handler(fc_handler)

#Handler for satellite.
sat_handler = CommandHandler('sat', satellite)
dispatcher.add_handler(sat_handler)

#Handler dor start.
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Handler for platesolver.
solve_handler = CommandHandler('solve', platesolve)
dispatcher.add_handler(solve_handler)

#Handler for image solving.
platesolve_image_handler = MessageHandler(Filters.photo | Filters.document, platesolve_image)
dispatcher.add_handler(platesolve_image_handler, group=1)

#Handler for normal text (not prefaced by "/")
not_command_handler = MessageHandler(Filters.text, not_command)
dispatcher.add_handler(not_command_handler)

#Handler for unknown commands.
unknown_command_handler = MessageHandler(Filters.command, unknown_command)
dispatcher.add_handler(unknown_command_handler)

#Start the updater.
updater.start_polling()