import configparser
import requests
import json
import time

class Platesolver:
    def __init__(self, chat_id):
        # Read ASTROMETRY in API_KEYS from 'config.ini'
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.ast_key = config['API_KEYS']['astrometry']
        self.bot_key = config['API_KEYS']['telegram']

        # Assign CHAT_ID to self.
        self.chat_id = chat_id

    def astrometry_login(self):
        #Generate json formatted url with API key
        login = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": self.ast_key})}).json()
        self.session_id = login["session"]

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

    def upload(self):
        out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": self.session_id, "url": self.file_url,"publicly_visible":"n"})}).json()
        self.sub_id = out["subid"]
        
    def get_jobid(self):
        #Loops until a request with a job_id value is received
        while True:
            time.sleep(1)
            try:
                #Requests the submission info json from nova.astrometry.net/api/submissions
                status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(self.sub_id)
                submissions_request = requests.post(status_check_url).json()
                #Extracts job_id from json
                self.job_id = submissions_request['jobs'][0]
                if self.job_id:
                    break
            except:
                pass

    def check_status(self):
        #Get nova.astrometry.net/api/jobs/ JSON query
        status_check_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id)
        while True:
            print('solving...')
            time.sleep(1)
            try:
                out = requests.post(status_check_url).json()
                #Save the status field into a variable
                status = out['status']
                #Check if status is success or failure and return things accordingly
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
        #Query nova.astrometry.net/api/jobs/JOBID/info/
        tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id) +'/info/'
        try:
            #Extract RA & DEC fields
            radec = requests.post(tags_url).json()
            ra = radec['calibration']['ra']
            dec = radec['calibration']['dec']
            #Format RA & DEC into a string.
            self.result_radec_string = ["The center of the image is at:\n ○ RA:  {}\n ○ DEC:  {}\n".format(ra, dec),'\n' , 'Found the following objects:\n']
        except:
            pass 
    
    def get_tags_objects(self):
        time.sleep(10)
        #Query nova.astrometry.net/api/jobs/JOBID/info/
        tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(self.job_id) +'/info/'
        try:
            #Extract tags fields
            tags = requests.post(tags_url).json()
            self.mac_tags = tags['tags']
        except:
            return None

    def generate_text_and_image(self):
        self.annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(self.job_id)
        radec_string = self.result_radec_string
        #Format tagged objects and append them to the initial RA & DEC list.
        for tag in self.mac_tags:
            print(tag)
            radec_string.append('   ○ ' + tag + '\n')

        self.solved_image_caption = "".join(radec_string)

    def send_messages(self, context, update, error=False):
        if error is True:
            context.bot.send_message(chat_id=self.chat_id, text= 'Looks like I failed to solve your image, please try again.')
        
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=self.annotated_url, caption=self.solved_image_caption)
        

    def platesolve(self, file_id, context, update):
        self.astrometry_login()
        print('Logged in', self.session_id)
        self.generate_file_url(file_id)
        print('File url is a go', self.file_url)
        self.upload()
        print('uploaded image')
        self.get_jobid()
        print('gotten a jobid', self.job_id)
        if self.check_status():
            self.send_messages(context, update, True)
            return True
        print('Status is a go')
        self.get_ra_dec_tags()
        print('radec tags are a go', self.result_radec_string)
        self.get_tags_objects()
        print('tags objects are a-okay', self.mac_tags)
        self.generate_text_and_image()
        print('text and image are good', self.solved_image_caption)
        self.send_messages(context, update)
        print('messages sent!')
        return False


    def testing(self):
        self.job_id = 4185650
        if self.check_status():
            return True
        self.get_ra_dec_tags()
        self.get_tags_objects()
        self.generate_text_and_image()
        print(self.solved_image_caption)