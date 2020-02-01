from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord 
import astropy.coordinates as coord
from urllib.parse import urlencode
from urllib.request import urlretrieve

def get_SDDS_image(coords_deg_lst):
    ra = float(coords_deg_lst[0])
    dec = float(coords_deg_lst[1])
    hcg7_center = SkyCoord(ra*u.deg, dec*u.deg, frame='icrs')
    type(hcg7_center.ra), type(hcg7_center.dec)
    impix = 1080
    imsize = 2*u.deg
    cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx'
    query_string = urlencode(dict(ra=hcg7_center.ra.deg, 
                                     dec=hcg7_center.dec.deg, 
                                     width=impix, height=impix, 
                                     scale=imsize.to(u.arcsec).value/impix))
    url = cutoutbaseurl + '?' + query_string
    # this downloads the image to your disk
    urlretrieve(url, 'SDSS_cutout.jpg')

def convert_to_deg(obj_ra, obj_dec):
    coords_deg = SkyCoord(str(obj_ra + " " + obj_dec), unit=(u.hourangle, u.deg))
    coords_deg_ra = round(coords_deg.ra.degree, 4)
    coords_deg_dec = round(coords_deg.dec.degree, 4)
    str_list = [str(coords_deg_ra), str(coords_deg_dec)]
    return str_list

def find_object_coords_fname(object_name):
    result_table = Simbad.query_object(object_name)
    try:
        obj_ra = result_table['RA'][0].replace(" ", ":")
        obj_dec = result_table['DEC'][0].replace(" ", ":")
        coords = ' '.join(convert_to_deg(obj_ra, obj_dec))
        get_SDDS_image(convert_to_deg(obj_ra, obj_dec))
        constellation = coord.get_constellation(SkyCoord(coords, frame='icrs', unit=(u.deg)))
        object_at_string = "Object <b>{}</b> is at:\n○ RA:  {} \n○ DEC:  {} \n \nIn the constellation of <b>{}</b>.".format(object_name, obj_ra, obj_dec, constellation)
        return True, object_at_string
    except:
        return False, "Object could not be found."

def show_SDSS_fcoords(obj_coords_lst):
    try:
        obj_ra = obj_coords_lst[0]
        obj_dec = obj_coords_lst[1]
        coords = ' '.join(convert_to_deg(obj_ra, obj_dec))
        get_SDDS_image(convert_to_deg(obj_ra, obj_dec))
        constellation = coord.get_constellation(SkyCoord(coords, frame='icrs', unit=(u.deg)))
        object_string = "Showing <b>DSS</b> image for:\n○ RA:  {} \n○ DEC:  {} \n \nIn the constellation of <b>{}</b>.".format(obj_ra, obj_dec, constellation)
        return True, object_string
    except:
        print("abc")
        return False, "Coordinates could not be found."

    