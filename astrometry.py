import requests, json

def get_file_path(file_id, bot_token):
    url_file_path = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(bot_token, file_id)
    response = requests.get(url_file_path).json()['result']['file_path']
    if response == None:
        exit
    else:
        return response

def generate_file_url(file_id, bot_token):
    file_path = get_file_path(file_id, bot_token)
    url = 'https://api.telegram.org/file/bot{}/{}'.format(bot_token, file_path)
    return url



#file_id = 'BQACAgQAAxkBAAICpV4yHHmWaz0yJKaEDHyE0bwzuX3NAALSBQACIhSRUQzmb5PAjpW_GAQ'
#bot_token = '965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s'