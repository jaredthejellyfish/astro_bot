#Bot key:  965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests, re, os
from satellite import forecasting

def generate_forecast():
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

def start(bot, update):
    print("rec")
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, text="Hey, welcome to astroplan V0.1!")

def forecast(bot, update):
    url = 'https://clearoutside.com/forecast_image_large/41.33/1.99/forecast.png'
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url, caption="Foreccast right up.")

def satellite(bot, update):
    os.system('python3 satellite.py')
    chat_id = update.message.chat_id
    bot.send_video(chat_id=chat_id, video=open('sat.mp4', 'rb'), caption=generate_forecast())

def main():
    updater = Updater('965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s', request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('forecast', forecast))
    dp.add_handler(CommandHandler('sat', satellite))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()