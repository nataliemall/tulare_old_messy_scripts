#calPIP_all_crops_compiler.py 
#For given year, run loop for all crop types available in the data 


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import os 
import pdb
import pandas as pd
import re 
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):


def read_data(year):  # read calPIP downloaded data file for given year
    year_file  = 'calPIP' + str(year) + '.csv'
    file_name = os.path.join('calPIP_includes_crop_areas', year_file)
    calPIP_data = pd.read_csv(file_name, sep = '\t')   #Pulls data from CSV file for the year

    crop_list = calPIP_data.SITE_NAME.unique()
    pdb.set_trace()
    return crop_list, calPIP_data


def clean_columns(crop_list):  # remove slashes and spaces, cut to 20 characters and place 'acres' in column name
    # pdb.set_trace()
    column_list = []
    for crop_type in tqdm(crop_list): 
        if type(crop_type) == float:
            crop_cleaned = str(crop_type)
            column_list.append(crop_cleaned)
        else:
            crop_strings = str(crop_type[0:20] + ' acres')
            crop_cleaned = crop_strings.replace("/", "_")  # transform these names by replacing '/' with '_' 
            column_list.append(crop_cleaned)
    # pdb.set_trace()
    return column_list


def make_dataframe(year, calPIP_data, column_list, crop_list): # Build empty dataframe for the crop acreage summations 
    all_COMTRS = calPIP_data.COMTRS.unique()
    array_zeros1 = np.full((len(all_COMTRS), len(crop_list)), 0) #array of zeros for dataset
    crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ column_list ] )   # makes overall dataframe for all crop types 
    array_tulare = np.full((1, 1), 0)
    tulare_overall_by_crop = pd.DataFrame(array_tulare, columns = ['year'])
    # pdb.set_trace()
    tulare_overall_by_crop['year'] = year 
    # pdb.set_trace()
    return crop4_df, tulare_overall_by_crop 


def acreage_compiler(year, crop_type, crop_iter, column_list, calPIP_data):  # compiles acreage for each COMTRS location and stores the data 
    total_skipped = 0 
    # calPIP_data
    crop_type_vals = calPIP_data.loc[lambda df: calPIP_data.SITE_NAME == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
    no_location_IDs = len(crop_type_vals.SITE_LOCATION_ID.unique()) # number of unique parcel IDs for specific crop 
    ## ^ Edit location ID search - test for different SITE_LOCATION_ID
    number_of_null_site_location_ids = sum(pd.isnull(crop_type_vals.SITE_LOCATION_ID))

    COMTRS_list = crop_type_vals.COMTRS.unique()
    no_COMTRS = len(crop_type_vals.COMTRS.unique())   # number of unique COMTRS that grow specific crop 
    
    crop_column = column_list[crop_iter]
    crop_iter = crop_iter + 1
    crop_acres_tulare = 0 # reset crop acreage to zero 

    save_crop_file = 1 
    if save_crop_file == 1:
        # path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        # directory_overall_folder 
        if os.path.isdir("/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages"):
            print('folder does exist')
        else:
            os.mkdir('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages')
            print('Created calPIP_crop_acreages folder')


        # pdb.set_trace()
        directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', str(year) + 'files' )
        try: # puts in file if folder already exists
            crop_type_vals.to_csv(os.path.join(directory, (crop_column +  '_all.csv') ) , header = True, na_rep = '0', index = False)   
        except: # creates file folder and puts in values if folder does not yet exist 
            # pdb.set_trace()
            os.mkdir(directory) 
            crop_type_vals.to_csv(os.path.join(directory, (crop_column +  '_all.csv') ) , header = True, na_rep = '0', index = False)   
    array_zeros = np.zeros([no_COMTRS, 1])  # array of the length of COMTRS for alfalfa
    crop2_df = pd.DataFrame(array_zeros, index = [COMTRS_list], columns = [str(crop_column)] )   # change column label to each type of crop 
    # COMTRS_iter = 0 
    crop_acres_list = np.zeros([no_COMTRS, 1])
    
    for COMTRS_iter, COMTRS_value in enumerate(tqdm(COMTRS_list)): 
        parcels_in_COMTRS = crop_type_vals.loc[crop_type_vals['COMTRS'] == COMTRS_value, :]  # filters by fields in this specific COMTRS section 

        parcel_IDs = parcels_in_COMTRS.SITE_LOCATION_ID.unique()  # array of unique parcel values in section
        num_parcels = len(parcel_IDs)   # number of parcels within the COMTRS
        # if crop_type_vals
        if num_parcels == 1: 
            total_in_COMTRS = parcels_in_COMTRS.AMOUNT_PLANTED.iloc[0]   # if only 1 value, just use that value 
        else:
            acreages_for_each_site_loc = np.zeros([num_parcels, 1])  # empty array for the summed acreage for each parcel (site location)
            for parcel_iter, individual_site in enumerate(parcel_IDs): #goes through the individual sites in the secition 
                specific_parcel = parcels_in_COMTRS.loc[parcels_in_COMTRS.SITE_LOCATION_ID == individual_site] # locates all permits a specific site
                # if specific_parcel.AMOUNT_PLANTED
                try:
                    total_at_site_loc = max(specific_parcel.AMOUNT_PLANTED)  # maximum acreage reported for that SITE_LOCATION_ID 
                except: 
                    total_at_site_loc = 0 
                    print(f'No value for amount planted at COMTRS {COMTRS_value} at parcel {individual_site}')

                # commented these back in
                # if pd.isnull(individual_site) == True or individual_site == np.nan:   # If site_ID is not labelled
                #     total_at_site_loc = sum(specific_parcel.AMOUNT_PLANTED.unique()) # sum up all unique area values
                acreages_for_each_site_loc[parcel_iter] = total_at_site_loc
                total_in_COMTRS = sum(acreages_for_each_site_loc)
                    # pdb.set_trace()

        # pdb.set_trace()
        if np.size(parcels_in_COMTRS.COUNTY_NAME) >= 1:
            COMTRS_county = parcels_in_COMTRS.COUNTY_NAME.reset_index().COUNTY_NAME[0]  # FIX THIS 
        else:
            COMTRS_county = 'unknown due to no matching COMTRS'
            print('skipped due to no matching COMTRS')
            total_skipped = total_skipped + 1 
            total_in_COMTRS = 0 
        # pdb.set_trace()
        if COMTRS_county == 'TULARE' and total_in_COMTRS > 0:
                crop_acres_tulare = crop_acres_tulare + total_in_COMTRS

        crop_acres_list[COMTRS_iter] = total_in_COMTRS
        # COMTRS_iter = COMTRS_iter + 1 

    crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 

    # crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']

    save_acres = 1     # Saves each crop's data for each COMTRS 
    if save_acres == 1:
        crop3_df = crop2_df.reset_index()
        crop3_df.columns = ['COMTRS', crop_column]
        directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', str(year) + 'files' )
        try: 
            crop3_df.to_csv(os.path.join(directory, (str(year) + crop_column + '_by_COMTRS'+ '.csv' ) ), header = True, na_rep = '0', index = False)   
        except: 
            os.mkdir(directory) 
            crop3_df.to_csv(os.path.join(directory, (str(year) + crop_column + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False)
    return crop2_df, directory, crop_column, crop_iter, crop_acres_tulare


def save_overall_dataframe(crop4_df, directory, year):
    crop5_df = crop4_df.reset_index()
    path_name = os.path.join(directory, (str(year) + '_all_crops_compiled.csv')) 
    crop5_df.to_csv( path_name, header = True, na_rep = '0', index = False)
    print(f'Saved compiled {year} data in {path_name}')


def calPIP_summed(year): 
    """enter year for desired data compilation, run for that year"""

    crop_list, calPIP_data = read_data(year)  # read calPIP data for given year 
    column_list = clean_columns(crop_list)         # clean column names - remove slashes and spaces 
    crop4_df, tulare_overall_by_crop = make_dataframe(year, calPIP_data, column_list, crop_list)    # make dataframe for the crop acreage summations     
    
    # pdb.set_trace()

    crop_iter = 0 
    for crop_type in tqdm(crop_list):  # Runs for each crop type in calPIP database, then connects to larger calPIP array using COMTRS index 
        crop2_df, directory, crop_column, crop_iter, crop_acres_tulare = acreage_compiler(year, crop_type, crop_iter, column_list, calPIP_data)  # sum up acreages for each crop type 
        crop4_df[crop_column] = crop2_df[crop_column].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 
        tulare_overall_by_crop[crop_column] = crop_acres_tulare
        # pdb.set_trace()

    save_overall_dataframe(crop4_df, directory, year)

    tulare_overall_by_crop = tulare_overall_by_crop.transpose()
    tulare_overall_by_crop = tulare_overall_by_crop.rename(columns=tulare_overall_by_crop.iloc[0])
    tulare_overall_by_crop = tulare_overall_by_crop.reindex(tulare_overall_by_crop.index.drop('year'))

    return tulare_overall_by_crop

def run_full_year_range():
    a = {}
    iter = 0 
    for year2 in tqdm(range(1990,2017)):
        a[year2] = calPIP_summed(year2) 
        if iter > 0: 
            results_all_years = pd.concat([results_all_years, a[year2]], axis=1)
        else: 
            results_all_years = a[year2]

        iter = iter + 1

    results_all_years.to_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results.csv', header = True, na_rep = '0', sep = '\t') 
    return results_all_years

def run_specific_year(year):
    a = {}
    a[year] = calPIP_summed(year)
    results_single_year = a[year] 
    results_single_year.to_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/single_years_results.csv', header = True, na_rep = '0', sep = '\t')
    return results_single_year



pdb.set_trace()
results_single_year = run_specific_year(1990)

# pdb.set_trace()
# results_all_years = run_full_year_range()





pdb.set_trace()


