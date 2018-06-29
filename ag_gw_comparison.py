## Python code to compile and compare the well data with tree acreage crop data 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import os 
import pdb
import pandas as pd
import re 
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):


def compile_data(folder_name):
	file_name = os.path.join( folder_name, 'df_well_ids_with_drawdown.csv')  # set file name and path for GW data
	drawdown_data = pd.read_csv(file_name)

	crop_data = pd.read_csv(os.path.join(folder_name, '2012_complete_acreage_breakdown.csv'))  # set file name and path for crop data
	crop_data = crop_data.rename(columns={"level_0": "co_mtrs"})  # rename comtrs column for future index matching 
	crop_data_parsed = crop_data.ix[:,['co_mtrs','tree_crop_acreage']]  # parse data to only include tree crop acreage 

	comtrs_well_id_table = pd.read_csv(os.path.join(folder_name, 'well_ids_with_comtrs_complete.csv') ) # set file name and path for well ID connection

	drawdown_data = drawdown_data.rename(columns={"CASGEM_STATION_ID": "county_ID"}) # rename county_ID column for future index matching 
	gw_with_comtrs = pd.merge(drawdown_data, comtrs_well_id_table)  # connect GW data with connecting table
	gw_with_crop_data = pd.merge(gw_with_comtrs, crop_data_parsed)  # connect crop data with gw-connected table 

	return gw_with_crop_data


def plot_crops_v_gw(gw_with_crop_data):
	plt.scatter(gw_with_crop_data.tree_crop_acreage, gw_with_crop_data.RP_change)
	plt.show()
	pdb.set_trace()



gw_with_crop_data = compile_data('tree_crop_gw_comparison1')

plot_crops_v_gw(gw_with_crop_data)