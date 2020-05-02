import requests, json, time

#Astrometry API key
api_key = 'ujwqfydrabjirpjm'

#Log into nova.astrometry.net
def astrometry_login():
    #Generate json formatted url with API key
    login = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": api_key})}).json()
    session_id = login["session"]
    return session_id

#Get the file path from the telegram server to generate the uploadable url
def get_file_path(file_id, bot_token):
    #Generate url based on bot key and file ID
    url_file_path = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(bot_token, file_id)
    file_path = requests.get(url_file_path).json()['result']['file_path']
    #Test if request got an appropriate response
    if file_path == None:
        exit
    else:
        return file_path

#Generate the file url to upload to nova.astrometry.net
def generate_file_url(file_id, bot_token):
    file_path = get_file_path(file_id, bot_token)
    url = 'https://api.telegram.org/file/bot{}/{}'.format(bot_token, file_path)
    return url

#Upload file from file_url to nova.astrometry.net and assign sub_id to global variable.
def upload(session_id, file_id, bot_token):
    global sub_id
    file_url = generate_file_url(file_id, bot_token)
    out = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": session_id, "url": file_url,"publicly_visible":"n"})}).json()
    sub_id = out["subid"]

#Get job_id from nova.astrometry.net/api/submissions request.
def get_jobid(sub_id):
    #Loops until a request with a job_id value is received
    while True:
        time.sleep(2)
        try:
            #Requests the submission info json from nova.astrometry.net/api/submissions
            status_check_url = 'http://nova.astrometry.net/api/submissions/'+ str(sub_id)
            submissions_request = requests.post(status_check_url).json()
            #Extracts job_id from json
            job_id = submissions_request['jobs'][0]
            if job_id:
                break
        except:
            pass
    return job_id

#Check if image has been solved or it has failed to solve.
def check_status(sub_id):
    job_id = get_jobid(sub_id)
    #Get nova.astrometry.net/api/jobs/ JSON query
    status_check_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id)
    while True:
        time.sleep(1)
        try:
            out = requests.post(status_check_url).json()
            #Save the status field into a variable
            finished_check = out['status']
            #Check if status is success or failure and return things accordingly
            if finished_check == 'success':
                return True
            elif finished_check == 'failure':
                return "failed"
            else:
                break
        except:
            break
    
#Extract RA & DEC tags from nova.astrometry.net/api/jobs/JOBID/info/ query
def get_ra_dec_tags(job_id):
    #Query nova.astrometry.net/api/jobs/JOBID/info/
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id) +'/info/'
    try:
        #Extract RA & DEC fields
        radec = requests.post(tags_url).json()
        ra = radec['calibration']['ra']
        dec = radec['calibration']['dec']
        #Format RA & DEC into a string.
        result_radec_string = ["The center of the image is at:\n ○ RA:  {}\n ○ DEC:  {}\n".format(ra, dec),'\n' , 'Found the following objects:\n']
        return result_radec_string
    except:
        pass 

#Extract object tags from nova.astrometry.net/api/jobs/JOBID/info/ query   
def get_tags_objects(job_id):
    #Query nova.astrometry.net/api/jobs/JOBID/info/
    tags_url = 'http://nova.astrometry.net/api/jobs/'+ str(job_id) +'/info/'
    try:
        #Extract tags fields
        tags = requests.post(tags_url).json()
        return tags['tags']
    except:
        exit

#Generate annotated file url from nova.astrometry.net/annotated_display/     
def gnerate_annotated_url(job_id):
    annotated_url = 'http://nova.astrometry.net/annotated_display/' + str(job_id)
    return annotated_url

#Format extracted tags into a string.
def generate_tags_string(job_id):
    #Get the RA & DEC string as a value on a list.
    tag_string_lst = get_ra_dec_tags(job_id)
    #Put the tagged objects into a list object.
    mac_tags = list(get_tags_objects(job_id))
    #Format tagged objects and append them to the initial RA & DEC list.
    for tag in mac_tags:
        tag_string_lst.append('   ○ ' + tag + '\n')
    return "".join(tag_string_lst)

#Check for platesolver status and return results
def platesolver_results(sub_id):
    #Loop over the check status to halt the program until it solves
    while check_status(sub_id) != True and check_status(sub_id) != 'failure':
        time.sleep(1)
    #Get job_id
    job_id = get_jobid(sub_id)
    #Grab annotated file url
    annotated_url = gnerate_annotated_url(job_id)
    #Grab RA, DEC, and machine tag string.
    machine_tags = generate_tags_string(job_id)
    return annotated_url, machine_tags

#Log into astrometry, upload image file and return session_id and sub_id strings.
def astrometry_job_run(file_id, bot_token):
    global sub_id
    session_id = astrometry_login()
    upload(session_id, file_id, bot_token)
    return session_id, sub_id