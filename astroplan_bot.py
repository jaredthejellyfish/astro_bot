#Bot:
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

#Astronomy
from astroquery.simbad import Simbad

#Gneral:
import logging, os, requests, json, time

#Custom functions:
from forecast import generate_link, basic_forecast
from satellite import sat_img, sat_gif2mp4, clean
from platesolve import astrometry_job_run, platesolver_results
from sky_coords import find_object_fname


#Initial text for when the bot is initialised with /start
start_text = '''
Hey!

Welocme to AstroPlan, a bot designed to make you astronomy planning journey esier. 

These are the commands you can currently use: 
•   /sat (region) (name of city) - Pulls cloud images from a satellite.
•   /fc (name of city) - Generates a forecast for that city.
•   /solve - Platesolves a star image.
•   /find (c) - Finds object from name, c flag enables finding through coordinates.
•   /help - List of all available commands.
'''

#Text for /help
help_text = '''
These are the commands you can currently use: 
•   /sat (region) (name of city) - Pulls cloud images from a satellite.
•   /fc (name of city) - Generates a forecast for that city.
•   /solve - Platesolves a star image.
•   /find (c) - Finds object from name, c flag enables finding through coordinates.
•   /help - List of all available commands.
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
    #Send beginning string.
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)

#Generation of forecast url and submission to user.
def forecast(update, context):
    #Pull city string from /fc "..."
    usr_city = context.args
    try:
        #Format string, generate forecast url, send message with image and string as caption.
        stringreturn = "Forecast for {} coming right up!".format(" ".join(usr_city).title())
        url = generate_link(usr_city)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=stringreturn)
    except:
        #Non valid city name exception
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city name.")

#Generation and upload of Satellite images for user.
def satellite(update, context):
    try:
        #Format context (region and user city)
        usr_city = " ".join(context.args[1:])
        region_code = "".join(context.args[0]).upper()
        #Generate caption text.
        caption_text = basic_forecast(usr_city)
        #Pull satellite image
        sat_img(emphem_city, region_code) 
        #Convert gif to mp4 with ffmpeg.
        sat_gif2mp4()
        #Send message with video and forecasted caption
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('sat.mp4', 'rb'), caption=caption_text)
        #Remove video file from working dir
        clean()
    except:
        #Invalid city name exception reporting
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid city or region name.")

#Unknown command handling.
def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I haven't been programmed to understand that command.")

#Normal text (no "/"") detection and handling.
def not_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="My master hasn't taught me how to read normal text, please send a command.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

#Astrometry upload, solving, and result fetching asynchronously to not stall the rest.
@run_async
def platesolve_image(update, context):
    global solving
    #Trigger solver if it is enabled.
    if solving == 1:
        try:
            #Pull file id from telegram servers.
            file_id = str(update.message.document.file_id)
            #Generate "Logged in with id: x & send it."
            login_text = astrometry_job_run(file_id, bot_token)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Loged into nova.astrometry.net with session id: {}.".format(login_text[0]))
            #Succesful file upload.
            context.bot.send_message(chat_id=update.effective_chat.id, text='File successfully uploaded with submission id: {}. \nResults can take up to 5 minutes to be generated, you can still send any other commands during this time.'.format(login_text[1]))
            #Pull, format and send astrometry results.
            results = platesolver_results(login_text[1])
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=results[0], caption=results[1])
            print('solver_finished')
        except:
            try:
                #Pull photo id from telegram servers.
                photo_id = str(update.message.photo[-1].file_id)
                #Generate "Logged in with id: x & send it."
                login_text = astrometry_job_run(photo_id, bot_token)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Loged into nova.astrometry.net with session id: {}.".format(login_text[0]))
                #Succesful file upload.
                context.bot.send_message(chat_id=update.effective_chat.id, text='File successfully uploaded with job id: {}. \nResults can take up to 5 minutes to be generated, you can still send any other commands during this time.'.format(login_text[1]))
                #Pull, format and send astrometry results.
                results = platesolver_results(login_text[1])
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=results[0], caption=results[1])
                print('solver_finished') 
            except:
                #Handle oversize exception
                context.bot.send_message(chat_id=update.effective_chat.id, text="Your file is too large :(")
                raise
    else:
        #Handle non-armed platesolver exception.
        context.bot.send_message(chat_id=update.effective_chat.id, text="Enable the solver to read image data.")
    
#Enable or disable input for image detection and upload.
def platesolve_enable(update, context):
    global solving
    enable_flag = ''
    try:
        enable_flag = context.args[0].lower()
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide the requiered arguments.")
    if enable_flag == 'enable':
        solving = 1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Solver enabled")
    elif enable_flag == 'disable':
        solving = 0
        context.bot.send_message(chat_id=update.effective_chat.id, text="Solver disabled")
    #Armed message send.
    time.sleep(0.2)
    
def find(update, context):
    try:
        object_by_coords_flag = context.args[0]
        if object_by_coords_flag == 'c':
            print("lookupbycoords")
            object_coords_lst = context.args[1:]
            #object_name = " ".join(object_name_lst).title()
            #radec = find_object_fname(object_name)
            context.bot.send_message(parse_mode='HTML', chat_id=update.effective_chat.id, text=object_coords_lst)
        else:
            object_name_lst = context.args
            object_name = " ".join(object_name_lst).title()
            radec = find_object_fname(object_name)
            context.bot.send_message(parse_mode='HTML', chat_id=update.effective_chat.id, text=radec)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide the requiered arguments.")
        exit
    

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
solve_handler = CommandHandler('solver', platesolve_enable)
dispatcher.add_handler(solve_handler)

#Handler for ofind.
find_handler = CommandHandler('find', find)
dispatcher.add_handler(find_handler)

#Handler for help.
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

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