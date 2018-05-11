#calPIP_all_crops_2015

#For 2015, run loop for all crop types available in the data 


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import os 
import pdb
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):



calPIP_2015_data = pd.read_csv('calPIP_includes_crop_areas/calPIP2015.csv', sep='\t')#, parse_dates=['DATE']) #error_bad_lines=False)#, index_col=0, parse_dates=True)

# print(calPIP_2015_data.columns)   # prints column names 
# COMTRS 
# calPIP_2015_data.COMTRS

crop_list = calPIP_2015_data.SITE_NAME.unique()

# crop_labels_complete = crop_list[1:10, :]
# column_list = np.zeros(len(calPIP_2015_data.SITE_NAME.unique()))
column_list = []
iter = 0 
for crop_type in tqdm(crop_list): 
    test3 = crop_type[0:10] + ' acres'
    # column_list[iter] = test3
    column_list.append(test3)
    iter = iter + 1

all_COMTRS = calPIP_2015_data.COMTRS.unique()
array_zeros1 = np.full((len(all_COMTRS), len(crop_list)), np.zeros) 
crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ column_list ] )   # makes overall dataframe for all crop types 
crop5_df = pd.DataFrame(index = [all_COMTRS])
# run for each crop type, then connect to larger calPIP array using some connector index 

pdb.set_trace()

crop_iter = 0 
for crop_type in tqdm(crop_list[0:2]):

    crop_type_vals = calPIP_2015_data.loc[lambda df: calPIP_2015_data.SITE_NAME == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
    no_location_IDs = len(crop_type_vals.SITE_LOCATION_ID.unique()) # number of unique parcel IDs for specific crop 
    no_COMTRS = len(crop_type_vals.COMTRS.unique())   # number of unique COMTRS that grow specific crop 

    save_crop_file = 0 
    if save_crop_file == 1:
        crop_type_vals.to_csv('alfalfa_TLB_all.csv')    # How to change to different name 

    COMTRS_list = crop_type_vals.COMTRS.unique()
    crop_df = pd.DataFrame({"COMTRS_alf": [COMTRS_list] })

    array_zeros = np.zeros([no_COMTRS, 1])  # array of the length of COMTRS for alfalfa
    crop2_df = pd.DataFrame(array_zeros, index = [COMTRS_list], columns = [ crop_type[0:10] + ' acres'] )   # change column label to each type of crop 
    crop_column = crop_type[0:10] + ' acres'

    test1 = crop2_df[lambda crop2_df: crop2_df.columns[0]]
    # pdb.set_trace()

    COMTRS_iter = 0 
    crop_acres_list = np.zeros([no_COMTRS, 1])
    # pdb.set_trace()
    for COMTRS_value in tqdm(COMTRS_list): 

        parcels_in_COMTRS = crop_type_vals.loc[crop_type_vals['COMTRS'] == COMTRS_value, :]  # filters by fields in this specific COMTRS section 
        # pdb.set_trace()

        if len(parcels_in_COMTRS.SITE_LOCATION_ID.unique()) == 1: 
            total_acres = parcels_in_COMTRS.AMOUNT_PLANTED.iloc[0]
        else:
            acres = parcels_in_COMTRS.AMOUNT_PLANTED.unique()   ###### put a check here to make sure they are separate parcels 
            total_acres = sum(acres)   # adds up unique crop areas 
            

            # IN this loop, put each acreage value in the crop4_df overall dataframe using iloc ??

        crop_acres_list[COMTRS_iter] = total_acres
        # crop2_df.crop_column[COMTRS_iter] = total_acres         # fix this  - how do I make the column name change depending on the crop used? 

        COMTRS_iter = COMTRS_iter + 1 

    crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 


    # crop4_df[lambda crop4_df: crop4_df.columns[crop_iter]] = crop_acres_list
    pdb.set_trace()

    # pd.merge(crop5_df, crop2_df, how = 'outer')#, on = index)
    crop4_df[index] = crop2_df.columns[0] 
    crop_iter = crop_iter + 1
    pdb.set_trace()


    save_acres = 1     # Saves each crop's data for each COMTRS 
    if save_acres == 1:
        crop_label = crop_type[0:10] + 'acres'



        crop3_df = crop2_df.reset_index()
        crop3_df.columns = ['COMTRS', crop_label]
        crop_file_name = crop_label + '.csv'
        # crop3_df.to_csv('crop_label.csv',header = True, na_rep = '0', index = False)    # how do I change the name of the csv file depending on the crop type? 
        
        path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        pdb.set_trace()


        crop4_df.to_csv(os.path.join(path, crop_file_name), header = True, na_rep = '0', index = False)   # HOW SAVE? 


        #make new row in the dataframe 

    pdb.set_trace()




































