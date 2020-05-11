import requests

class Soho:
    def __init__(self):
        pass

    def get_soho(self, chat_id='test_soho_image'):
        uri = 'https://sohowww.nascom.nasa.gov/data/LATEST/current_c2.gif'
        try:
            with open('soho_{}.gif'.format(chat_id), 'wb') as f:
                        f.write(requests.get(uri).content)
        except:
            return True


soho = Soho()
soho.get_soho()