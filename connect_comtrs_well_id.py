###############  Takes the file of wells already connected to a COMTRS and spits out a file of well+coordinate data not yet connected 


# File goals:
	# Extract the county_ids from COMTRS_with_well_county_ID3.csv 
	# Compare this to the list of county_ids save (the list of well IDs in TLB)
	# Make another table of only the county_ids and coordinate locations in TLB that are not already listed
	# save this file and import it into QGIS 
	# merge by location and repeat this process 

import numpy as np 
import math 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import pdb
import pandas as pd
import seaborn as sns
from tqdm import tqdm  # for something in tqdm(something something):


def get_gqis_merged_data(COMTRS_with_well_county):

	qgis_merged_data = pd.read_csv(str(COMTRS_with_well_county + '.csv'), sep = ',')  # reads iteration 1 of the connected data 

	try:
		qgis_connected_wells = qgis_merged_data.county_ID.astype(np.int64)
	except:
		qgis_connected_wells = qgis_merged_data.CASGEM_STA.astype(np.int64)

	set_of_connected_wells = set(qgis_connected_wells)

	all_well_ids = pd.read_csv('tlb_county_IDs_lat_lon.csv' , sep = ',')
	# or 
	# all_well_ids = pd.read_csv('wells_not_yet_included_iter9.csv' , sep = ',')
	print('set all_well_ids to the subset you want to look through')
	pdb.set_trace()
	wells_not_yet_included = pd.Series()
	wells_already_included = pd.Series()
	for num, well_indiv_id in enumerate(tqdm(all_well_ids.CASGEM_STATION_ID)):
		if well_indiv_id in set_of_connected_wells:
			print('this well is already listed')
			indiv_included_well = all_well_ids.loc[all_well_ids.CASGEM_STATION_ID == well_indiv_id]
			wells_already_included = wells_already_included.append(indiv_included_well)
			# pdb.set_trace()
		else: 
			if num == 0:
				wells_not_yet_included = all_well_ids.loc[all_well_ids.CASGEM_STATION_ID == well_indiv_id]
				# pdb.set_trace()
			else: 
				well_not_listed = all_well_ids.loc[all_well_ids.CASGEM_STATION_ID == well_indiv_id]
				wells_not_yet_included = wells_not_yet_included.append(well_not_listed)
				# pdb.set_trace()

			print(f'A well not included is {well_indiv_id}')

	wells_not_yet_included = wells_not_yet_included.set_index('CASGEM_STATION_ID')
	wells_not_yet_included = wells_not_yet_included[['LATITUDE', 'LONGITUDE']]
			# save these wells to a separate file containing the geographic coordinates 
	return wells_already_included, wells_not_yet_included


def create_comtrs_wellid_table():

	for iter in range(12):
		iter_data = pd.read_csv(str('COMTRS_with_well_county_round' + str(iter+1) + '.csv'), sep = ',') # reads each file from the QGIS iterations 
		iter_data = iter_data.rename(columns={"CASGEM_STA": "county_ID"}) # renames the CASGEM_STA column for consistency

		well_ids_with_comtrs = iter_data.ix[:, ['county_ID','co_mtrs']]  # saves only the county ID and comtrs column 
		well_ids_with_comtrs.county_ID = well_ids_with_comtrs.county_ID.astype(int)  # converts the well IDs to integers 

		if iter == 0:
			well_ids_with_comtrs_complete = well_ids_with_comtrs  # begins complete table 
		else: 
			well_ids_with_comtrs_complete = well_ids_with_comtrs_complete.append(well_ids_with_comtrs)  #appends iteration to the overall table 

	return well_ids_with_comtrs_complete 


# wells_already_included, wells_not_yet_included = get_gqis_merged_data('COMTRS_with_well_county_round12')
# pdb.set_trace()
# wells_not_yet_included.to_csv('wells_not_yet_included_iter10.csv')

well_ids_with_comtrs_complete = create_comtrs_wellid_table()  # includes 14245 wells (114 not yet connected through QGIS)

well_ids_with_comtrs_complete.to_csv('well_ids_with_comtrs_complete.csv')

pdb.set_trace()









