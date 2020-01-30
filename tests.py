# Basic notebook importsc
import matplotlib
import pylab as plt
import numpy as np
import healpy as hp

import skymap

from skymap import Skymap,McBrydeSkymap,OrthoSkymap
from skymap import SurveySkymap,SurveyMcBryde,SurveyOrtho
from skymap import DESSkymap,BlissSkymap

SKYMAPS = [Skymap,McBrydeSkymap,OrthoSkymap]
SURVEYS = [SurveySkymap,SurveyMcBryde,SurveyOrtho]
ZOOMS   = [DESSkymap,BlissSkymap]

fig,axes = plt.subplots(1,3,figsize=(20,4))
for i,cls in enumerate(SKYMAPS):
    plt.sca(axes[i])
    smap = cls()
    plt.title(cls.__name__)

fig,axes = plt.subplots(1,3,figsize=(20,4))
for i,cls in enumerate(SKYMAPS):
    plt.sca(axes[i])
    smap = cls()
    smap.draw_milky_way()
    smap.draw_lmc()
    smap.draw_smc()
    plt.title(cls.__name__)


fig,axes = plt.subplots(1,3,figsize=(20,4))
for i,cls in enumerate(SKYMAPS):
    plt.sca(axes[i])
    smap = cls(date='2018/11/02 01:00:00')
    smap.draw_airmass(airmass=1.4,color='b')
    smap.draw_zenith(alpha=1.0,radius=2.0,color='g',)
    smap.draw_lmc()
    smap.draw_smc()


fig,axes = plt.subplots(1,3,figsize=(20,4))
for i,cls in enumerate(SURVEYS):
    plt.sca(axes[i])
    smap = cls()
    smap.draw_des(label='DES')
    smap.draw_maglites(label='MagLiteS')
    smap.draw_bliss(label='BLISS')
    plt.title('Footprints (%s)'%cls.__name__)
    plt.legend(loc='upper right')


plt.figure()
smap = DESSkymap()
smap.draw_des(label='DES')
smap.draw_maglites(label='MagLiteS')
smap.draw_bliss(label='BLISS')
plt.suptitle('DES Zoom Footprint')
plt.legend(loc='upper left',fontsize=10)