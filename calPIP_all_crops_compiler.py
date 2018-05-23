#calPIP_all_crops_compiler.py 
#For given year, run loop for all crop types available in the data 


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


# Function: enter year for desired data compilation, run for that year 
def calPIP_summed(year): 

    year_file  = 'calPIP' + str(year) + '.csv'
    file_name = os.path.join('calPIP_includes_crop_areas', year_file)
    calPIP_data = pd.read_csv(file_name, sep = '\t')   #Pulls data from CSV file for the year

    crop_list = calPIP_data.SITE_NAME.unique()
    column_list = []
    # pdb.set_trace()
    for crop_type in tqdm(crop_list): 
        if type(crop_type) == float:
            crop_cleaned = str(crop_type)
            column_list.append(crop_cleaned)
        else:
            crop_strings = str(crop_type[0:15] + ' acres')
            crop_cleaned = crop_strings.replace("/", "_")  # transform these names by replacing '/' with '_' 
            column_list.append(crop_cleaned)
    # pdb.set_trace()

    all_COMTRS = calPIP_data.COMTRS.unique()
    array_zeros1 = np.full((len(all_COMTRS), len(crop_list)), np.zeros) #array of zeros for dataset
    crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ column_list ] )   # makes overall dataframe for all crop types 

    # Runs for each crop type, then connects to larger calPIP array using COMTRS index 
    crop_iter = 0 
    for crop_type in tqdm(crop_list):
        calPIP_data
        crop_type_vals = calPIP_data.loc[lambda df: calPIP_data.SITE_NAME == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
        no_location_IDs = len(crop_type_vals.SITE_LOCATION_ID.unique()) # number of unique parcel IDs for specific crop 
        ## ^ Edit location ID search - test for different SITE_LOCATION_ID
        number_of_null_site_location_ids = sum(pd.isnull(crop_type_vals.SITE_LOCATION_ID))

        COMTRS_list = crop_type_vals.COMTRS.unique()
        no_COMTRS = len(crop_type_vals.COMTRS.unique())   # number of unique COMTRS that grow specific crop 
        
        crop_column = column_list[crop_iter]
        crop_iter = crop_iter + 1

        save_crop_file = 1 
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
                total_acres = parcels_in_COMTRS.AMOUNT_PLANTED.iloc[0]   # if only 1 value, just use that value 
            else:
                parcel_IDs = parcels_in_COMTRS.SITE_LOCATION_ID.unique()  # array of unique parcel values in section
                no_parcels = len(parcel_IDs)   # number of parcels within the COMTRS
                acreages_for_each_site_loc = np.zeros([no_parcels, 1])  # empty array for the summed acreage for each parcel (site location)
                parcel_iter = 0 
                for individual_site in parcel_IDs: #goes through the individual sites in the secition 
                    specific_parcel = parcels_in_COMTRS.loc[parcels_in_COMTRS.SITE_LOCATION_ID == individual_site] # locates all permits a specific site
                    total_at_site_loc = max(specific_parcel.AMOUNT_PLANTED)  # maximum acreage reported for that SITE_LOCATION_ID 
                    if pd.isnull(individual_site) == True or individual_site == np.nan:   # If site_ID is not labelled
                        total_at_site_loc = sum(specific_parcel.AMOUNT_PLANTED.unique()) # sum up all unique area values
                    acreages_for_each_site_loc[parcel_iter] = total_at_site_loc
                    total_acres = sum(acreages_for_each_site_loc)
                    parcel_iter = parcel_iter + 1 
                        # pdb.set_trace()

            crop_acres_list[COMTRS_iter] = total_acres
            COMTRS_iter = COMTRS_iter + 1 

        crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 
        crop4_df[crop_column] = crop2_df[crop_column].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 

        crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']

        save_acres = 1     # Saves each crop's data for each COMTRS 
        if save_acres == 1:
            crop3_df = crop2_df.reset_index()
            crop3_df.columns = ['COMTRS', crop_column]
            directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', str(year) + 'files' )
            try: 
                crop3_df.to_csv(os.path.join(directory, (str(year) + crop_column + '.csv' ) ), header = True, na_rep = '0', index = False)   
            except: 
                os.mkdir(directory) 
                crop3_df.to_csv(os.path.join(directory, (str(year) + crop_column + '.csv' ) ), header = True, na_rep = '0', index = False)

    crop5_df = crop4_df.reset_index()
    path_name = os.path.join(directory, (str(year) + '_all_crops.csv')) 
    crop5_df.to_csv(os.path.join(directory, (str(year) + '_all_crops.csv')), header = True, na_rep = '0', index = False)
    print(f'Saved compiled {year} data in {path_name}')
    pdb.set_trace()

    return crop5_df, crop2_df 


    # Next steps: 
        # for 2007_all_crops, sum the acreage for each crop type
        # locate the column position of top 10 crops 
        # for each of these crops, sum up the acres for each county  

calPIP_summed(2007)
pdb.set_trace()


