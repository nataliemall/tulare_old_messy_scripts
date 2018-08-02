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


def compile_data(folder_name):  # option 1 
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

def compile_averaged_data(folder_name): # option 2 
	file_name = os.path.join( folder_name, 'GW_change_comparison1995with2010.csv')  # set file name and path for GW data
	drawdown_data = pd.read_csv(file_name)

	crop_data = pd.read_csv(os.path.join(folder_name, 'orchard_crop_acreage_difference.csv'))  # set file name and path for crop data
	crop_data = crop_data.rename(columns={"COMTRS": "co_mtrs"})  # rename comtrs column for future index matching 
	crop_data_parsed = crop_data.ix[:,['co_mtrs','orchard_acreage_difference']]  # parse data to only include tree crop acreage 

	comtrs_well_id_table = pd.read_csv(os.path.join(folder_name, 'well_ids_with_comtrs_complete.csv') ) # set file name and path for well ID connection

	drawdown_data = drawdown_data.rename(columns={"CASGEM_STATION_ID": "county_ID"}) # rename county_ID column for future index matching 
	pdb.set_trace()
	gw_with_comtrs = pd.merge(drawdown_data, comtrs_well_id_table)  # connect GW data with connecting table
	gw_with_crop_data = pd.merge(gw_with_comtrs, crop_data_parsed)  # connect crop data with gw-connected table 

	return gw_with_crop_data


def compile_seasonal_drawdown_data(folder_name, year_analysing): # Plot the seasonal change in drawdown 
	file_name = os.path.join( folder_name, 'seasonal_df_year' + str(year_analysing)+ '.csv')  # set file name and path for GW data
	drawdown_data = pd.read_csv(file_name)
	drawdown_data = drawdown_data.rename(columns={"well_ID": "county_ID"}) # rename well_ID column for future index matching 
	drawdown_data.county_ID = np.int64(drawdown_data.county_ID)

	orchard_acreages = pd.read_csv(os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', (str(year_analysing) + 'files' ), (str(year_analysing) + '_orchard_by_comtrs.csv')  ))
	orchard_acreages = orchard_acreages.rename(columns={"COMTRS": "co_mtrs"})  # rename comtrs column for future index matching 

	comtrs_well_id_table = pd.read_csv('well_ids_with_comtrs_complete.csv')  # set file name and path for well ID connection
	
	gw_with_comtrs = pd.merge(drawdown_data, comtrs_well_id_table)  # connect GW data with connecting table
	gw_with_crop_data = pd.merge(gw_with_comtrs, orchard_acreages)  # connect crop data with gw-connected table 


	gw_with_crop_data['seasonal_change'] = gw_with_crop_data.dry_season - gw_with_crop_data.rainy_season  # high depletion means very large, positive number 
	# pdb.set_trace()
	# print('heres where we are stopped')
	return gw_with_crop_data, year_analysing



def plot_crops_v_gw(gw_with_crop_data):
	plt.scatter(gw_with_crop_data.orchard_acreage_difference, gw_with_crop_data.RP_difference)
	plt.xlabel('Change in crop acreage within section')
	plt.ylabel('Change in GW drawdown of well ')
	x = gw_with_crop_data.orchard_acreage_difference
	y = gw_with_crop_data.RP_difference

	idx = np.isfinite(x) & np.isfinite(y)
	test = (np.polyfit(x[idx], y[idx], 1))
	plt.plot(x[idx], test[0]*x[idx] + test[1])
	# plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))

	plt.figure()
	plt.hist(x,35)
	plt.title('Groundwater drawdown 1990 - 2010')
	plt.xlabel('Change in drawdown (larger number means more severe depletion)')
	plt.ylabel('number of wells')
	plt.show()
	pdb.set_trace()

def plot_drawdown_with_year(year_analysing): 
	x_column = 'tree_crop_acreage_year' + str(year_analysing)
	plt.scatter(gw_with_crop_data[x_column], gw_with_crop_data.seasonal_change)

	x = gw_with_crop_data[x_column]
	y = gw_with_crop_data.seasonal_change

	idx = np.isfinite(x) & np.isfinite(y)
	test = (np.polyfit(x[idx], y[idx], 1))
	plt.plot(x[idx], test[0]*x[idx] + test[1])
	# plt.xlabel('Orchard crop acreage within each section')
	# plt.ylabel('Change in GW drawdown of well from rainy season to dry season ')
	plt.show()	


# gw_with_crop_data = compile_data('tree_crop_gw_comparison1')  # 2012 data comparison with 2012 crop data 


# gw_with_crop_data = compile_averaged_data('tree_crop_gw_comp_2010_1990')

# gw_with_crop_data = compile_averaged_data('tree_crop_gw_dry_season_comparison')

# for graph_num, year in enumerate(range (1990, 2017)):
# 	gw_with_crop_data, year_analysing = compile_seasonal_drawdown_data('seasonal_drawdown_yearly', 1991)
# 	plot_drawdown_with_year(year_analysing)

# 	fig, (graph_num, ax2) = plt.subplots(2, sharey=True)


##### plot a bunch right next to each other###########

fig, axs = plt.subplots(2,5, figsize=(15, 6), facecolor='w', edgecolor='k', sharey = True) #, sharex = True)
fig.subplots_adjust(hspace = .5, wspace=.001)

axs = axs.ravel()

for i in range(7):
    year_analysing = 2010 + i 
    gw_with_crop_data, year_analysing = compile_seasonal_drawdown_data('seasonal_drawdown_yearly', year_analysing)
    x_column = 'tree_crop_acreage_year' + str(year_analysing)
    x = gw_with_crop_data[x_column]
    y = gw_with_crop_data.seasonal_change
    # pdb.set_trace()
    axs[i].scatter(x, y)
    axs[i].set_title(str(year_analysing))
axs[0].set(ylabel = 'GW seasonal drawdown')
axs[5].set(xlabel = 'Total acreage of orchard crops')
# fig.xlabel = ('Orchard crop acreage')
# fig.ylabel = ('Change in GW drawdown of well from rainy season to dry season ')
plt.show()



# gw_with_crop_data = compile_averaged_data('tree_crop_gw_rainy_season_comparison')
pdb.set_trace()

# plot_crops_v_gw(gw_with_crop_data)






