from astroquery.simbad import Simbad

def find_object_fname(object_name):
    result_table = Simbad.query_object(object_name)
    try:
        obj_ra = result_table['RA'][0].replace(" ", ":")
        obj_dec = result_table['DEC'][0].replace(" ", ":")
        object_at_string = "Object <b>{}</b> is at:\n○ RA:  {} \n○ DEC:  {}".format(object_name, obj_ra, obj_dec)
        return object_at_string
    except:
        return "Object could not be found."

