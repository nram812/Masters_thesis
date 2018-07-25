#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:38:18 2018

@author: neeleshrampal
"""

filename = '/Volumes/Promise1/Neelesh/MODIS_L3/2002/365/MOD08_D3.A2002365.061.2017280190741.hdf'
from pyhdf import SD

f = SD.SD(filename)
datasets = f.datasets().keys()
d1 = []
for key in datasets:
    #
    if 'Cloud_Fraction_Nadir' in key:
        d1.append(key)
# print d1
sds = f.select('Cloud_Fraction_Nadir_Day_Mean')
data = sds.get()
f.close()
dset = 'Cloud_Fraction_Nadir_Pixel_Counts'
sds = f.select(dset)
data = sds.get()
f.close()
# import pylab as py
# py.figure()
# py.imshow(data)
# py.show()
# import os


# make notes
sds = f.select('Cloud_Fraction_Nadir_Day_JHisto_vs_Pressure')
data = np.array(sds.get(), dtype=float)
c = np.where(data == sds.attributes()['_FillValue'])
data[c] = np.nan
# data=sds.get()
data1 = np.nansum(data, axis=(0, 1))
py.figure()
py.imshow(np.nansum(data, axis=0)[-8])
6:
lcf = np.nansum(data[6:], axis=(0, 1))
sds = f.select('Cloud_Fraction_Nadir_Day_Pixel_Counts')
data2 = sds.get()
lcc = lcf * 1.0 / data2 * 1.0
print sds.attributes()
""" the low cloud fraction can be calculated by summing only over all the pressure levels (680-1110) as this tells us all the cloud retrievals
at 5km that have pressures greater than 680hpa, you then use the total counts in conjunction with this. """

"""The above lines are purely for testing"""

import netCDF4 as nc4
from netCDF4 import Dataset
from pyhdf import SD

# begin by opening the dataset
f = Dataset('global_cloud_fraciton_and_counts.nc', 'w', format='NETCDF4')  # 'w' stands for write
tempgrp = f.createGroup('Cloud_data')
tempgrp.createDimension('lon', 360)
tempgrp.createDimension('lat', 180)

tempgrp.createDimension('time', None)
tempgrp.createDimension('time_date', None)

lcf = tempgrp.createVariable('Cloud_Fraction_Day_Nadir', 'f4', ('time', 'lon', 'lat'), zlib=True,
                             least_significant_digit=4, complevel=3)
cf_counts = tempgrp.createVariable('Cloud_Fraction_Day_Nadir_counts', 'f4', ('time', 'lon', 'lat'), zlib=True,
                                   least_significant_digit=4, complevel=3)
lcf_counts = tempgrp.createVariable('Low_Cloud_Day_Nadir_counts', 'f4', ('time', 'lon', 'lat'), zlib=True,
                                    least_significant_digit=4, complevel=3)
# time = tempgrp.createVariable('Time', 'f4', 'time')
time_date = tempgrp.createVariable('time_data', 'U16', 'time')

# Add global attributes
f.description = "This dataset contains data from the MODIS Terra cloud dataset. The cariables of interest are the Cloud_Fraction_NADIR_DAY_MEAN from year(day) 2000(56) to 2017 (365). Note this is not the low cloud fraction this is total cloud fraction"
f.history = "Created Wed 25th July"

# Add local attributes to variable instances
# longitude.units = 'degrees east'
# latitude.units = 'degrees north'
time.units = 'days since 55th Day of 2000'
lcf.units = 'Percentage'
lcf_counts.units = 'Counts'
f.close()

dir_1 = '/Volumes/Promise1/Neelesh/MODIS_L3/'
# temp.warning = 'This data is not low cloud fraction'
# get time in days since Jan 01,01
from datetime import datetime
import netCDF4 as nc4
from netCDF4 import Dataset
from pyhdf import SD
import os
os.chdir('/Users/neeleshrampal/OneDrive/Masters_Project/')
counter = 0
import numpy as np
import time as tm

f = nc4.Dataset('global_cloud_fraciton_and_counts.nc', 'r+', format='NETCDF4')
lcf = f['Cloud_data']['Cloud_Fraction_Day_Nadir']
time = f['Cloud_data']['time_data']
cf_counts = f['Cloud_data']['Cloud_Fraction_Day_Nadir_counts']
lcf_counts = f['Cloud_data']['Low_Cloud_Day_Nadir_counts']
"""edit make a list so you can loop through the list directories,also errors in pre processing"""
"""This is the file that is causing all the errors /Volumes/Promise1/Neelesh/MODIS_L3/2000/118/MOD08_D3.A2000118.061.2017272232121.hdf"""
start = tm.time()
for year in os.listdir(dir_1):
    if year <> '.DS_Store':
        dir2 = dir_1 + year + '/'
        for day in os.listdir(dir2):


            if day <> '.DS_Store':
                dir3 = dir2 + day + '/'
                for file in os.listdir(dir3):
                    if file <> '.DS_Store':
                        dir4 = dir3 + file

                        f2 = SD.SD(dir4)  # this is the netcdf4 file
                        sds = f2.select('Cloud_Fraction_Nadir_Day_JHisto_vs_Pressure')  # dataset is only number of count
                        data_hist = np.array(sds.get(), dtype=float)
                        c = np.where(data_hist == sds.attributes()['_FillValue'])  # get_rid_fillvalues
                        data_hist[c] = np.nan
                        lcf_c = np.nansum(data_hist[6:], axis=(0, 1))
                        lcf_counts[counter] = lcf_c  # Only sum over the low cloud pixels ([6:])
                        sds = f2.select('Cloud_Fraction_Nadir_Day_Pixel_Counts')
                        # the total number of pixel counts
                        t_cf = np.array(sds.get(), dtype=float)  # total cloud coutns
                        c = np.where(t_cf == sds.attributes()['_FillValue'])  # get_rid_fillvalues
                        t_cf[c] = np.nan
                        cf_counts[counter] = t_cf
                        lcf[counter] = lcf_c * 1.0 / t_cf * 1.0

                        sre1 = str(year) + str(day)
                        time[counter] = sre1
                        counter = counter + 1
                        print dir4


                    else:
                        print 'DSstro'


            else:
                print 'uce'


            time_rem = -(start - tm.time()) * (6400.0 - counter) / 3600.0
            print time_rem, 'hours', counter

f.close()