import requests, json, time

api_key = 'ujwqfydrabjirpjm'

#file_id = 'AgACAgQAAxkBAAIC3V4yKPk1gmQHHDrh344TEi0XswnfAAJqsTEbqwABkVGTkrOZwNPSv0EWthsABAEAAwIAA3kAA2dlAgABGAQ'
bot_token = '965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s'

sub_id = 3351945

def astrometry_login():
    login = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": api_key})}).json()
    session_id = login["session"]
    return session_id

def get_file_path(file_id, bot_token):
    url_file_path = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(bot_token, file_id)
    response = requests.get(url_file_path).json()['result']['file_path']
    if response == None:
        print('we fucked up chief')
        exit
    else:
        return response

def generate_file_url(file_id, bot_token):
    file_path = get_file_path(file_id, bot_token)
    url = 'https://api.telegram.org/file/bot{}/{}'.format(bot_token, file_path)
    print(url)
    return url

def upload(file_id, bot_token):
    global sub_id
    session_id = astrometry_login()
    file_url = generate_file_url(file_id, bot_token)
    out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": session_id, "url": file_url})}).json()
    sub_id = out["subid"]

def check_status():
    global sub_id
    try:
        status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(sub_id)
        out = requests.post(status_check_url).json()
        try:
            is_finished = out['processing_finished']
            return is_finished
        except:
            return "Yer fuked"
    except:
        return "Invalid"

def get_tags():
    global sub_id
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(sub_id) +'/machine_tags/'
    tags = requests.post(tags_url).json()
    return tags['tags']

def gnerate_annotated_url():
    global sub_id
    annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(sub_id)
    return annotated_url

def generate_tags_string():
    tag_string_lst = ['Found the following objects:\n']
    mac_tags = list(get_tags())
    for tag in mac_tags:
        tag_string_lst.append('   ○ ' + tag + '\n')
    return "".join(tag_string_lst)



#upload(photo_id, bot_token)
is_finished = check_status()
print(is_finished)
while str(is_finished) == "None":
    is_finished = check_status()

tags_string = generate_tags_string()
annotated_url = gnerate_annotated_url()

print(annotated_url, "\n", tags_string)
