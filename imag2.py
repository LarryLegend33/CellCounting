# To Do
# Don't allow selection of a new cell w/out a return press

from sys import exit
import matplotlib.pyplot as pl
import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import Rectangle, Circle
from collections import Counter

red = raw_input('Please enter red file ')
green =raw_input('Please enter green file ')
blue = raw_input('Please enter blue file ')
depth = raw_input('D, DV, or V? ')

if depth != 'D' and depth != 'DV' and depth != 'V':

   print('invalid input')
   exit()

width = raw_input('M, ML, or L? ')

if width != 'M' and width != 'ML' and width != 'L':

   print('invalid input')
   exit()

fig = pl.figure()
ax = fig.add_axes([0,0,1,1])
pl.ion()
pl.show()

img_red = mpimg.imread(red)
img_green = mpimg.imread(green)
img_blue = mpimg.imread(blue)
im_start = pl.imshow(img_red)
cell_list = []


class Cell:

   def __init__(self,xloc,yloc):
        
        self.x = xloc
        self.y = yloc
        self.isred = False
        self.isgreen = False
        self.isblue = False
        self.cid_Cell = fig.canvas.mpl_connect('key_press_event',self.color)
        self.color = "" 

   def color(self,event):


        if event.key == 'r':

           self.isred = True
           print("Cell is Red")

        elif event.key == 'g':

           self.isgreen = True
           print("Cell is Green")

        elif event.key == 'b':

           self.isblue = True
           print("Cell is Blue")

        elif event.key == 'enter':
           
           fig.canvas.mpl_disconnect(self.cid_Cell)
           print("Cell Created")
           curr_cell = pl.gca().patches[-1]
           
           if self.isred and self.isgreen and self.isblue:
               curr_cell.set_facecolor('k')
               self.color = "RGB"
         
           elif self.isred and self.isgreen:
               curr_cell.set_facecolor('y')
               self.color = "RG"
           
           elif self.isred and self.isblue:
               curr_cell.set_facecolor('m')
               self.color = "RB"

           elif self.isgreen and self.isblue:
               curr_cell.set_facecolor('c')
               self.color= "GB"

           elif self.isred:
               curr_cell.set_facecolor('r')
               self.color = "R"
           
           elif self.isgreen:
               curr_cell.set_facecolor('g')
               self.color = "G"
           
           elif self.isblue:
               curr_cell.set_facecolor('b')
               self.color = "B"
           
           else:
               curr_cell.set_facecolor('w')

def on_key(event):

    global cell_list
    zord = 1

    if event.key == 'left':
      del(ax.images[0])
      imag_red = pl.imshow(img_red, zorder = zord)
      pl.draw()

    elif event.key == 'up':

      del(ax.images[0])
      imag_green = pl.imshow(img_green, zorder = zord)
      pl.draw()

    elif event.key == 'right':

      del(ax.images[0])
      imag_blue = pl.imshow(img_blue, zorder = zord)
      pl.draw()

    elif event.key == 'f1':

      make_graph(cell_list)
    
    elif event.key == 'f2':

      del(pl.gca().patches[-1])
      del(cell_list[-1])  
      pl.draw()
      print('Cell Subtracted')

def on_click(event):

     global cell_list
     circ = ax.add_patch(Circle((event.xdata,event.ydata),10))
     circ.set_zorder(2)
     circ.set_edgecolor('w')
     pl.draw()
     xloc = round(event.xdata*(640.0/1024.0),2) #this converts pixel coords to micron coords
     yloc = round(event.ydata*(640.0/1024.0),2)
     new_cell = Cell(xloc,yloc)
     cell_list.append(new_cell)
    

def make_graph(lis):
    
   
   # fig2 = pl.figure()
   # ax2 = fig2.add_subplot(111)
    numcells = range(len(cell_list))
    color_list = [cell_list[i].color for i in numcells]
    C = Counter(color_list)
    print(color_list)
    
    print(C)    
    xvals = [cell_list[j].x for j in numcells]
    yvals = [cell_list[k].y for k in numcells]
   # colordict = {'R':1,'G':2,'B':3,'RG':4,'RB':5,'GB':6, 'RGB':7,'':8}
   # dictdex = [colordict[s] for s in color_list]
   # pl.scatter(dictdex, xvals)
   

    if depth == 'DV':

       xvals =  [x + 640 for x in xvals] 

    elif depth == 'V':

       xvals = [x + 1280 for x in xvals]

    if width == 'ML':

       yvals = [y + 640 for y in yvals]

    elif width == 'L':

       yvals = [y + 1280 for y in yvals]

   # print(xvals)
   # print(yvals)

    output = np.matrix([color_list, xvals, yvals])
    print(output)
    np.save('temp',output)

cid = fig.canvas.mpl_connect('key_press_event',on_key)
cid_mousepress = fig.canvas.mpl_connect('button_press_event', on_click)






