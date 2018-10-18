#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:38:18 2018

@author: neeleshrampal
"""
"""Edits have been made to incorparate a cloud fraction vs hISTROGRAM product"""

"""One must note that the product is likely to be conservative for cumulus cloud regions, due to its determination of partly cloudy reubis"""
filename = '/Volumes/Promise1/Neelesh/MODIS_L3/2002/365/MOD08_D3.A2002365.061.2017280190741.hdf'
from pyhdf import SD

f = SD.SD(filename)
datasets = f.datasets().keys()
d1 = []
for key in datasets:
    #
    if 'Histo_vs_Pressure' in key:
        d1.append(key)
# print d1
"""the goal for today is to ensure that you can obtain the mean cloud fraction from grouping the data"""
sds = f.select('Cloud_Fraction_Nadir_Day_Mean')
data = sds.get()/1e4
c=np.where(data<0.0)
data[c]=np.nan
#f.close()
dset = 'Cloud_Fraction_Nadir_Day_Pixel_Counts'
sds = f.select(dset)
data4 = np.array(sds.get(),dtype=float)

# import pylab as py
fig=py.figure()
py.imshow(data4,vmin=0,vmax=1000)
fig.show()
# import os


# make notes
sds = f.select('Total_Totals_Histogram_Counts')
sds=f.select('Cloud_Optical_Thickness_ISCCP_JHisto_vs_Pressure')


sds=f.select('Cloud_Fraction_Nadir_Day_JHisto_vs_Pressure')
dsw=sds.get()*1.0
c=np.where(dsw==-9999.0)
dsw[c]=np.nan
data2=np.array(sds.get()*1.0, dtype=float)re(data2== sds.attributes()['_FillValue'])
sds=f.select('Cloud_Top_Pressure_Nadir_Day_Histogram_Counts')
data1 = np.array(sds.get()*1.0, dtype=float)
c=np.where(data4==-9999.0)
#lets see if we can estimate the cloud fraction
#np.nan

data12=np.nansum(data1[:,:],axis=(0))
data12[c]=np.nan
# data=sds.get()
#data1 = np.nansum(data, axis=(0, 1))
# py.figure()
# py.imshow(np.nansum(data, axis=0)[-8])
# 6:
# lcf = np.nansum(data[6:], axis=(0, 1))
sds = f.select('Cloud_Fraction_Nadir_Day_Pixel_Counts')

data2 = sds.get()
lcc = np.nansum(dsw,axis=(0,1))* 1.0 / data4 * 1.0

fig,ax2=py.subplots()

#ax.imshow(lcc)
ax2.imshow(lcc,vmin=0,vmax=1)
fig.show()
print sds.attributes()
""" the low cloud fraction can be calculated by summing only over all the pressure levels (680-1110) as this tells us all the cloud retrievals
at 5km that have pressures greater than 680hpa, you then use the total counts in conjunction with this. """

"""The above lines are purely for testing"""

import netCDF4 as nc4
from netCDF4 import Dataset
from pyhdf import SD
import os
os.chdir('/Users/neeleshrampal/OneDrive/Masters_Project/')
# begin by opening the dataset
f = Dataset('Joint_Histogram data_Terra.nc', 'w', format='NETCDF4')  # 'w' stands for write
tempgrp = f.createGroup('Cloud_data_ter')
tempgrp.createDimension('lon', 360)
tempgrp.createDimension('lat', 180)
tempgrp.createDimension('p_bins', 7)
tempgrp.createDimension('o_bins', 8)
tempgrp.createDimension('time', None)
tempgrp.createDimension('time_date', None)

lcf = tempgrp.createVariable('Cloud_Optical_Thickness_ISCCP_JHisto_vs_Pressure', 'f4', ('time','p_bins','o_bins','lat', 'lon'), zlib=True,
                             least_significant_digit=4, complevel=3)


# time = tempgrp.createVariable('Time', 'f4', 'time')
time_date = tempgrp.createVariable('time_data', 'U16', 'time')

# Add global attributes
f.description = "This dataset contains data from the MODIS Terra cloud dataset. The cariables of interest are the Cloud_Fraction_NADIR_DAY_MEAN from year(day) 2000(56) to 2017 (365). Note this is not the low cloud fraction this is total cloud fraction"
f.history = "Created Thursday 18th October"

# Add local attributes to variable instances
# longitude.units = 'degrees east'
# latitude.units = 'degrees north'
time_date.units = 'days since 55th Day of 2000'
lcf.units = 'Counts'

f.close()

dir_1 = '/Volumes/Promise1/Neelesh/MODIS_L3/'
#dir_1 = '/Volumes/Promise1/Neelesh/Aqua2000/'
# temp.warning = 'This data is not low cloud fraction'
# get time in days since Jan 01,01
from datetime import datetime
import netCDF4 as nc4
from netCDF4 import Dataset
from pyhdf import SD

counter = 0
import numpy as np
import time as tm

f = nc4.Dataset('Joint_Histogram data_Terra.nc', 'r+', format='NETCDF4')
lcf = f['Cloud_data_ter']['Cloud_Optical_Thickness_ISCCP_JHisto_vs_Pressure']
time = f['Cloud_data_ter']['time_data']

"""edit make a list so you can loop through the list directories,also errors in pre processing"""
"""This is the file that is causing all the errors /Volumes/Promise1/Neelesh/MODIS_L3/2000/118/MOD08_D3.A2000118.061.2017272232121.hdf"""

xc=[]
for year in os.listdir(dir_1):
    if year <> '.DS_Store':
        dir2 = dir_1 + year + '/'
        for day in os.listdir(dir2):
            start = tm.time()

            if day <> '.DS_Store':
                dir3 = dir2 + day + '/'
                for file in os.listdir(dir3):
                    if file <> '.DS_Store':
                        dir4 = dir3 + file
                        try:
                            f2 = SD.SD(dir4)  # this is the netcdf4 file
                            sds = f2.select('Cloud_Optical_Thickness_ISCCP_JHisto_vs_Pressure')  # dataset is only number of count
                            data_hist = np.array(sds.get(), dtype=float)
                            c = np.where(data_hist == sds.attributes()['_FillValue'])  # get_rid_fillvalues
                            data_hist[c] = np.nan
                            lcf[counter]=data_hist[:]

                            sre1 = str(year) + str(day)
                            time[counter] = sre1
                            counter = counter + 1
                            print dir4
                        except:
                            xc.append(dir4)

                            lcf[counter] = np.nan*np.zeros([7,8,180,360])

                            sre1 = str(year) + str(day)
                            time[counter] = sre1
                            counter = counter + 1

                    else:
                        print 'DSstro'


            else:
                print 'uce'


            time_rem = -(start - tm.time()) * (6400.0 - counter) / 3600.0
            print time_rem, 'hours', counter

f.close()
np.save('chur_xc_files_failed_ter',xc)