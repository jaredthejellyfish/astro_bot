from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from forecast import generate_link, basic_forecast
from satellite import sat_img, sat_gif2mp4
import logging, os
from start_text import start_text

emphem_city = 'Barcelona'

updater = Updater(token='965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)

def not_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't quite get that. Try using an actual command.")

def forecast(update, context):
    usr_city = context.args
    try:
        stringreturn = "Forecast for {} right up!".format(" ".join(usr_city).title())
        url = generate_link(usr_city)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=stringreturn)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city name.")
    
def caps(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="got sum thicc context")

def satellite(update, context):
    try:
        usr_city = " ".join(context.args[1:])
        region_code = "".join(context.args[0])
        caption_text = basic_forecast(usr_city)
        sat_img(emphem_city, region_code) 
        sat_gif2mp4()
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('sat.mp4', 'rb'), caption=caption_text)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city name.")


caps_handler = CommandHandler('title', caps)
dispatcher.add_handler(caps_handler)

caps_handler = CommandHandler('fc', forecast)
dispatcher.add_handler(caps_handler)

caps_handler = CommandHandler('sat', satellite)
dispatcher.add_handler(caps_handler)

echo_handler = MessageHandler(Filters.text, not_command)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()