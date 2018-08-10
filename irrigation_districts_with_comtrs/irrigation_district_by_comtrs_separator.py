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
agency_names = []

for num, irrigation_dist in enumerate(all_tlb_data.AGENCYNAME ):
	pdb.set_trace()
	test2 = irrigation_dist.replace('/','-')

	agency_names[num] = test2
# test = all_tlb_data.CO_MTRS[all_tlb_data]

# all_tlb_data.columns


irrigation_districts_tlb = all_tlb_data.AGENCYNAME.unique()
# test = irrigation_districts_tlb.tolist()

pdb.set_trace()

for irrigation_dist in irrigation_districts_tlb:   # 342 unique regions 
	print(f'District is:{irrigation_dist}')

	if irrigation_dist == 'North Kern Water Storage District':
		pdb.set_trace()
		manual_test = pd.read_csv('North_Kern_Water_Storage_District.csv')


	comtrs = all_tlb_data.CO_MTRS[all_tlb_data.AGENCYNAME == irrigation_dist]
	comtrs = pd.DataFrame(comtrs)

	comtrs.to_csv(str(irrigation_dist + '.csv'), index = False  )

	# pdb.set_trace()


# all_tlb_data.AGENCYUNIQ


# pdb.set_trace()



