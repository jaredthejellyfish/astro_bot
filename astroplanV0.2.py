from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from forecast import generate_link, basic_forecast
from satellite import sat_img, sat_gif2mp4, clean
import logging, os

start_text = '''
Hey!

Welocme to AstroPlan, a bot designed to make you astronomy planning journey esier. 

These are the current commands you can currently use: 
•   /sat (region) (name of city) - Pulls cloud images from a satellite.
•   /fc (name of city) - Generates a forecast for that city.
'''

emphem_city = 'Barcelona'

solving = 0

updater = Updater(token='965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


dispatcher = updater.dispatcher

def removeTelegramMessageHandler(self, handler):
        """
        De-registers a message handler.
        Args:
            handler (any):
        """

        if handler in self.telegram_message_handlers:
            self.telegram_message_handlers.remove(handler)



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)

def forecast(update, context):
    usr_city = context.args
    try:
        stringreturn = "Forecast for {} coming right up!".format(" ".join(usr_city).title())
        url = generate_link(usr_city)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=stringreturn)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city name.")
    
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

def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I haven't been programmed to understand that command.")

def not_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="My master hasn't taught me how to read normal text, please send a command.")

def platesolve_image(update, context):
    global solving
    if solving == 1:
        try:
            print("photo")
            file = context.bot.getFile(update.message.photo[-1].file_id)
            print ("file_id: " + str(update.message.photo[-1].file_id))
            file.download('image')
        except:
            print("other")
            exit
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Send a command before uploading a picture")
    
    solving = 0
    print(solving)

def platesolve(update, context):
    global solving
    print("platesolver engaged")
    solving = 1
    

fc_handler = CommandHandler('fc', forecast)
dispatcher.add_handler(fc_handler)

sat_handler = CommandHandler('sat', satellite)
dispatcher.add_handler(sat_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

solve_handler = CommandHandler('solve', platesolve)
dispatcher.add_handler(solve_handler)

platesolve_image_handler = MessageHandler(Filters.photo | Filters.document, platesolve_image)
dispatcher.add_handler(platesolve_image_handler, group=1)

not_command_handler = MessageHandler(Filters.text, not_command)
dispatcher.add_handler(not_command_handler)

unknown_command_handler = MessageHandler(Filters.command, unknown_command)
dispatcher.add_handler(unknown_command_handler)


updater.start_polling()