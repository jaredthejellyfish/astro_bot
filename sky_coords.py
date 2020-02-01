from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord as sc
import astropy.coordinates as coord
from urllib.parse import urlencode
from urllib.request import urlretrieve

def get_SDDS_image(coords_list):
    hcg7_center = sc(42.0000*u.deg, 47.1953*u.deg, frame='icrs')
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

def find_object_coords_fname(object_name):
    result_table = Simbad.query_object(object_name)
    try:
        obj_ra = result_table['RA'][0].replace(" ", ":")
        obj_dec = result_table['DEC'][0].replace(" ", ":")
        object_at_string = "Object <b>{}</b> is at:\n○ RA:  {} \n○ DEC:  {}".format(object_name, obj_ra, obj_dec)
        return object_at_string
    except:
        return "Object could not be found."

get_SDDS_image(1)