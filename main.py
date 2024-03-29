from forecast import Forecast
from satellite import Satellite
from platesolve import Platesolver
from db_man import Database
from soho import Soho
from sdss_finder import SDSS
from all_sky import AllSky

import telegram
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater, dispatcher, run_async
from telegram import update

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

telegram_token = config['API_KEYS']['telegram']

updater = Updater(token=telegram_token, use_context=True)

dispatcher = updater.dispatcher

running_solver = {}
running_bot = {}

class AstroBot:      
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.get_location()
        self.f_obj_mode = False

        self.sat = Satellite()
        self.fc = Forecast()
        self.soho = Soho()
        self.sdss = SDSS()
        self.alsk = AllSky()

    def sat_gif(self, update, context):
        ready_message = context.bot.send_message(chat_id=self.chat_id, text= 'Getting your forecast ready...')
        outputs = self.sat.get_sat(self.lat, self.lon, self.chat_id)
        if outputs[0]:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Oh no! Looks like there was an error getting your forecast :( \nPlease try again later.')
        else:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Here is your forecast... ')
            context.bot.send_animation(chat_id=self.chat_id, 
                                        animation= open(str(self.chat_id)+'.gif', 'rb'), 
                                        caption=outputs[1], 
                                        parse_mode=telegram.ParseMode.HTML)
            self.sat.cleanup(self.chat_id)

    def clo_forecast(self, update, context,):
        clo_url, text = self.fc.get_fc(self.lat, self.lon)
        context.bot.sendPhoto(chat_id=self.chat_id, photo=clo_url, caption=text)

    def soho_gif(self, update, context):
        ready_message = context.bot.send_message(chat_id=self.chat_id, text= 'Getting your SOHO animation ready...')
        output = self.soho.get_gif(self.chat_id)
        if output:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Oh dang! Looks like there was an error getting your GIF :( \nPlease try again later.')
        else:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Here is your gif, careful, its hot... ')
            context.bot.send_video( chat_id=self.chat_id, 
                                    video= open('soho_' + str(self.chat_id) + '.mp4', 'rb')) 

            self.soho.cleanup(self.chat_id)

    def find_object(self, update, context):
        output = self.sdss.get_SDDS(update, context, self.chat_id)
        ready_message = context.bot.send_message(chat_id=self.chat_id, text= 'Getting your SDSS image and coordinates ready...')
        if output[0] == False:
            context.bot.sendPhoto(  chat_id=self.chat_id, 
                                    photo=open('SDSS_' + str(self.chat_id) + '.jpg', 'rb'), 
                                    caption=output[1],
                                    parse_mode=telegram.ParseMode.HTML)
            self.sdss.cleanup(self.chat_id)
        elif output[0] == True:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Oh no! Looks like there was an error getting your object :( \nPlease try again later.')

    def all_sky(self, update, context):
        ready_message = context.bot.send_message(chat_id=self.chat_id, text= 'Getting your All Sky image ready...')
        if self.alsk.get_jpg(self.chat_id):
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Oh no! Looks like there was an error getting your image :( \nPlease try again later.')
        else:
            context.bot.edit_message_text(chat_id=self.chat_id, message_id=ready_message.message_id, text='Here is your image... ')
            context.bot.sendPhoto(chat_id=self.chat_id, 
                                        photo= open('allsky_{}.jpg'.format(self.chat_id), 'rb'), 
                                        caption='Looks like the sky is still there!', 
                                        parse_mode=telegram.ParseMode.HTML)
            self.alsk.cleanup(self.chat_id)

    def gage_intent(self, update, context):
            if update.message.text == 'Find Object' or self.f_obj_mode == True:
                if self.f_obj_mode == False:
                    context.bot.send_message(chat_id=self.chat_id, text= 'What object would you like to find?')
                    self.f_obj_mode = True

                elif self.f_obj_mode == True:
                    self.f_obj_mode = False
                    self.find_object(update, context)

            if update.message.text == 'Satellite Forecast':
                if self.get_location():
                    self.askfor_location(update, context)
                    return
                self.sat_gif(update, context)

            if update.message.text == 'Clearoutside Forecast':
                if self.get_location():
                    self.askfor_location(update, context)
                    return
                self.clo_forecast(update, context)

            if update.message.text == 'SOHO Latest':
                if self.get_location():
                    self.askfor_location(update, context)
                    return
                self.soho_gif(update, context)

            if update.message.text == 'AllSky Image':
                if self.get_location():
                    self.askfor_location(update, context)
                    return
                self.all_sky(update, context)

    def get_location(self):
        db = Database()
        stat = db.get_user(self.chat_id)
        del db
        if stat is not True:
            self.lat, self.lon, self.time = stat
        else:
            return True

    def askfor_location(self, update, context):
        context.bot.send_message(chat_id=self.chat_id, text= 'Looks like I don\'t have your location. \nCould you tap the Update Location button?')

@run_async
def manage_bot(update, context):
    chat_id = update.effective_chat.id

    if chat_id not in running_bot.keys():
        bot = AstroBot(chat_id)
        running_bot[chat_id] = bot
        bot.gage_intent(update, context)

    else:
        bot = running_bot[chat_id]
        bot.gage_intent(update, context)
        
@run_async
def platesolve_image(update, context):
    file_id = update.message.photo[-1].file_id
    chat_id = update.message.chat_id

    if chat_id not in running_solver.keys():
        pl = Platesolver(chat_id)
        running_solver[chat_id] = pl

        if pl.platesolve(file_id, context, update) is False:
            try:
                running_solver.pop(chat_id)
            except KeyError:
                print("Key {} not found".format(chat_id))

    else:
        context.bot.send_message(chat_id=chat_id, text= 'The solver is already running, I can only handle one image per user.')

@run_async
def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Welocme to AstroPlan! \nA bot designed to make you astronomy planning journey esier.")

    location_keyboard = telegram.KeyboardButton(text="Send my location!", request_location=True)
    custom_keyboard = [[location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id, 
                    text="\nMost of my services are location based so I'm gonna need your location to work. Press the button below if you would like to share it with me.", 
                    reply_markup=reply_markup)

@run_async
def location(update, context):
    chat_id = update.message.chat_id

    user_location = update.message.location
    lat = round(user_location.latitude, 5)
    lon = round(user_location.longitude,5)
    db = Database()
    db.upd_user(chat_id, lat, lon)
    del db

    loc_button = telegram.KeyboardButton(text="Update Location", request_location=True)
    custom_keyboard = [['Satellite Forecast', 'Clearoutside Forecast'], 
                       ['SOHO Latest', 'Find Object', 'AllSky Image'],
                       [loc_button]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id, 
                    text="Awesome! I'll put it in the database so you can use it later :)", 
                    reply_markup=reply_markup)

image_platesolve_handler = MessageHandler(Filters.photo, platesolve_image)
dispatcher.add_handler(image_platesolve_handler)    

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

plain_text_handler = MessageHandler(Filters.text, manage_bot)
dispatcher.add_handler(plain_text_handler)

updater.start_polling()