#calPIP_all_crops_2015
#For 2015, run loop for all crop types available in the data 


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import os 
import pdb
import pandas as pd
import seaborn as sns
import re 
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):

calPIP_2015_data = pd.read_csv('calPIP_includes_crop_areas/calPIP2015.csv', sep='\t') #Pulls data from CSV file for the year

crop_list = calPIP_2015_data.SITE_NAME.unique()
column_list = []
for crop_type in tqdm(crop_list): 
    crop_strings = str(crop_type[0:15] + ' acres')
    crop_cleaned = crop_strings.replace("/", "_")  # transform these names by replacing '/' with '_' 
    column_list.append(crop_cleaned)

all_COMTRS = calPIP_2015_data.COMTRS.unique()
array_zeros1 = np.full((len(all_COMTRS), len(crop_list)), np.zeros) #array of zeros for dataset
crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ column_list ] )   # makes overall dataframe for all crop types 

# Runs for each crop type, then connects to larger calPIP array using COMTRS index 
crop_iter = 0 
for crop_type in tqdm(crop_list):

    crop_type_vals = calPIP_2015_data.loc[lambda df: calPIP_2015_data.SITE_NAME == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
    no_location_IDs = len(crop_type_vals.SITE_LOCATION_ID.unique()) # number of unique parcel IDs for specific crop 
    ## ^ Edit location ID search - test for different SITE_LOCATION_ID

    COMTRS_list = crop_type_vals.COMTRS.unique()
    no_COMTRS = len(crop_type_vals.COMTRS.unique())   # number of unique COMTRS that grow specific crop 
    
    crop_column = column_list[crop_iter]
    crop_iter = crop_iter + 1

    save_crop_file = 0 
    if save_crop_file == 1:
        path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        crop_type_vals.to_csv(os.path.join(path, (crop_column +  '_all.csv') ) , header = True, na_rep = '0', index = False)   

    array_zeros = np.zeros([no_COMTRS, 1])  # array of the length of COMTRS for alfalfa
    crop2_df = pd.DataFrame(array_zeros, index = [COMTRS_list], columns = [str(crop_column)] )   # change column label to each type of crop 
    COMTRS_iter = 0 
    crop_acres_list = np.zeros([no_COMTRS, 1])
    for COMTRS_value in tqdm(COMTRS_list): 
        parcels_in_COMTRS = crop_type_vals.loc[crop_type_vals['COMTRS'] == COMTRS_value, :]  # filters by fields in this specific COMTRS section 

        if len(parcels_in_COMTRS.SITE_LOCATION_ID.unique()) == 1: 
            total_acres = parcels_in_COMTRS.AMOUNT_PLANTED.iloc[0]
        else:
            acres = parcels_in_COMTRS.AMOUNT_PLANTED.unique()   ###### put a check here to make sure they are separate parcels - use SITE_LOCATION_ID
            total_acres = sum(acres)   # adds up unique crop areas 
            # In this loop, put each acreage value in the crop4_df overall dataframe using iloc ??
        crop_acres_list[COMTRS_iter] = total_acres
        COMTRS_iter = COMTRS_iter + 1 

    crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 
    crop4_df[crop_column] = crop2_df[crop_column].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 

    crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']

    save_acres = 1     # Saves each crop's data for each COMTRS 
    if save_acres == 1:
        crop3_df = crop2_df.reset_index()
        crop3_df.columns = ['COMTRS', crop_column]
        path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        crop3_df.to_csv(os.path.join(path, (crop_column + '.csv' ) ), header = True, na_rep = '0', index = False)   

    pdb.set_trace()
crop5_df = crop4_df.reset_index()
crop5_df.to_csv(os.path.join(path, 'all_crops_2015.csv'), header = True, na_rep = '0', index = False)
pdb.set_trace()