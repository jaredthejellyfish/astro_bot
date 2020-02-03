#Object catalog
from astroquery.simbad import Simbad

#Coordinates and astornomical units
from astropy import units as u
from astropy.coordinates import SkyCoord 
import astropy.coordinates as coord

#Url stuff
from urllib.parse import urlencode
from urllib.request import urlretrieve

#Download SDSS image from coordinates
def get_SDDS_image(coords_deg_lst):
    #Turn RA & DEC strings into floats.
    ra = float(coords_deg_lst[0])
    dec = float(coords_deg_lst[1])
    #Calculate the center of the file to be retrieved.
    hcg7_center = SkyCoord(ra*u.deg, dec*u.deg, frame='icrs')
    type(hcg7_center.ra), type(hcg7_center.dec)
    #Size in pixels of image to be downloaded.
    impix_w = 1657
    impix_h = 1129
    #Frame width in degrees.
    imsize = 1.2*u.deg
    #Base url to queery for SDSS cutouts
    cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx'
    #Queery to concatenate to base url
    query_string = urlencode(dict(ra=hcg7_center.ra.deg, 
                                     dec=hcg7_center.dec.deg, 
                                     width=impix_w, height=impix_h, 
                                     scale=imsize.to(u.arcsec).value/impix_w))
    #
    url = cutoutbaseurl + '?' + query_string
    #Download .jpg file
    urlretrieve(url, 'SDSS_cutout.jpg')

#Convert 'hh:mm:ss hh:mm:ss' coords to deg
def convert_to_deg(obj_ra, obj_dec):
    #Generate skycoord object with RA & DEC
    coords_deg = SkyCoord(str(obj_ra + " " + obj_dec), unit=(u.hourangle, u.deg))
    #Extract RA & DEC from skycoord obj
    coords_deg_ra = round(coords_deg.ra.degree, 4)
    coords_deg_dec = round(coords_deg.dec.degree, 4)
    #Generate string with RA & DEC
    str_list = [str(coords_deg_ra), str(coords_deg_dec)]
    return str_list

#Find object coordinates from "nickname" input.
def find_object_coords_fname(object_name):
    #Query Simbad for the object.
    result_table = Simbad.query_object(object_name)
    try:
        #Extract RA & DEC
        obj_ra = result_table['RA'][0].replace(" ", ":")
        obj_dec = result_table['DEC'][0].replace(" ", ":")
        #Generate coords string
        coords = ' '.join(convert_to_deg(obj_ra, obj_dec))
        #Get image for coords
        get_SDDS_image(convert_to_deg(obj_ra, obj_dec))
        #Get constellation for coords
        constellation = coord.get_constellation(SkyCoord(coords, frame='icrs', unit=(u.deg)))
        #Generate string with RA, DEC, and constellation
        object_at_string = "Object <b>{}</b> is at:\n○ RA:  {} \n○ DEC:  {} \n \nIn the constellation of <b>{}</b>.".format(object_name, obj_ra, obj_dec, constellation)
        return True, object_at_string
    except:
        return False, "Object could not be found."

#Show SDSS cutout from coordinate input
def show_SDSS_fcoords(obj_coords_lst):
    try:
        #Get object RA & DEC
        obj_ra = obj_coords_lst[0]
        obj_dec = obj_coords_lst[1]
        #Get coords string
        coords = ' '.join(convert_to_deg(obj_ra, obj_dec))
        #Get SDSS cutout 
        get_SDDS_image(convert_to_deg(obj_ra, obj_dec))
        #Get constellaiton
        constellation = coord.get_constellation(SkyCoord(coords, frame='icrs', unit=(u.deg)))
        #Generate result string.
        object_string = "Showing <b>DSS</b> image for:\n○ RA:  {} \n○ DEC:  {} \n \nIn the constellation of <b>{}</b>.".format(obj_ra, obj_dec, constellation)
        return True, object_string
    except:
        return False, "Coordinates could not be found."    