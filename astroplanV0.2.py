from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from forecast import generate_link, basic_forecast

updater = Updater(token='965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey!\nWelocme to astroplan, a bot designed to make you astronomy planning journey esier. \nThese are the current commands you can use: \n· /sat - Pulls cloud images from a satellite. \n· /fc (name of city) - Generates a forecast for the nearest city to you.")

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


caps_handler = CommandHandler('title', caps)
dispatcher.add_handler(caps_handler)

caps_handler = CommandHandler('fc', forecast)
dispatcher.add_handler(caps_handler)

echo_handler = MessageHandler(Filters.text, not_command)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()