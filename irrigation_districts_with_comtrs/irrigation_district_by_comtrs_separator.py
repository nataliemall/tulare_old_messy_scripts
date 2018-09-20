### Separate out the different irrigation distrcts from tlb_irrigation_districts_all.csv

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
import seaborn as sns
import re 
# from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):


all_tlb_data = pd.read_csv('tlb_irrigation_districts_all.csv')

test = all_tlb_data.AGENCYNAME   # Replace '/' with '-'
agency_names = np.zeros(len(test))
agency_names = agency_names.tolist()
agency_names = []


### Figure out how to remove the slashes here ###
for num, irrigation_dist in enumerate(all_tlb_data.AGENCYNAME ):

	if "/" in irrigation_dist:

		previous = irrigation_dist 
		test2 = irrigation_dist.replace('/','-')
	
		all_tlb_data.AGENCYNAME[num] = test2
		pdb.set_trace()

	# if num == 0:
	# 	agency_names= test2
	# else:
	# 	pdb.set_trace()
	# 	agency_names = pd.concat( agency_names, test2 )
# test = all_tlb_data.CO_MTRS[all_tlb_data]


# all_tlb_data.columns

pdb.set_trace()	

irrigation_districts_tlb = all_tlb_data.AGENCYNAME.unique()
# test = irrigation_districts_tlb.tolist()

pdb.set_trace()

for irrigation_dist in irrigation_districts_tlb:   # 342 unique regions 
	print(f'District is:{irrigation_dist}')

	if irrigation_dist == 'North Kern Water Storage District':
		pdb.set_trace()
		# manual_test = pd.read_csv('North_Kern_Water_Storage_District.csv')


	comtrs = all_tlb_data.CO_MTRS[all_tlb_data.AGENCYNAME == irrigation_dist]
	comtrs = pd.DataFrame(comtrs)

	comtrs.to_csv(str(irrigation_dist + '.csv'), index = False  )

	# pdb.set_trace()


# all_tlb_data.AGENCYUNIQ


# pdb.set_trace()



