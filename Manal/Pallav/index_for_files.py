#This file deals with light vs darkness in flies
from __future__ import print_function
import scipy.io as spio
import scipy.interpolate as spin
from scipy.linalg import norm
from numpy import *
from scipy.spatial.distance import cdist
import sys
import os
import cPickle as pickle
import pandas as pd
import pylab
import matplotlib.pyplot as plt


# In[7]:

def index(x_pos,y_pos): # latest index
    x_nor=x_pos-x_pos[0]
    y_nor=y_pos-y_pos[0]

    d=cumsum(sqrt(gradient(x_nor)**2+gradient(y_nor)**2))
    r=sqrt(x_nor**2+y_nor**2);

    #velocity calculation

    vx=gradient(x_nor)
    vy=gradient(y_nor)
    v=sqrt(vx**2+vy**2)
    cuts= (v>0.0) & (r>20.0)
    ind=r/d 
    ind[~cuts]=1
    indx=average(1-ind)
    if max(r)<50:
        return(0)
    return indx
    

def staytime(x_pos,y_pos): #Incomplete
    x_nor=x_pos-x_pos[0]
    y_nor=y_pos-y_pos[0]

    d=cumsum(sqrt(gradient(x_nor)**2+gradient(y_nor)**2))
    r=sqrt(x_nor**2+y_nor**2)
    
    #Calculating the nhoodtime/stop time
    points=dstack((x_pos,y_pos))[0]
    M=cdist(points,points)
    
    nmask=ones(x_pos.size,dtype=bool)

    i=0
    
    while(i<x_pos.size):
        bg=i
        end=min(x_pos.size,i+15)
        if max(M[i,i:end])<10:
            nmask[i:end]=False
            i=end+1
        else:
            i=i+1
# Different cuts
#    cuts= (v>0.1) & (d>5.0)
    

    stoptime=(x_pos.size)-(x_pos[cuts]).size   
    staytime=x_pos.size
    if len(where(r>20)[0])>0:
        staytime=min(where(r>20)[0])
    


# In[8]:

#for wild type
rlist=[]
indexlist={}
timelist=[]
filenamelist=[]
dt=1/50
count=0
mode='darkness'
#['6','12','11','14','15'],['1','5','9','10']
for dirname,dirnames,filenames in os.walk("/home1/dilawars/_DATA/Manal/25.06.2016_0.5M/"):
    for filename in filenames:
        if 'mat' != filename.split('.')[-1]:
            continue
        filenamelist.append(filename)
        data=spio.loadmat(os.path.join(dirname, filename))
        timestamps=ndarray.flatten(data['timestamps'])
    
        for key in data.keys():
            if key not in ['__globals__','__version__','__header__']:
                exec(key+"=ndarray.flatten(data['"+key+"'])")

        #smoothing
        times=timestamps[0:x_pos.size]
        splx=spin.UnivariateSpline(times,x_pos,s=20)
        sply=spin.UnivariateSpline(times,y_pos,s=20)
        x_smooth=splx(times)
        y_smooth=sply(times)
        
        x_pos,y_pos=x_smooth,y_smooth
        x_nor=x_pos-x_pos[0]
        y_nor=y_pos-y_pos[0]
        
        r=sqrt(x_nor**2+y_nor**2)

    
    #x_smooth=splx(times)
    #y_smooth=sply(times)

   


        timelist.append(x_pos.size)

        dt=1/30.0
    #    print("%s %0.3f %d %d"%(filename,index,stoptime*dt,staytime*dt),end='\n')
        rlist.append(average(r))
        indx=index(x_pos,y_pos)
        indexlist[filename]=indx
        print(filename,average(r),indx,end='\n')
        
        
        plt.plot(x_pos, y_pos, 'r-')
        
        # location of dots
        plt.xlim([0,480]) #[200,1100] for Tachykinin
        plt.ylim([0,480])  #[75,1000] for Tachykinin
        plt.axes().set_aspect('equal')
        plt.plot(x_pos[0],y_pos[0],'ko',ms=15, mfc='none', mew=1)   
        
   
        plt.savefig("./"+ filename.split(".")[0]+'.png')
        plt.close()
        plt.show()


# In[9]:

idxs=array([round(indexlist[keys],2) for keys in indexlist.keys()])
idxs[idxs>0]


# In[10]:

#Plot of the r/d index for Control and Test

rlist1=rlist_low
rlist2=rlist_high

rlist1[:]=[1-x for x in rlist1]
rlist2[:]=[1-x for x in rlist2]

timelist1=timelist_low
timelist2=timelist_high

filename1=filename_low
filename2=filename_high

from scipy.stats import mannwhitneyu

import matplotlib.pyplot as plt
#plt.figure()
plt.xlim((0.8,1.4))
plt.plot(len(rlist1)*[1],rlist1,"ro")
plt.plot([1],average(rlist1),"rx")
plt.plot(len(rlist2)*[1.2],rlist2,"go")
plt.plot([1.2],average(rlist2),"gx")
sv=mannwhitneyu(rlist1,rlist2)
plt.annotate(map(lambda x:'%f' % x,sv),(1.1,0.3))
plt.xticks([])
plt.show()


# In[ ]:

#Plot of t vs index in a 2d plot
plt.xlim(0,4000)
plt.ylim(0,1.0)
plt.plot(timelist1,rlist1,"ro", ms = 8, mec = 'red') #markersize and markeredgecolor
plt.plot(timelist2,rlist2,"go", ms = 8, mec = 'green')

plt.show()


# In[ ]:

#Box plots of the data

plt.xlim(0.5,4.0)
plt.ylim(0,1.0)

data=[rlist2,rlist1]
#plt.boxplot(data)

bp = plt.boxplot(data, widths=0.5)
plt.setp(bp['boxes'], color='black') 
#for i in range(2):
y = data[0]
x = numpy.random.normal(1+0, 0.04, size=len(y))
plt.plot(x, y, 'g.', alpha=0.4, ms=11)

y = data[1]
x = numpy.random.normal(1+1, 0.04, size=len(y))
plt.plot(x, y, 'r.', alpha=0.4, ms=11)

plt.show( )


# In[ ]:

d


# In[ ]:

ind[d==0]=1.0


# In[ ]:

ind[~cuts]


# In[ ]:

ind[where(cuts)]


# In[ ]:

indexlist


# In[ ]:

#For individual files

from scipy.signal import argrelextrema
import matplotlib.pyplot as plt


fname='/home1/dilawars/_DATA/Manal/25.06.2016_0.5M/CS_2016-06-25-145601-0000.mat'

data=spio.loadmat(fname)

        #data=spi.loadmat("/media/pallab/My Passport/with dot experiment/Light Light Light/data"+str(i)+"/n1")
timestamps=ndarray.flatten(data['timestamps'])

for key in data.keys():
    if key not in ['__globals__','__version__','__header__']:
        exec(key+"=ndarray.flatten(data['"+key+"'])")

times=timestamps[0:x_pos.size]

splx=spin.UnivariateSpline(times,x_pos,s=4000)
sply=spin.UnivariateSpline(times,y_pos,s=4000)

x_smooth=splx(times)
y_smooth=sply(times)

time_extrema=argrelextrema(x_smooth, greater)[0]
len(time_extrema)


ax=plt.gca()
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_aspect('equal')
#ax.polar('True')

plt.xlim([200,1100]) #[200,1100] for Tachykinin
plt.ylim([100,1000])  #[75,1000] for Tachykinin
#theta=linspace(0,2*pi,1000)
#x0,y0,r=250,225,220

#xc=x0+r*cos(theta)
#yc=y0+r*sin(theta)
#plt.plot(xc,yc),
#plt.plot(gradient(x_smooth),'g-')
plt.plot(x_pos, y_pos, 'r-')
plt.show()


# In[ ]:

import numpy
numpy.var(rlist2)


# In[ ]:

# Independent two-tailed t-test, unequal variances
from scipy import stats
stats.ttest_ind(rlist1, rlist2, equal_var = False)


# In[ ]:

times=timestamps[0:x_pos.size]

splx=spin.UnivariateSpline(times,x_pos,s=4000)
sply=spin.UnivariateSpline(times,y_pos,s=4000)
x_smooth=splx(times)
y_smooth=sply(times)


x_nor=x_smooth-x_smooth[0]
y_nor=y_smooth-y_smooth[0]


d=cumsum(sqrt(gradient(x_nor)**2+gradient(y_nor)**2))
r=sqrt(x_nor**2+y_nor**2);


# In[ ]:

x_nor=x_pos-x_pos[0]
y_nor=y_pos-y_pos[0]

x_shift,y_shift = roll(x_nor,1), roll(y_nor,-1)

d=cumsum(sqrt((x_shift-x_nor)**2+(y_shift-y_nor)**2))
r=sqrt(x_nor**2+y_nor**2)


# In[ ]:

for fname,i,r in zip(filename_darkness,indexlist_darkness,rlist_darkness):
    print("%s %0.2f %0.2f"%(fname,i,r), end='\n')


# In[ ]:

zip(filename_light,indexlist_light)


# In[ ]:

rlist


# In[ ]:

indexlist_light


# In[ ]:

#Box plots of the data

#plt.xlim((0,.5))
#plt.ylim((0,700))
indexlist_darkness=array(indexlist_darkness)
indexlist_light=array(indexlist_light)

data=[indexlist_darkness[indexlist_darkness>0],indexlist_light[indexlist_light>0]]
#plt.boxplot(data)
p0,p1=0,1
bp = plt.boxplot(data,positions=[p0,p1], widths=0.3)

plt.setp(bp['boxes'], color='black') 
#for i in range(2):

y = data[0]
x = random.normal(p0, 0.04, size=len(y))
plt.plot(x, y, 'k.', alpha=0.8, ms=11)

y = data[1]
x = random.normal(p1, 0.04, size=len(y))
plt.plot(x, y, 'y.', alpha=0.8, ms=11)
plt.axes().set_aspect(10)

plt.xticks([])

plt.show()


# In[ ]:

from scipy.stats import mannwhitneyu


# In[ ]:

rlist_darkness=array(rlist_darkness)
rlist_light=array(rlist_light)
mannwhitneyu(rlist_light[indexlist_light>0],rlist_darkness[indexlist_darkness>0])


# In[ ]:

cuts=array([True,True,False])


# In[ ]:

a=array([0,0,0])


# In[ ]:

a[cuts]=2
a[~cuts]=1


# In[ ]:

a


# In[ ]:



