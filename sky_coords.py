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

def find_coords_system(object_coords_lst):
    if object_coords_lst[0].find(" ") > 0:
        print('+aa bb cc.ddd, +aa bb cc.ddd')
    elif object_coords_lst[0].find(":") > 0 and len(object_coords_lst) == 2:
        print('+aa:bb:cc.ddd, +aa:bb:cc.ddd')
    elif len(object_coords_lst) == 2 and object_coords_lst[0].find(" ") < 0:
        print('123.321, 345.543')





