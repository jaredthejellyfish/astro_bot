#Bot key:  965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests, re, os
from satellite import clean
from forecast import forecasting

def start(bot, update):
    print("rec")
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Hey!\nWelocme to astroplan, a bot designed to make you astronomy planning journey esier. \nThese are the current commands you can use: \n· /sat - Pulls cloud images from a satellite. \n· /forecast - Generates a forecast for the nearest city to you.")

def caps(update, context):
    print("abc")
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def forecast(bot, update):
    url = 'https://clearoutside.com/forecast_image_large/41.33/1.99/forecast.png'
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url, caption="Foreccast right up.")

def generate_forecast_satellite():
    location = 'Castelldefels, ES'
    unf_forecasting = forecasting(location)
    if unf_forecasting[0] == True:
        return "Damn, it looks like there is gonna be some rain. I wouldn't recommend bringing out the telescope tonight."
    elif unf_forecasting[1] == True:
        return "Oh no, it looks like there are gonna be some clouds!"
    elif unf_forecasting[3] > 50:
        return "Careful, there are going to be no clouds or rain, but the humidity is going to be a little high."
    else:
        return "All clear! Looks like you'll be having some fun :)."

def satellite(bot, update):
    os.system('python3 satellite.py')
    chat_id = update.message.chat_id
    bot.send_video(chat_id=chat_id, video=open('sat.mp4', 'rb'), caption=generate_forecast_satellite())
    clean()

def main():
    updater = Updater('965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s', request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('caps', caps))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('forecast', forecast))
    dp.add_handler(CommandHandler('sat', satellite))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()