import configparser
import requests
import json
import time

import telegram

class Platesolver:
    def __init__(self, chat_id):
        # Read ASTROMETRY in API_KEYS from 'config.ini'
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.ast_key = config['API_KEYS']['astrometry']
        self.bot_key = config['API_KEYS']['telegram']

        # Assign CHAT_ID to self.
        self.chat_id = chat_id


    def astrometry_login(self, context, update):
        # Generate json formatted url with API key
        login = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": self.ast_key})}).json()
        self.session_id = login["session"]

        # Status message for the user to be updated
        self.status_message = context.bot.send_message(chat_id=self.chat_id, text= 'Logged into astrometry.net with session id: {}'.format(self.session_id))
        time.sleep(5) # Enough time to read the message


    def generate_file_url(self, file_id):
        #Generate url based on bot key and file ID
        url_file_path = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.bot_key, file_id)
        file_path = requests.get(url_file_path).json()['result']['file_path']

        #Test if request got an appropriate response
        if file_path == None:
            exit
        else:
            # Generate URL from FILE_PATH
            self.file_url = 'https://api.telegram.org/file/bot{}/{}'.format(self.bot_key, file_path)

    def upload(self, context, update):
        # Upload image at FILE_URL to astrometry.net
        out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": self.session_id, "url": self.file_url,"publicly_visible":"n"})}).json()
        self.sub_id = out["subid"]

        # Update the user status message
        context.bot.edit_message_text(chat_id=self.chat_id, message_id=self.status_message.message_id, text='File uploaded to astrometry.net with submission id: {}'.format(self.sub_id))
        
    def get_jobid(self):
        # Loops until a request with a job_id value is received
        while True:
            time.sleep(1)
            try:
                # Requests the submission info json from nova.astrometry.net/api/submissions
                status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(self.sub_id)
                submissions_request = requests.post(status_check_url).json()
                # Extracts job_id from json
                self.job_id = submissions_request['jobs'][0]
                if self.job_id:
                    break
            except:
                pass

    def check_status(self, context, update):
        # Update user status message
        context.bot.edit_message_text(chat_id=self.chat_id, message_id=self.status_message.message_id, text='File being solved with job id: {}'.format(self.job_id))

        # Get nova.astrometry.net/api/jobs/ JSON query
        status_check_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id)
        while True:
            try:
                out = requests.post(status_check_url).json()
                # Save the status field into a variable
                status = out['status']
                # Check if status is success or failure and return things accordingly
                if status == 'success':
                    time.sleep(10)
                    break
                elif status == 'failure':
                    return True
                else:
                    break
            except:
                break

    def get_ra_dec_tags(self):
        # Query nova.astrometry.net/api/jobs/JOBID/info/
        tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id) +'/info/'
        try:
            # Extract RA & DEC fields
            radec = requests.post(tags_url).json()
            ra = radec['calibration']['ra']
            dec = radec['calibration']['dec']
            # Format RA & DEC into a string.
            self.result_radec_string = ["<b>The center of the image is at:</b>\n ○ RA:  {}\n ○ DEC:  {}\n".format(ra, dec),'\n']
        except:
            self.get_ra_dec_tags() 
    
    def get_tags_objects(self):
        # Query nova.astrometry.net/api/jobs/JOBID/info/
        tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id) +'/info/'
        try:
            # Extract tags fields
            tags = requests.post(tags_url).json()
            self.mac_tags = tags['tags']
            print(self.mac_tags)
        except:
            return None

    def generate_text_and_image(self):
        self.annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(self.job_id)
        radec_string = self.result_radec_string
        # Format tagged objects and append them to the initial RA & DEC list.
        if len(self.mac_tags) > 0:
            radec_string.append('<b>Found the following objects:</b>\n')
            for tag in self.mac_tags:
                radec_string.append('   ○ ' + tag + '\n')
        else:
            radec_string.append('<b>No named objects could be found.</b>')

        self.solved_image_caption = "".join(radec_string)

    def send_messages(self, context, update, error=False):
        if error is True:
            context.bot.send_message(chat_id=self.chat_id, text= 'Looks like I failed to solve your image, please try again.')
        
        context.bot.edit_message_text(chat_id=self.chat_id, message_id=self.status_message.message_id, text='File solved! Here are your results:')
        context.bot.send_photo(chat_id=update.effective_chat.id, 
                               photo=self.annotated_url, 
                               caption=self.solved_image_caption, 
                               parse_mode=telegram.ParseMode.HTML)
        

    def platesolve(self, file_id, context, update):
        self.astrometry_login(context, update)
        self.generate_file_url(file_id)
        self.upload(context, update)
        self.get_jobid()
        if self.check_status(context, update):
            self.send_messages(context, update, True)
            return True
        self.get_ra_dec_tags()
        self.get_tags_objects()
        self.generate_text_and_image()
        self.send_messages(context, update)
        return False