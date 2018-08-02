
import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import os 
import pdb
import pandas as pd
import re 
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):


# fig=plt.figure(figsize=(15, 6),facecolor='w', edgecolor='k')
# for i in range(10):

#     #this part is just arranging the data for contourf 
#     ind2 = py.find(zz==i+1)
#     sfr_mass_mat = np.reshape(sfr_mass[ind2],(pixmax_x,pixmax_y))
#     sfr_mass_sub = sfr_mass[ind2]
#     zi = griddata(massloclist, sfrloclist, sfr_mass_sub,xi,yi,interp='nn')


#     temp = 250+i  # this is to index the position of the subplot
#     ax=plt.subplot(temp)
#     ax.contourf(xi,yi,zi,5,cmap=plt.cm.Oranges)
#     plt.subplots_adjust(hspace = .5,wspace=.001)

#     #just annotating where each contour plot is being placed
#     ax.set_title(str(temp))


fig, axs = plt.subplots(2,5, figsize=(15, 6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.001)

axs = axs.ravel()

for i in range(10):

    axs[i].contourf(np.random.rand(10,10),5,cmap=plt.cm.Oranges)
    axs[i].set_title(str(250+i))

plt.show()