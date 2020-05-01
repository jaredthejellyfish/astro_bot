from forecast import Forecast
from satellite import Satellite

import telegram
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater, dispatcher, run_async
from telegram import update

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

telegram_token = config['API_KEYS']['telegram']

updater = Updater(token=telegram_token, use_context=True)

dispatcher = updater.dispatcher

lat, lon = 41.28610, 1.98241

sat = Satellite()
fc = Forecast()

class AstroBot:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.db = {}

    def sat_gif(self, update, context):
        outputs = sat.get_sat(lat, lon, self.chat_id)
        if outputs[0]:
            return True
        else:
            print(outputs[1])
            context.bot.send_photo(chat_id=update.effective_chat.id, parse_mode='HTML', photo=open(str(self.chat_id)+'.gif', 'rb'), caption=outputs[1])
        
    


@run_async
def manage_bot(update, context):
    chat_id = update.effective_chat.id
    ab = AstroBot(chat_id)
    ab.sat_gif(update, context)
        
    
    

plain_text_handler = MessageHandler(Filters.text, manage_bot)
dispatcher.add_handler(plain_text_handler)

updater.start_polling()