

def generate_tags_string(job_id):
    tag_string_lst = get_ra_dec_tags(job_id)
    mac_tags = list(get_tags_objects(job_id))
    formatted_mac_tag_string = ['   ○ ' + tag + '\n' for tag in mac_tags]
    tag_string_lst.append(formatted_mac_tag_string)
    return "".join(tag_string_lst)