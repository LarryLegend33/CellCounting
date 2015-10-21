import numpy as np
import os
from matplotlib import pyplot as pl
from scipy import stats
from collections import Counter

#this lists all elements of the current working direcotry

temp = [np.load(f) for f in os.listdir(os.getcwd()) if f != '#imagall.py' if f != 'imagall.py' if  f!=  '.DS_Store' if f!= 'imagall2.py' if f!= 'depthmap.py']

#recursively concatenates all npy files in temp
catmat = reduce(lambda x,y: np.concatenate((x,y), axis =1), temp)

colordict = {'R':1,'G':2,'B':3,'RG':4,'RB':5,'GB':6,'RGB':7,'':8}
labels = ['R','G','B','RG','RB','GB','RGB','']
indicies = map(lambda i: i + 1, range(7))
index_replace = [colordict[s] for s in catmat[0]]
print(Counter(catmat[0]))

#correction for confocal slip. adds 121 pixels to yvals above 640, 242 to yvals above 1280

catmat[1] = [float(y) + 121 if float(catmat[2,x]) > 640 else float(y) for x,y in enumerate(catmat[1])]

catmat[1] = [float(y) + 121 if float(catmat[2,x]) > 1280 else float(y) for x,y in enumerate(catmat[1])]


firstlayer = [catmat[0,i] for i,j in enumerate(catmat[1]) if float(j) < 400]
secondlayer = [catmat[0,k] for k,l in enumerate(catmat[1]) if float(l) >= 400 and float(l) < 800]
thirdlayer =  [catmat[0,m] for m,n in enumerate(catmat[1]) if float(n) >= 800 and float(n) < 1200]
fourthlayer =  [catmat[0,o] for o,p in enumerate(catmat[1]) if float(p) >= 1200]
#fifthlayer =  [catmat[0,q] for q,r in enumerate(catmat[1]) if float(r) >= 1600]



firstlayercount = Counter(firstlayer)
secondlayercount = Counter(secondlayer)
thirdlayercount =  Counter(thirdlayer)
fourthlayercount =  Counter(fourthlayer)
#fifthlayercount =  Counter(fifthlayer)


firstlayer2 = [catmat[0,i] for i,j in enumerate(catmat[1]) if float(j) < 300]
secondlayer2 = [catmat[0,k] for k,l in enumerate(catmat[1]) if float(l) >= 300 and float(l) < 600]
thirdlayer2 =  [catmat[0,m] for m,n in enumerate(catmat[1]) if float(n) >= 600 and float(n) < 900]
fourthlayer2 =  [catmat[0,o] for o,p in enumerate(catmat[1]) if float(p) >= 600 and float(p) < 800]
fifthlayer2 =  [catmat[0,q] for q,r in enumerate(catmat[1]) if float(r) >= 900]

toplayer =  [catmat[0,i] for i,j in enumerate(catmat[1]) if float(j) < 300]
midlayer = [catmat[0,k] for k,l in enumerate(catmat[1]) if float(l) >= 300 and float(l) < 600]
bottomlayer = [catmat[0,k] for k,l in enumerate(catmat[1]) if float(l) >= 600]

toplayercount = Counter(toplayer)
midlayercount = Counter(midlayer)
bottomlayercount = Counter(bottomlayer)



firstlayer2count = Counter(firstlayer2)
secondlayer2count = Counter(secondlayer2)
thirdlayer2count = Counter(thirdlayer2)
fourthlayer2count = Counter(fourthlayer2)
fifthlayer2count = Counter(fifthlayer2)


#pl.hexbin(catmat[1], catmat[2], gridsize = 30)
#pl.colorbar()
#pl.show()


reds = catmat[:, catmat[0,:] == 'R']
rgs = catmat[:, catmat[0,:] == 'RG']
greens = catmat[:, catmat[0,:] == 'G']
blues = catmat[:, catmat[0,:] == 'B']

dummypoint = (['',''],['0','2000'], ['0','2000']) # dummy point just expands the bounds of the hexbin plot, and only will have one point so will show up blank w mincnt set at 1. 
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
#pl.hexbin(blues[1],blues[2], mincnt = 0, linewidth = 0, cmap = 'Blues', gridsize = 25)
#pl.hexbin(greens[1],greens[2], mincnt = 1, linewidth = 0, cmap = 'Blues', gridsize = 25)
pl.hexbin(rgs[1],rgs[2], mincnt = 1, linewidth = 0, cmap = 'Blues', gridsize = 25)

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
    


