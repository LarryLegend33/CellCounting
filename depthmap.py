import numpy as np
import os
from matplotlib import pyplot as pl
from scipy import stats
from collections import Counter

#this lists all elements of the current working direcotry

temp = [np.load(f) for f in os.listdir(os.getcwd()) if f != '#imagall.py' if f != 'imagall.py' if  f!=  '.DS_Store' if f!= 'imagall2.py' if f!= 'depthmap.py']

# use all blue values for dorsal surface. then filter by blue, b/c no npy files from analysis have blue cells. do this after confocal slip correction b/c it will
#correct the dorsal surface controls for slip too. 

#recursively concatenates all npy files in temp. puts together 3 arrays of labels, xvals, and yvals from all files for each cell. 
catmat = reduce(lambda x,y: np.concatenate((x,y), axis =1), temp)

colordict = {'R':1,'G':2,'B':3,'RG':4,'RB':5,'GB':6,'RGB':7,'':8}
labels = ['R','G','B','RG','RB','GB','RGB','']
indicies = map(lambda i: i + 1, range(7))
index_replace = [colordict[s] for s in catmat[0]]
print(Counter(catmat[0]))

#correction for confocal slip. adds 121 pixels to xvals above 640, 242 to xvals above 1280 b/c confocal slips upwards by 121 pixels every time it moves laterally. 

catmat[1] = [float(y) + 121 if float(catmat[2,x]) > 640 else float(y) for x,y in enumerate(catmat[1])]
catmat[1] = [float(y) + 121 if float(catmat[2,x]) > 1280 else float(y) for x,y in enumerate(catmat[1])]


#THIS IS FOR HEXBIN PLOTTING. DON'T PLOT THE BLUE DORSAL SURFACE CONTROL NEURONS
reds = catmat[:, catmat[0,:] == 'R']
rgs = catmat[:, catmat[0,:] == 'RG']
greens = catmat[:, catmat[0,:] == 'G']


#DEPTH CALCULATION SHOULD OCCUR HERE. 

dorsal_surface = catmat[:, catmat[0,:] == 'B']
#here, for each cell in reds, rgs, and greens, find the neuron with the closest x coordinate (eg. closest row 2 value) in dorsal_surface. take the row 1 value of reds, rgs, or greens and subtract the row 1 value of dorsal_surface at that index.
 #SO NEED FUNCTION THAT SAYS "FIND THE INDEX WHERE THE TWO VALUES ARE MOST SIMILAR BETWEEN TWO LISTS (A and B) OF LENGTH X". OUTPUT SHOULD BE A LIST OF LENGTH X THAT CONTAINS INDICIES OF LIST B THAT ARE CLOSEST TO THE VALUES AT EACH INDEX IN LIST A  

# LOOP MUST GO THROUGH EACH RED[2],GREEN[2],AND RG[2] ARRAY CELL BY CELL: EACH TIME, IT SEARCHES DORSAL_SURFACE[2]. SO FIRST MAKE A LIST OF THESE. THEN GIVE BACK THE INDEX WHERE THEY ARE THE CLOSEST, AND SUBTRACT DORSAL_SURFACE[1] FROM RED[1], GREEN[1] OR RG[1] 


red_depthadj = np.empty(reds.shape,dtype = (np.str,7))
red_depthadj[0] = reds[0]
red_depthadj[2] = reds[2]

green_depthadj = np.empty(greens.shape, dtype = (np.str,7))
green_depthadj[0] = greens[0]
green_depthadj[2] = greens[2]

rgs_depthadj = np.empty(rgs.shape, dtype = (np.str,7))
rgs_depthadj[0] = rgs[0]
rgs_depthadj[2] = rgs[2]

temp_sub1 = np.zeros((reds.shape[1], dorsal_surface.shape[1]))
for i in range(reds.shape[1]):
  for j in range(dorsal_surface.shape[1]): 
     temp_sub1[i,j] = float(reds[2,i])-float(dorsal_surface[2,j])  #this will have a distance for each cell in reds in rows, from each cell in dors_surf in cols
  minind = np.argmin(np.abs(temp_sub1[i,:]))
  red_depthadj[1,i] = float(reds[1,i]) - float(dorsal_surface[1, minind])
 
temp_sub2 = np.zeros((greens.shape[1], dorsal_surface.shape[1]))
for i in range(greens.shape[1]):
  for j in range(dorsal_surface.shape[1]): 
     temp_sub2[i,j] = float(greens[2,i])-float(dorsal_surface[2,j])  #this will have a distance for each cell in reds in rows, from each cell in dors_surf in cols
  minind = np.argmin(np.abs(temp_sub2[i,:]))
  green_depthadj[1,i] = float(greens[1,i]) - float(dorsal_surface[1, minind])

temp_sub3 = np.zeros((rgs.shape[1], dorsal_surface.shape[1]))
for i in range(rgs.shape[1]):
  for j in range(dorsal_surface.shape[1]): 
     temp_sub3[i,j] = float(rgs[2,i])-float(dorsal_surface[2,j])  #this will have a distance for each cell in reds in rows, from each cell in dors_surf in cols
  minind = np.argmin(np.abs(temp_sub3[i,:]))
  rgs_depthadj[1,i] = float(rgs[1,i]) - float(dorsal_surface[1, minind])

catmat2 = np.concatenate((red_depthadj, green_depthadj, rgs_depthadj), axis=1)
         
firstlayer = [catmat2[0,i] for i,j in enumerate(catmat2[1]) if float(j) < 200] 
secondlayer = [catmat2[0,k] for k,l in enumerate(catmat2[1]) if float(l) >= 200 and float(l) < 400]
thirdlayer =  [catmat2[0,m] for m,n in enumerate(catmat2[1]) if float(n) >= 400 and float(n) < 600]
fourthlayer =  [catmat2[0,o] for o,p in enumerate(catmat2[1]) if float(p) >= 600 and float(p) < 800]
fifthlayer =  [catmat2[0,q] for q,r in enumerate(catmat2[1]) if float(r) >= 800 and float(r) < 1000]
sixthlayer =  [catmat2[0,s] for s,t in enumerate(catmat2[1]) if float(t) >= 1000]
firstlayercount = Counter(firstlayer)
secondlayercount = Counter(secondlayer)
thirdlayercount =  Counter(thirdlayer)
fourthlayercount =  Counter(fourthlayer)
fifthlayercount =  Counter(fifthlayer)
sixthlayercount = Counter(sixthlayer)

firstlayer2 = [catmat2[0,i] for i,j in enumerate(catmat2[1]) if float(j) < 300] 
secondlayer2 = [catmat2[0,k] for k,l in enumerate(catmat2[1]) if float(l) >= 300 and float(l) < 600]
thirdlayer2 =  [catmat2[0,m] for m,n in enumerate(catmat2[1]) if float(n) >= 600 and float(n) < 900]
fourthlayer2 =  [catmat2[0,o] for o,p in enumerate(catmat2[1]) if float(p) >= 900 and float(p) < 1200]
#fifthlayer2 =  [catmat2[0,q] for q,r in enumerate(catmat2[1]) if float(r) >= 800 and float(r) < 1000]
sixthlayer2 =  [catmat2[0,s] for s,t in enumerate(catmat2[1]) if float(t) >= 1200]
firstlayercount2 = Counter(firstlayer2)
secondlayercount2 = Counter(secondlayer2)
thirdlayercount2 =  Counter(thirdlayer2)
fourthlayercount2 =  Counter(fourthlayer2)
#fifthlayercount2 =  Counter(fifthlayer)
sixthlayercount2 = Counter(sixthlayer2)



rrg_depthadj = np.concatenate((red_depthadj, rgs_depthadj), axis=1)


redadj_yquant = stats.mstats.mquantiles(red_depthadj[1].astype(np.float32), prob = [0, .25,.5,.75,1])
greenadj_yquant = stats.mstats.mquantiles(green_depthadj[1].astype(np.float32), prob = [0, .25,.5,.75,1])
rgsadj_yquant = stats.mstats.mquantiles(rgs_depthadj[1].astype(np.float32), prob = [0, .25,.5,.75,1])

rrg_yquant = stats.mstats.mquantiles(rrg_depthadj[1].astype(np.float32), prob = [0, .25,.5,.75,1])

# PLOT THE HEATMAPS
dummypoint = (['',''],['0','2000'], ['0','2000'])
reds = np.concatenate((reds,dummypoint), axis =1)
greens = np.concatenate((greens,dummypoint), axis =1)  
rgs = np.concatenate((rgs,dummypoint), axis = 1)  


fig = pl.figure(frameon = False)
ax = pl.Axes(fig, [0,0,1,1])
#ax = pl.Axes(fig, [0,0,.75,.75])
ax.set_axis_off()
fig.add_axes(ax)
pl.axis([0,2000,0,2000])
#pl.hexbin(reds[1],reds[2], mincnt = 1, linewidth = 0, cmap = 'Blues', gridsize = 25)
pl.hexbin(rgs[1],rgs[2], mincnt = 1, linewidth = 0, cmap = 'Blues', gridsize = 25)
#pl.hexbin(greens[1],greens[2], mincnt = 1, linewidth = 0, cmap = 'Blues', gridsize = 25)
pl.colorbar()
pl.show()


yquantile_all = stats.mstats.mquantiles(catmat[1].astype(float), prob = [0, .25, .5, .75, 1])

xquantile_all = stats.mstats.mquantiles(catmat[2].astype(float), prob = [0, .25, .5, .75, 1])

# red_quantiles_x = stats.mstats.mquantiles(reds[1].astype(float), prob = [0, .25, .5, .75, 1])

# red_quantiles_y = stats.mstats.mquantiles(reds[2].astype(float), prob = [0, .25, .5, .75, 1])

# rg_quantiles_x = stats.mstats.mquantiles(rgs[1].astype(float), prob = [0, .25, .5, .75, 1])

# rg_quantiles_y = stats.mstats.mquantiles(rgs[2].astype(float), prob = [0, .25, .5, .75, 1])
 
# green_quantiles_x = stats.mstats.mquantiles(greens[1].astype(float), prob = [0, .25, .5, .75, 1])
 
# green_quantiles_y = stats.mstats.mquantiles(greens[2].astype(float), prob = [0, .25, .5, .75, 1])
 


# pl.figure()
# pl.scatter(index_replace, map(lambda j: -1*float(j), catmat[1]))
# pl.xticks(indicies, labels)
# pl.figure()
# pl.scatter(catmat[2], index_replace)
# pl.yticks(indicies, labels)
# pl.show()

 

# want to use a matrix instead of array as output of imag2. also, make sure to make scatters here
    


