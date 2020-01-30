import requests, json, multiprocessing, time

api_key = 'ujwqfydrabjirpjm'

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
    out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": session_id, "url": file_url,"publicly_visible":"n"})}).json()
    sub_id = out["subid"]

def get_jobid(sub_id):
    no_jobid = True
    while no_jobid == True:
        time.sleep(2)
        try:
            status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(sub_id)
            out = requests.post(status_check_url).json()
            job_id = out['jobs'][0]
            if job_id:
                no_jobid = False
            else:
                no_jobid = True
        except:
            no_jobid = True
    return job_id

def check_status(sub_id):
    job_id = get_jobid(sub_id)
    is_finished = False
    status_check_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id)
    while is_finished == False:
        time.sleep(1)
        try:
            out = requests.post(status_check_url).json()
            finished_check = out['status']
            if finished_check == 'success':
                is_finished = True
            elif finished_check == 'failure':
                print("solve failed")
                return "failed"
            else:
                is_finished = False
                break
        except:
            print("failed")
            break
    return is_finished

def get_ra_dec_tags(job_id):
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id) +'/info/'
    try:
        radec = requests.post(tags_url).json()
        ra = radec['calibration']['ra']
        dec = radec['calibration']['dec']
        result_radec_string = ["The center of the image is at:\n ○ RA:  {}\n ○ DEC:  {}\n".format(ra, dec),'\n' , 'Found the following objects:\n']
        return result_radec_string
    except:
        pass 
    
def get_tags_objects(job_id):
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id) +'/info/'
    try:
        tags = requests.post(tags_url).json()
        return tags['tags']
    except:
        exit
      
def gnerate_annotated_url(job_id):
    annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(job_id)
    return annotated_url

def generate_tags_string(job_id):
    tag_string_lst = get_ra_dec_tags(job_id)
    mac_tags = list(get_tags_objects(job_id))
    for tag in mac_tags:
        tag_string_lst.append('   ○ ' + tag + '\n')
    return "".join(tag_string_lst)

def platesolver_results(sub_id):
    while check_status(sub_id) == False and check_status(sub_id) != 'failure':
        time.sleep(1)
        print("Solving image with submission id:", sub_id)

    job_id = get_jobid(sub_id)
    annotated_url = gnerate_annotated_url(job_id)
    machine_tags = generate_tags_string(job_id)
    return annotated_url, machine_tags

def astrometry_job_run(file_id, bot_token):
    global sub_id
    session_id = astrometry_login()
    upload(session_id, file_id, bot_token)
    return session_id, sub_id