import requests
import os

class Soho:
    def get_gif(self, chat_id='test_soho_image'):
        uri = 'https://sohowww.nascom.nasa.gov/data/LATEST/current_c2small.mp4'
        try:
            with open('soho_{}.mp4'.format(chat_id), 'wb') as f:
                        f.write(requests.get(uri).content)
        except:
            return True

    def cleanup(self, chat_id='test_soho_image'):
        try:
            # Clean directory after use of the image
            os.remove('soho_{}.mp4'.format(chat_id))
        except:
            pass