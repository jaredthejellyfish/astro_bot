import requests, json, multiprocessing, time

api_key = 'ujwqfydrabjirpjm'

#file_id = 'AgACAgQAAxkBAAIC3V4yKPk1gmQHHDrh344TEi0XswnfAAJqsTEbqwABkVGTkrOZwNPSv0EWthsABAEAAwIAA3kAA2dlAgABGAQ'
#bot_token = '965873757:AAGDYWeqXydOHcg8PI-qMK_DSH8ojBJn2-s'

sub_id = 3213478

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

def upload(session_id, file_id, bot_token):
    global sub_id
    file_url = generate_file_url(file_id, bot_token)
    out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": session_id, "url": file_url})}).json()
    sub_id = out["subid"]

def get_jobid(sub_id):
    status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(sub_id)
    out = requests.post(status_check_url).json()
    job_id = out['jobs'][0]
    return job_id

def check_status(sub_id):
    is_finished = False
    status_check_url = 'http://nova.astrometry.net/api/jobs/'+ str(sub_id)
    while is_finished == False:
        #time.sleep(5)
        try:
            out = requests.post(status_check_url).json()
            finished_check = out['status']
            if finished_check == 'success':
                is_finished = True
            elif finished_check == 'failed':
                print("solve failed")
                break
            else:
                is_finished = False
        except:
            print("failed")
            break
    return is_finished

def get_tags(job_id):
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id) +'/machine_tags/'
    tags = ''
    try:
        tags = requests.post(tags_url).json()
    except:
        exit
    return tags['tags'] 

def gnerate_annotated_url(job_id):
    annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(job_id)
    return annotated_url

def generate_tags_string(job_id):
    tag_string_lst = ['Found the following objects:\n']
    mac_tags = list(get_tags(job_id))
    for tag in mac_tags:
        tag_string_lst.append('   ○ ' + tag + '\n')
    return "".join(tag_string_lst)

def platesolver_results(sub_id):
    job_id = get_jobid(sub_id)
    annotated_url = gnerate_annotated_url(job_id)
    machine_tags = generate_tags_string(job_id)
    return annotated_url, machine_tags

def astrometry_job_run(file_id, bot_token):
    global sub_id
    session_id = astrometry_login()
    upload(session_id, file_id, bot_token)
    return session_id, sub_id
