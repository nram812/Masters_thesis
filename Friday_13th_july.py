
# coding: utf-8

# In[2]:

import numpy as np
import pylab as py
import matplotlib.pyplot as plt
#data is reshaped
import numpy as np
import pylab as py
x=np.load('/Users/neeleshrampal/OneDrive/_2017/Transition/lts_and_fraction_results_series/sst_monthly_time_series.npy').reshape(180,61,111)
y=np.load('/Users/neeleshrampal/OneDrive/_2017/Physics 788/modis_cloud_fraction_final.npy')
mean_x=np.nanmean(x,axis=0)
temp_bins=range(290,305,2)
info=np.digitize(mean_x,bins=temp_bins)



# ## July 13th 2018
# First we load the relevant cloud fraction and sst datasets, the purpose of this is to investigate whether anomallies in sst, are strongly correlated to CF in different SST regions. The figure beneath illustrates the to show that the data set is consistent for both variables.
# The figures below simply ensure that the data is consistent.
# 

# In[3]:

fig,ax=plt.subplots(4,1,figsize=(10,10))
ax.shape
ax[0].imshow(x[48],vmin=294,vmax=305)
ax[1].imshow(y[49],vmin=0.0,vmax=1)
ax[2].plot(y[:,31,60],label='seasonaility of the data')
ax[3].imshow(info)
plt.show()


# ## Next Task
# * Firstly, for every point in time, we will group the data into divisions of SST.
# This wasnt entirely successful, as clear cut relationships do not emerge.

# In[157]:


info=np.digitize(mean_x,bins=temp_bins)
#print info[0]
new_sst=np.zeros([180,len(temp_bins)])
new_cf=np.zeros([180,len(temp_bins)])
for i in range(180):
    for j in range(len(temp_bins)):#number of bins
        #print j
        new_sst[i,j]=np.nanmean(x[i][np.where(info==j)])
        new_cf[i,j]=np.nanmean(y[i][np.where(info==j)])

py.figure()
py.plot(new_sst[48:,6],new_cf[48:,6],'x')
py.show()
z=[]
for i in range(len(temp_bins)):
    z.append(np.corrcoef(new_sst[48:176,i],new_cf[48:176,i])[0,1])
    
print z    
#print x[0:180,31,60]


# ## New Task
# * Here we will analyse the strength of the non local and local regions in large spatial domains.
# 

# In[10]:

temp_bins=range(290,305,2)
info=np.digitize(mean_x,bins=temp_bins)
klein_region=[range(30,51),range(80,101)]
y1=y.reshape(15,12,61,111)
season_mean=np.repeat(np.nanmean(y1,axis=0),15,axis=0).reshape(12,15,61,111,order='C').reshape(180,61,111,order='F')
x1=x.reshape(15,12,61,111)
season_meanx=np.repeat(np.nanmean(x1,axis=0),15,axis=0).reshape(12,15,61,111,order='C').reshape(180,61,111,order='F')
#seasonality of each of the variables
fig,ax=py.subplots()
ax.plot(season_meanx[:,40,80],'r',label='SST')
ax2=ax.twinx()
ax2.plot(-season_mean[:,40,80],'b',label='CLOUD fraction')
plt.legend()
fig.show()

anom_y=y-season_mean
anom_x=x-season_meanx
coor=np.zeros([61,111])
for i in range(61):
    for j in range(111):
        coor[i,j]=np.corrcoef(anom_y[48:176,i,j],anom_x[48:176,40,80])[0,1]
        #coor[i,j]=np.corrcoef(y[48:176,i,j],x[48:176,40,80])[0,1]
#klein_cf=np.nanmean(y[:,klein_region[0],klein_region[1]],axis=(1,2))
py.figure()
py.imshow(coor,vmin=-0.3,vmax=0.2,cmap='nipy_spectral')
py.show()

# additionally lets make a plot of cloud fraction and sst anomallies
fig1,ax1=py.subplots()
ax1.plot(anom_x[:,40,80],'r',label='SST')
ax3=ax1.twinx()
ax3.plot(anom_y[:,40,80],'b',label='CLOUD fraction')
#plt.legend()
fig1.show()



# In[29]:

#Fourier transfrom of SST
#choose 168 to avoid spectral leakage.

from scipy.fftpack import fft,fftfreq,fftshift
fft=fft(anom_x[48:168,40,80])
freq=fftfreq(len(x[48:168,40,80]))
fft1=fftshift(fft)
freq1=fftshift(freq)
py.figure()
py.subplot(121)
py.plot(freq1,np.log(abs(fft1)**2))
py.xlabel('Month$^{-1}$')

py.show()

from scipy.fftpack import fft,fftfreq,fftshift
fft=fft(x[48:168,40,80])
freq=fftfreq(len(x[48:168,40,80]))
fft1=fftshift(fft)
freq1=fftshift(freq)
py.subplot(122)
py.plot(freq1,np.log(abs(fft1)**2))
py.xlabel('Month$^{-1}$')

py.show()



# # Results
# Non local correlations seem unclear, there is also a lag in seasonal cycle between the two osilattions, which might be worth investigation
# ## other things that need to be investigated are:
# * How similar are the seasonailities of the variables
# * The variability of cloud fraction on large scales vs smaller scales and the grouping of different regions
# * The response of SST in stratocumulus regions remains uncertain, as the response to sst range from positive to negative, you need to read the "Change in cloud cover in a warmed cliamte"
