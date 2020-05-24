import requests
import os
class AllSky:
    def get_jpg(self, chat_id='test_ask_img'):
        uri = 'http://allsky.local/img.jpg'
        try:
            with open('allsky_{}.jpg'.format(chat_id), 'wb') as f:
                        f.write(requests.get(uri).content)
        except:
            return True

    def cleanup(self, chat_id):
        os.remove('allsky_{}.jpg'.format(chat_id))