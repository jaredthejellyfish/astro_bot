# -----------------------------------------------------------
# Generates a continuation to prior APT plan from FIT file
#
# (C) 2020 Gerard Almenara, Barcelona, Spain
# Released under GNU Public License (GPL)
# email jarredthejellyfish@gmail.com
# -----------------------------------------------------------

from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
from lxml import etree
import numpy as np
import re, argparse


xml_template = """
<?xml version="1.0"?>
	<CCDPlans>
	<CCDLightPlans>
		<Plan>
			<Name>%(plan_name)s</Name>
			<DontDither>%(dither)s</DontDither>
			<Vertical>0</Vertical>
			<Exposures>
				<Order>1</Order>
				<Exp>0</Exp>
				<Bin>%(bnn)s</Bin>
				<Pause>1</Pause>
				<Count>1</Count>
				<RunCommand>#CCDCool A %(temp)s</RunCommand>
				<WaitCommand>0</WaitCommand>
				<Filter>-1</Filter>
				<FrameType>-1</FrameType>
			</Exposures>
			<Exposures>
				<Order>2</Order>
				<Exp>0</Exp>
				<Bin>%(bnn)s</Bin>
				<Pause>1</Pause>
				<Count>1</Count>
				<RunCommand>#GoTo++ 20 Blind %(coords)s</RunCommand>
				<WaitCommand>0</WaitCommand>
				<Filter>-1</Filter>
				<FrameType>-1</FrameType>
			</Exposures>
			<Exposures>
				<Order>3</Order>
				<Exp>0</Exp>
				<Bin>%(bnn)s</Bin>
				<Pause>1</Pause>
				<Count>1</Count>
				<RunCommand>#CCDGain %(gain)s</RunCommand>
				<WaitCommand>0</WaitCommand>
				<Filter>-1</Filter>
				<FrameType>-1</FrameType>
			</Exposures>
			<Exposures>
				<Order>4</Order>
				<Exp>%(exposure)s</Exp>
				<Bin>%(bnn)s/Bin>
				<Pause>%(pause)s</Pause>
				<Count>%(count)s</Count>
				<RunCommand></RunCommand>
				<WaitCommand>0</WaitCommand>
				<Filter>-1</Filter>
				<FrameType>-1</FrameType>
			</Exposures>
		</Plan>
	</CCDLightPlans>
	</CCDPlans>
"""

parser = argparse.ArgumentParser()

parser.add_argument("-c", help="Image count (default is 10)")
parser.add_argument("-n", help="Plan name")
parser.add_argument("-d", help="Dithering (y/n)")
parser.add_argument("-f", help="File name")
parser.add_argument("-p", help="Pause")

args = parser.parse_args()

if args.c:
    count = str(args.c)
else:
    count = "10"
if args.n:
    name = args.n
else:
    name = "ASI 294MC Pro Cool (Lights)"
if args.d:
    if args.d == "y":
        dither = "-1"
    if args.d == "n":
        dither = "1"
else:
    dither = "-1"
if args.f:
    f_name = args.f
else:
    f_name = "test.fit"
if args.p:
    pause = str(args.p)
else:
    pause = "5"

def xml_file_generation_writing(plan_file, xml):
    plan_file = open("APT_PlanExport.xml", "w+")
    plan_file.write(xml)
    plan_file.close()

def get_fits_coords(f_name):
    #Open FITs file
    hdul = fits.open(f_name)
    #Extract Rigth Ascention and Declination
    obj_ra = hdul[0].header['OBJCTRA']
    obj_dec = hdul[0].header['OBJCTDEC']
    #Close FITs file
    hdul.close()
    return obj_ra + " " + obj_dec

def get_convert_coords(f_name):
    inp = get_fits_coords(f_name)
    #Input splitting
    inp_list = re.split(r'[:,\s]\s*', inp)
    #Input formatting
    coords_ra = inp_list[0] + "d" + inp_list[1] + "m" + inp_list[2] + "s"
    coords_dec = inp_list[-3] + "d" + inp_list[-2] + "m" + inp_list[-1] + "s"
    #Coordinate conversion
    coords_dirty = SkyCoord(coords_ra, coords_dec)
    #Coordinate cleaning
    coords_lst = str(coords_dirty).split("(")
    coords_clean = coords_lst[-1].replace(")>", "")
    return coords_clean.replace(",", "")

def get_fits_arguments(f_name):
    hdul = fits.open(f_name)
    gain = str(hdul[0].header['GAIN'])
    exposure = str(hdul[0].header["EXPTIME"])
    temp = str(hdul[0].header['SET-TEMP'])
    binning = str(hdul[0].header['XBINNING']) + "x" + str(hdul[0].header['YBINNING'])
    hdul.close()
    return temp, gain, exposure, binning

def generate_plan_data(count, name, dither, f_name, pause):
    coords = get_convert_coords(f_name)
    setting_list = get_fits_arguments(f_name)
    data = {"plan_name":name, "dither":dither, "temp":setting_list[0], "coords":coords, "gain":setting_list[1], "exposure":setting_list[2], "bnn":setting_list[3], "count":count, "pause":pause}
    xml = xml_template%data
    return xml


xml = generate_plan_data(count, name, dither, f_name, pause)

xml_file_generation_writing(f_name, xml)