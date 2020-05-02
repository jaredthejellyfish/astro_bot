from forecast import Forecast
from satellite import Satellite
from platesolve import Platesolver

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

running_solver = {}

class AstroBot:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.db = {}

    def sat_gif(self, update, context):
        ready_message = context.bot.send_message(chat_id=self.chat_id, text= 'Getting your forecast ready...')
        outputs = sat.get_sat(lat, lon, self.chat_id)
        if outputs[0]:
            return True
        else:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Here is your forecast... ')
            context.bot.send_animation(chat_id=self.chat_id, 
                                       animation= open(str(self.chat_id)+'.gif', 'rb'), 
                                       caption=outputs[1], 
                                       parse_mode=telegram.ParseMode.HTML)
            sat.cleanup(self.chat_id)

    def clo_forecast(self, update, context):
        clo_url, text = fc.get_fc(lat, lon)
        context.bot.sendPhoto(chat_id=self.chat_id, photo=clo_url, caption=text)


@run_async
def manage_bot(update, context):
    chat_id = update.effective_chat.id
    ab = AstroBot(chat_id)
    ab.sat_gif(update, context)
        
@run_async
def platesolve_image(update, context):
    file_id = update.message.photo[-1].file_id
    chat_id = update.message.chat_id
    if chat_id not in running_solver.keys():
        pl = Platesolver(chat_id)
        running_solver[chat_id] = pl
        if pl.platesolve(file_id, context, update) is False:
            try:
                del running_solver[chat_id]
            except KeyError:
                print("Key {} not found".format(chat_id))
    else:
        context.bot.send_message(chat_id=chat_id, text= 'The solver is already running, I can only handle one image per user.')
    

image_platesolve_handler = MessageHandler(Filters.photo, platesolve_image)
dispatcher.add_handler(image_platesolve_handler)    
    

plain_text_handler = MessageHandler(Filters.text, manage_bot)
dispatcher.add_handler(plain_text_handler)

updater.start_polling()