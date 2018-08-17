### Compile and read PUR formatted data 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import os 
import pdb
import pandas as pd
import seaborn as sns
import re 
from tqdm import tqdm  # for something in tqdm(something something):


def add_comtrs_pre_1990(year): #adds the comtrs as a column # preliminary processing of 1974 - 1989 data
    final_two_digits = str(year)
    final_two_digits = final_two_digits[-2:]

    overall_data = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(final_two_digits) + '.txt'), sep = '\t')
    # pdb.set_trace()
    # tlb_overall_data = overall_data[overall_data.county_cd == 54] 16 15 10

    tlb_county_cds = [10, 15, 16, 54]
    tlb_overall_data = overall_data.loc[(overall_data["county_cd"].isin(tlb_county_cds)) ]


    #COMTRS:
    # COunty, Meridian, Township, Range, Section 
    tlb_county = np.int64(tlb_overall_data.county_cd)
    tlb_overall_data.county_cd = tlb_county

    tlb_overall_data = tlb_overall_data[~tlb_overall_data['township'].isnull()]
    tlb_township = np.int64(tlb_overall_data.township)
    tlb_overall_data.township = tlb_township
    # pdb.set_trace()
    try:
        tlb_range = np.int64(tlb_overall_data.range)
        # tlb_range = np.int64(tlb_overall_data.range)
    except:
        # pdb.set_trace()
        test = np.array(tlb_overall_data.range)
        test2 = test.tolist()
        where_are_NaNs = np.isnan(test2)
        test3 = tlb_overall_data.range
        test3[where_are_NaNs] = 99
        tlb_range = np.int64(test3)
    tlb_overall_data.range = tlb_range

    tlb_section = np.int64(tlb_overall_data.section)
    tlb_overall_data.section = tlb_section
    # pdb.set_trace()

    len_dataset = len(tlb_overall_data.section)
    COMTRS = pd.DataFrame()
    COMTRS2 = np.zeros(len_dataset)
    COMTRS['comtrs'] = COMTRS2
    tlb_overall_data['comtrs'] = np.zeros((len_dataset))

    array_township = tlb_overall_data.township.values 
    string_list_township = [str(item).zfill(2) for item in array_township]
    tlb_overall_data["township_string"] = string_list_township

    array_range = tlb_overall_data.range.values 
    string_list_range = [str(item).zfill(2) for item in array_range]
    tlb_overall_data["range_string"] = string_list_range

    array_section = tlb_overall_data.section.values
    string_list_section = [str(item).zfill(2) for item in array_section]
    tlb_overall_data["section_string"] = string_list_section

    # pdb.set_trace()
    print('fix base line meridian here')
    # Replace "H" with "M" since this is clearly not using the Humbolt Meridian, but the Mount Diable meridian 
    # undone since this just exacerbated the problem 
    # tlb_overall_data.base_ln_mer = tlb_overall_data.base_ln_mer.replace('H', 'M')
    tlb_overall_data["base_ln_mer"]
    pdb.set_trace()
    tlb_overall_data["comtrs"] = (tlb_overall_data["county_cd"].map(str) + tlb_overall_data["base_ln_mer"] + tlb_overall_data["township_string"]  + tlb_overall_data["tship_dir"] + tlb_overall_data["range_string"] + tlb_overall_data["range_dir"] + tlb_overall_data["section_string"])

    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = False )
    # pdb.set_trace()


def add_comtrs_1990_2004(year): #adds the comtrs as a column # preliminary processing of 1990 - 2004 data
    final_two_digits = str(year)
    final_two_digits = final_two_digits[-2:]
    # pdb.set_trace()
    # Extract data from counties 10, 15, 16, 54
    overall_data_fresno = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_10_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kern = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_15_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kings = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_16_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_tulare = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_54_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)

    full_dataset = [overall_data_fresno, overall_data_kern, overall_data_kings, overall_data_tulare]

    for dataset_num, dataset in tqdm(enumerate(full_dataset)):
        print(len(dataset))
        # pdb.set_trace()
        tlb_county = np.int64(dataset.county_cd)
        dataset.county_cd = tlb_county

        dataset = dataset[~dataset['township'].isnull()]
        try: # fix township
            tlb_township = np.int64(dataset.township)
        except:
            # pdb.set_trace()
            number_exceptions = 0 
            tlb_township = np.zeros(len(dataset.township))
            for township_num, township in enumerate(dataset.township):
                try:
                    township = np.int64(township)
                    tlb_township[township_num] = township
                except:
                    number_exceptions = number_exceptions + 1
                    print(township)
                    print(number_exceptions)
                    tlb_township[township_num] = 99
        dataset.township = np.int64(tlb_township)    # added this in to round the numbers and remove decimals 

        try: # fix range
            tlb_range = np.int64(dataset.range)
            # tlb_range = np.int64(tlb_overall_data.range)
        except:
            # pdb.set_trace()
            number_exceptions = 0 
            tlb_range = np.zeros(len(dataset.range))
            for range_num, range_val in enumerate(dataset.range):
                try:
                    range_val = np.int64(range_val)
                    tlb_range[range_num] = range_val
                except:
                    number_exceptions = number_exceptions + 1
                    print(range_val)
                    print(number_exceptions)
                    tlb_range[range_num] = 99

        dataset.range = np.int64(tlb_range)

        try:  # Fix sections
            tlb_section = np.int64(dataset.section)
            # tlb_range = np.int64(tlb_overall_data.range)
        except:
            # pdb.set_trace()
            number_exceptions = 0 
            tlb_section = np.zeros(len(dataset.section))
            for section_num, section_val in enumerate(dataset.section):
                try:
                    section_val = np.int64(section_val)
                    tlb_section[section_num] = section_val
                except:
                    number_exceptions = number_exceptions + 1
                    print(section_val)
                    print(number_exceptions)
                    tlb_section[section_num] = 99


        # tlb_section = np.int64(dataset.section)
        dataset.section = np.int64(tlb_section)


        len_dataset = len(dataset.section)
        COMTRS = pd.DataFrame()
        COMTRS2 = np.zeros(len_dataset)
        COMTRS['comtrs'] = COMTRS2
        dataset['comtrs'] = np.zeros((len_dataset))


        # pdb.set_trace()

        try:
            array_township = dataset.township.values 
            string_list_township = [str(item).zfill(2) for item in array_township]
            dataset["township_string"] = string_list_township

            array_range = dataset.range.values 
            string_list_range = [str(item).zfill(2) for item in array_range]
            dataset["range_string"] = string_list_range

            array_section = dataset.section.values
            string_list_section = [str(item).zfill(2) for item in array_section]
            dataset["section_string"] = string_list_section

        except:
            print('error here')

        # pdb.set_trace()

        dataset["comtrs"] = (dataset["county_cd"].map(str) + dataset["base_ln_mer"] + dataset["township_string"]  + dataset["tship_dir"] + dataset["range_string"] + dataset["range_dir"] + dataset["section_string"])
        dataset = dataset.set_index(['comtrs'])
                # pdb.set_trace()
        if dataset_num == 0:
            tlb_overall_data = dataset
        else:
            # pdb.set_trace()
            # merge these 4 datasets together, run a function similar to calculate_acres_pre_1990(), output should be acres in each comtrs for each crop type (site_code)
            tlb_overall_data = pd.concat([tlb_overall_data, dataset])
        # pdb.set_trace()

    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = True )


def add_comtrs_2005_2016(year): #adds the comtrs as a column # preliminary processing of 2004 - 2016 data
    '''relatively simple since this dataset already includes the comtrs'''
    final_two_digits = str(year)
    final_two_digits = final_two_digits[-2:]
    # pdb.set_trace()
    # Extract data from counties 10, 15, 16, 54
    overall_data_fresno = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_10_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kern = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_15_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kings = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_16_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_tulare = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/pur' + str(year) +'/udc' + final_two_digits + '_54_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)

    full_dataset = [overall_data_fresno, overall_data_kern, overall_data_kings, overall_data_tulare]

    for dataset_num, dataset in tqdm(enumerate(full_dataset)):
        if dataset_num == 0:
            tlb_overall_data = dataset
        else:
            # pdb.set_trace()
            tlb_overall_data = pd.concat([tlb_overall_data, dataset])
    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = True )


def read_data(year):

    directory='/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/data_with_comtrs'
    tlb_overall_data = pd.read_csv(os.path.join(directory, str('comtrs_pur_vals_year' + str(year) + '.csv') ) )

    if year < 1990:
        tlb_overall_data.acre_unit_treated = tlb_overall_data.acre_unit_treated.values / 100 # divide by 100 since original database does not include decimal point
        crop_list = np.int64(tlb_overall_data.commodity_code.unique())

    if year > 1989:
        crop_list = np.int64(tlb_overall_data.site_code.unique())

    return crop_list, tlb_overall_data

def make_dataframe(year, tlb_overall_data, crop_list): # Build empty dataframe for the crop acreage summations 
    
    all_COMTRS = tlb_overall_data.comtrs.unique()
    array_zeros1 = np.full((len(all_COMTRS), len(crop_list)), 0) #array of zeros for dataset
    crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ crop_list ] )   # makes overall dataframe for all crop types 
    array_tulare = np.full((1, 1), 0)
    tulare_overall_by_crop = pd.DataFrame(array_tulare, columns = ['year'])
    # pdb.set_trace()
    tulare_overall_by_crop['year'] = year 
    # pdb.set_trace()
    return crop4_df, tulare_overall_by_crop  #returns framework for the compiled crop types by comtrs, and tulare_overall_by_crop (to be used later)


def calculate_acres_pre_1990(year, crop_type, crop_iter, crop_list, tlb_overall_data): # for a given set of comtrs, calculate total tree crop acreage 

    crop_type_vals = tlb_overall_data.loc[lambda df: tlb_overall_data.commodity_code == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
    # no_reg_firm_IDs = len(crop_type_vals.reg_firm_no.unique()) # number of registration firms for a specific crop 
    ## ^ Edit location ID search - test for different SITE_LOCATION_ID
    # number_of_null_site_location_ids = sum(pd.isnull(crop_type_vals.reg_firm_no))

    COMTRS_list = crop_type_vals.comtrs.unique()
    no_COMTRS = len(crop_type_vals.comtrs.unique())   # number of unique COMTRS that grow specific crop 
    
    crop_column = crop_list[crop_iter]
    crop_iter = crop_iter + 1
    crop_acres_tulare = 0 # reset crop acreage to zero 

    save_crop_file = 1 
    if save_crop_file == 1:
        # path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        # directory_overall_folder 
        if os.path.isdir("/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26"):
            print('folder does exist')
        else:
            os.mkdir('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26')
            print('Created calPIP_crop_acreages folder')

    array_zeros = np.zeros([no_COMTRS, 1])  # array of the length of COMTRS for alfalfa
    crop2_df = pd.DataFrame(array_zeros, index = [COMTRS_list], columns = [str(crop_column)] )   # change column label to each type of crop 
    # COMTRS_iter = 0 
    crop_acres_list = np.zeros([no_COMTRS, 1])
    # pdb.set_trace()

    for COMTRS_iter, COMTRS_value in enumerate(tqdm(COMTRS_list)): 
        # pdb.set_trace()
        everything_in_this_comtrs = crop_type_vals.loc[crop_type_vals['comtrs'] == COMTRS_value, :]  # filters by fields in this specific COMTRS section 

        batch_IDs = everything_in_this_comtrs.batch_no.unique()  # array of unique batch registration values in section
        num_batches = len(batch_IDs)   # number of parcels within the COMTRS

        acreages_for_each_batch = np.zeros([num_batches, 1])  # empty array for the summed acreage for each parcel (site location)
        for batch_num, individual_batch in enumerate(batch_IDs): #goes through the individual sites in the secition 
            specific_registrant = everything_in_this_comtrs.loc[everything_in_this_comtrs.batch_no == individual_batch] # locates all permits a specific site
            # pdb.set_trace()
            # if specific_parcel.acre_unit_treated
            try:
                total_at_this_batch = max(specific_registrant.acre_unit_treated)  # maximum acreage reported for that SITE_LOCATION_ID 
            except: 
                total_at_this_batch = 0 
                print(f'No value for amount planted at COMTRS {COMTRS_value} at registrant {individual_batch}')

            # commented these back in
            # if pd.isnull(individual_site) == True or individual_site == np.nan:   # If site_ID is not labelled
            #     total_at_site_loc = sum(specific_parcel.AMOUNT_PLANTED.unique()) # sum up all unique area values
            acreages_for_each_batch[batch_num] = total_at_this_batch
            total_in_COMTRS = sum(acreages_for_each_batch)
                # pdb.set_trace()

        crop_acres_list[COMTRS_iter] = total_in_COMTRS  #puts all of this crop for this comtrs in the crop_acres_list
    
    try:
        # crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop # risk of misassigning
        crop_type_string = str(crop_type)
        crop2_df[crop_type_string] = crop_acres_list   #tried this method instead so nothing gets misassigned 
        # crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']
        # pdb.set_trace()

        save_acres = 1     # Saves each crop's data for each COMTRS 
        if save_acres == 1:
            crop3_df = crop2_df.reset_index()
            crop3_df.columns = ['COMTRS', crop_column]
            year_string = str(year) 
            year_two_digits = year_string[-2:]
            # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages', str(year) + 'files' )
            directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )
            # try: 
            #     crop3_df.to_csv(os.path.join(directory, (year_two_digits + 'crop' + str(crop_column) + '_by_COMTRS'+ '.csv' ) ), header = True, na_rep = '0', index = False)   
            #     # pdb.set_trace()
            # except: 
            #     os.mkdir(directory) 
            #     crop3_df.to_csv(os.path.join(directory, (year_two_digits + 'crop' + str(crop_column) + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False)

            # comtrs_with_crop
    except:
        print('crop2_df make have been empty for this crop type')
    return crop2_df, directory, crop_column, crop_iter, crop_acres_tulare

def calculate_acres_1990_2016(year, crop_type, crop_iter, crop_list, tlb_overall_data): # for a given set of comtrs, calculate total tree crop acreage
    # overall_data = pd.read_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results.csv', sep = '\t', index_col =0) 

    # total_skipped = 0 
    # calPIP_data
    crop_type_vals = tlb_overall_data.loc[lambda df: tlb_overall_data.site_code == crop_type, : ]  # pulls permits for each of the crop types (filters for only this crop)
    # pdb.set_trace()
    print('Paused here in calculate_acres_1990_2016')
    # no_reg_firm_IDs = len(crop_type_vals.reg_firm_no.unique()) # number of registration firms for a specific crop 
    ## ^ Edit location ID search - test for different SITE_LOCATION_ID
    # number_of_null_site_location_ids = sum(pd.isnull(crop_type_vals.reg_firm_no))

    COMTRS_list = crop_type_vals.comtrs.unique()
    no_COMTRS = len(crop_type_vals.comtrs.unique())   # number of unique COMTRS that grow specific crop 
    
    crop_column = crop_list[crop_iter]
    crop_iter = crop_iter + 1
    crop_acres_tulare = 0 # reset crop acreage to zero 
    # pdb.set_trace()

    save_crop_file = 1 
    if save_crop_file == 1:
        # path='/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages'
        # directory_overall_folder 
        if os.path.isdir("/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26"):
            print('folder does exist')
        else:
            os.mkdir('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26')
            print('Created calPIP_crop_acreages folder')

    array_zeros = np.zeros([no_COMTRS, 1])  # array of the length of COMTRS for alfalfa
    crop2_df = pd.DataFrame(array_zeros, index = [COMTRS_list], columns = [str(crop_column)] )   # change column label to each type of crop 
    # COMTRS_iter = 0 
    crop_acres_list = np.zeros([no_COMTRS, 1])
    # pdb.set_trace()

    for COMTRS_iter, COMTRS_value in enumerate(tqdm(COMTRS_list)): 
        # pdb.set_trace()
        everything_in_this_comtrs = crop_type_vals.loc[crop_type_vals['comtrs'] == COMTRS_value, :]  # filters by fields in this specific COMTRS section 

        site_loc_IDs = everything_in_this_comtrs.site_loc_id.unique()  # array of unique batch registration values in section
        num_site_loc_IDs = len(site_loc_IDs)   # number of parcels within the COMTRS

        acreages_for_each_site_loc_id = np.zeros([num_site_loc_IDs, 1])  # empty array for the summed acreage for each parcel (site location)
        for loc_id_num, individual_batch in enumerate(site_loc_IDs): #goes through the individual sites in the secition 
            specific_registrant = everything_in_this_comtrs.loc[everything_in_this_comtrs.site_loc_id == individual_batch] # locates all permits a specific site
            # pdb.set_trace()
            # if specific_parcel.acre_planted
            try:
                total_at_this_site_loc = max(specific_registrant.acre_planted)  # maximum acreage reported for that SITE_LOCATION_ID 
            except: 
                total_at_this_site_loc = 0 
                print(f'No value for amount planted at COMTRS {COMTRS_value} at registrant {individual_batch}')

            # commented these back in
            # if pd.isnull(individual_site) == True or individual_site == np.nan:   # If site_ID is not labelled
            #     total_at_site_loc = sum(specific_parcel.AMOUNT_PLANTED.unique()) # sum up all unique area values
            acreages_for_each_site_loc_id[loc_id_num] = total_at_this_site_loc
            total_in_COMTRS = sum(acreages_for_each_site_loc_id)
                # pdb.set_trace()

        crop_acres_list[COMTRS_iter] = total_in_COMTRS  #puts all of this crop for this comtrs in the crop_acres_list
    
    # pdb.set_trace()
    print('This point was reached yay')

    try:
        # crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop # risk of misassignment 
        crop_type_string = str(crop_type)
        crop2_df[crop_type_string] = crop_acres_list   #tried this method instead so nothing gets misassigned 
        # crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']
        # pdb.set_trace()
  
        if save_crop_file == 1:  # Saves each crop's data for each COMTRS 
            crop3_df = crop2_df.reset_index()
            crop3_df.columns = ['COMTRS', crop_column]
            year_string = str(year) 
            year_two_digits = year_string[-2:]
            # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages', str(year) + 'files' )
            # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )
            # try: 
            #     crop3_df.to_csv(os.path.join(directory, (year_two_digits + 'crop' + str(crop_column) + '_by_COMTRS'+ '.csv' ) ), header = True, na_rep = '0', index = False)   
            #     # pdb.set_trace()
            # except: 
            #     os.mkdir(directory) 
            #     crop3_df.to_csv(os.path.join(directory, (year_two_digits + 'crop' + str(crop_column) + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False)

            # comtrs_with_crop
    except:
        print('crop2_df may have been empty for this crop type')

    # pdb.set_trace()
    return crop2_df, crop_column, crop_iter, crop_acres_tulare


def compile_data_by_comtrs(year): 
    '''Compiles 1974 - 2016 data by comtrs'''
    print(f'Starting comtrs compilation of year {year}')
    crop_list, tlb_overall_data = read_data(year)
    # pdb.set_trace()
    # print('check tlb_overall_data here')
    crop4_df, tulare_overall_by_crop = make_dataframe(year, tlb_overall_data, crop_list)    # make dataframe for the crop acreage summations     
    # pdb.set_trace()
    crop_iter = 0 
    if year < 1990:
        for crop_type in tqdm(crop_list):  # Runs for each crop type in calPIP database, then connects to larger calPIP array using COMTRS index 
            try:
                # deleted variable directory - hopefully this solves it!!! 
                crop2_df, directory, crop_column, crop_iter, crop_acres_tulare = calculate_acres_pre_1990(year, crop_type, crop_iter, crop_list, tlb_overall_data)  # sum up acreages for each crop type 
                # pdb.set_trace()
                crop4_df[crop_column] = crop2_df[str(crop_column)].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 
                # tulare_overall_by_crop[crop_column] = crop_acres_tulare
            except:
                crop_iter = crop_iter + 1 
                print(f'crop2 dataframe may have been empty for this crop type number {crop_type}')
    if year > 1989:
        for crop_type in tqdm(crop_list):  # Runs for each crop type in calPIP database, then connects to larger calPIP array using COMTRS index 
            try:
                # pdb.set_trace()
                # print('run this by hand')
                crop2_df, crop_column, crop_iter, crop_acres_tulare = calculate_acres_1990_2016(year, crop_type, crop_iter, crop_list, tlb_overall_data)  # sum up acreages for each crop type 
                print('This never gets printed so idt it''s working')
                # pdb.set_trace()
                crop4_df[crop_column] = crop2_df[str(crop_column)].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 
                # tulare_overall_by_crop[crop_column] = crop_acres_tulare
                print(f'crop2 dataframe EXISTS for crop type number {crop_type}') 
            except:
                crop_iter = crop_iter + 1 
                print(f'crop2 dataframe may have been empty for this crop type number {crop_type}')    
    
    crop5_df = crop4_df.reset_index()
    year_string = str(year) 
    year_two_digits = year_string[-2:]
    directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )
    try:
        crop5_df.to_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False, sep = '\t')
    except:
        os.mkdir(directory)
        crop5_df.to_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False, sep = '\t')

    # pdb.set_trace()
    # crop3_df.to_csv(os.path.join(directory, (str(year) + 'crop' + str(crop_column) + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False)


def retrieve_data_for_irrigation_district(irrigation_district, normalized):

    irrigation_district_data = os.path.join('~/Box Sync/herman_research_box/tulare_git_repo/irrigation_districts_with_comtrs', irrigation_district + '.csv')
    try:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['co_mtrs'])
    except:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['CO_MTRS']) 

    crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1974,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    # crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    crop_list_normalized = [ 'year', 'all_tree_crops_normalized', 'all_annual_crops', 'all_crops', 'percent_tree_crops']
    df_shape_normalized = (len(range(1974,2017)), len(crop_list_normalized))
    zero_fillers_normalized = np.zeros(df_shape_normalized)
    sum_crop_types_normalized = pd.DataFrame(zero_fillers_normalized, columns = [ crop_list_normalized ] )

    codes_pre_1990 = pd.read_csv('~/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26/site_codes_with_crop_types.csv', usecols = ['site_code_pre_1990', 'site_name_pre_1990', 'is_orchard_crop_pre_1990', 'is_annual_crop_pre_1990']) # , index_col = 0)
    codes_1990_2016 = pd.read_csv('~/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26/site_codes_with_crop_types.csv', usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016']) #, index_col = 0)
    # # as shown on table 'sites_1990-2016' from PUR downloaded dataset 

    tree_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_orchard_crop_pre_1990 == 1]
    # tree_crops_pre_1990_list = tree_crops_pre_1990.values.tolist()
    tree_crops_pre_1990 = [str(i) for i in tree_crops_pre_1990]

    tree_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_orchard_crop_1990_2016 == 1]
    tree_crops_1990_2016_list = tree_crops_1990_2016.values.tolist()
    tree_crops_1990_2016 = [str(round(i)) for i in tree_crops_1990_2016_list]
    # pdb.set_trace()


    annual_crops_pre_1990 = codes_pre_1990.site_code_pre_1990.loc[codes_pre_1990.is_annual_crop_pre_1990 == 1]
    annual_crops_pre_1990 = [str(i) for i in annual_crops_pre_1990]

    annual_crops_1990_2016 = codes_1990_2016.site_code_1990_2016.loc[codes_1990_2016.is_annual_crop_1990_2016 == 1]
    annual_crops_1990_2016_list = annual_crops_1990_2016.values.tolist()
    annual_crops_1990_2016 = [str(round(i)) for i in annual_crops_1990_2016_list]

    # all_crops_1990_2016 = [tree_crops_1990_2016_list, annual_crops_1990_2016_list]

    test = [tree_crops_1990_2016_list + annual_crops_1990_2016_list]
    test1 = test[0]
    all_crops_1990_2016 = [str(round(i)) for i in test1]


    test = [tree_crops_pre_1990 + annual_crops_pre_1990]
    all_crops_pre_1990 = test[0]

    for df_row, year in tqdm(enumerate(range(1974,2017))):    # editted here to include up to 2016 
        print(f'Compiling and normalizing the data into different crop types for year {year}')
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        year_date_time = pd.to_datetime(year, format='%Y')
        directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )

        # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_data_raw/data_with_comtrs/')
        comtrs_compiled_data = pd.read_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' )), sep = '\t')
        # pdb.set_trace()
        # print('find county column here')
        try:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["level_0"].isin(comtrs_in_irrigation_dist.co_mtrs)) ]
        except:
            crop_data_in_irrigation_district = comtrs_compiled_data.loc[(comtrs_compiled_data["level_0"].isin(comtrs_in_irrigation_dist.CO_MTRS)) ]
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.rename(columns = {"level_0": "comtrs"}) 
        crop_data_in_irrigation_district = crop_data_in_irrigation_district.set_index('comtrs')

        # pdb.set_trace()

        if year < 1990:
            # teset = str(tree_crops_pre_1990)
            # tree_crops_pre_1990 = np.reshape(tree_crops_pre_1990, (len(tree_crops_pre_1990), 1))
            # tree_crops_pre_1990 = tree_crops_pre_1990.tolist()
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_pre_1990)]  # Columns that are tree crops 
            annual_crop_columns =  crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_pre_1990)]
            print(tree_crop_columns)

            
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_pre_1990)] 

            sum_alfalfa = sum(crop_data_in_irrigation_district['3101'])
            sum_nectarine = sum(crop_data_in_irrigation_district['2303'])
        else: # year 1990 - 2016
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_1990_2016)]  # Columns that are tree crops 
            print(tree_crop_columns)
            annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are annual crops 
            
            all_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(all_crops_1990_2016)]
            # pdb.set_trace()
            # pdb.set_trace()
            sum_alfalfa = sum(crop_data_in_irrigation_district['23001'])
            sum_nectarine = sum(crop_data_in_irrigation_district['5003'])        

        tree_data = crop_data_in_irrigation_district[tree_crop_columns]
        tree_crop_acreage_by_fruit_type = tree_data[tree_crop_columns].sum()
        acreage_of_all_tree_crops = tree_data[tree_crop_columns].sum().sum()
        # pdb.set_trace()

        annual_data = crop_data_in_irrigation_district[annual_crop_columns]
        annual_acreage_by_annual_crop_type = annual_data[annual_crop_columns].sum()
        acreage_of_all_annual_crops = annual_data[annual_crop_columns].sum().sum()
        acreage_of_all_crops = acreage_of_all_tree_crops + acreage_of_all_annual_crops

        sum_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_crop_types.iloc[df_row]['alfalfa'] = str(sum_alfalfa)
        sum_crop_types.iloc[df_row]['all_tree_crops'] = str(acreage_of_all_tree_crops)
        sum_crop_types.iloc[df_row]['all_annual_crops'] = str(acreage_of_all_annual_crops)
        sum_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)
        sum_crop_types.iloc[df_row]['percent_tree_crops'] = str(acreage_of_all_tree_crops / acreage_of_all_crops * 100)
        sum_crop_types.set_index('year')
        # pdb.set_trace()

        ### Normalizing Next steps: 
        # for each comtrs value, find the total number of acres (sum for all crop types)
        # multiply each value in the section by (640 / comtrs total)
        # carry on 

        if normalized == 1:
            all_crop_data = crop_data_in_irrigation_district[all_crop_columns]
            print('normalizing the above ammounts so that the total acreage across crop types for each comtrs is not above 640 acres')
            acreage_each_comtrs = all_crop_data.sum(axis = 1)
            all_crop_data_normalized = all_crop_data  # start normalized dataframe 

            number_of_skips = 0 

            for num, comtrs in enumerate(tqdm(all_crop_data_normalized.index)):
                # pdb.set_trace()
                if all_crop_data.loc[comtrs].sum() > 640:
                    # pdb.set_trace()
                    all_crop_data_normalized.loc[comtrs] = all_crop_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]
                    # pdb.set_trace()
                    # tree_data_normalized.loc[comtrs] =  tree_data_normalized.loc[comtrs] * 640 / acreage_each_comtrs.loc[comtrs]    
                else: 
                    number_of_skips = number_of_skips + 1 

            # pdb.set_trace()
            tree_data_normalized = all_crop_data_normalized[tree_crop_columns]
            annual_data_normalized = all_crop_data_normalized[annual_crop_columns]
            # pdb.set_trace()

            acreage_of_all_tree_crops_normalized = tree_data_normalized[tree_crop_columns].sum().sum()
            acreage_of_all_annual_crops_normalized = annual_data_normalized[annual_crop_columns].sum().sum()
            acreage_of_all_crops_normalized = acreage_of_all_tree_crops_normalized + acreage_of_all_annual_crops_normalized

            sum_crop_types_normalized.iloc[df_row]['year'] = year_date_time.year 
            sum_crop_types_normalized.iloc[df_row]['all_tree_crops_normalized'] = str(acreage_of_all_tree_crops_normalized)
            sum_crop_types_normalized.iloc[df_row]['all_annual_crops'] = str(acreage_of_all_annual_crops_normalized)
            sum_crop_types_normalized.iloc[df_row]['all_crops'] = str(acreage_of_all_crops_normalized)     
            sum_crop_types_normalized.iloc[df_row]['percent_tree_crops'] = str(acreage_of_all_tree_crops_normalized / acreage_of_all_crops_normalized * 100)
            sum_crop_types_normalized.set_index('year')
        else:
            sum_crop_types_normalized = 'not normalized'


    sum_crop_types.to_csv(str('calPUR_data' + str(irrigation_district) + '.csv'), index = False) 
    if normalized == 1:
        sum_crop_types_normalized.to_csv(str('calPUR_data_normalized' + str(irrigation_district) + '.csv'), index = False) 

    # pdb.set_trace()
    return sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district


def county_commissioner_data(irrigation_district):
    county_name = irrigation_district.split('_')[0]

    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df_all = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df_all[df_all.county==county_name]

    # first: what crops are highest value total (top 10 in 2016)
    print(df[df.index=='2016'].sort_values(by='value', ascending=False).head(10))
    highest_valued = df[df.index=='2016'].sort_values(by='value', ascending=False).head(10)
    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))
    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    df_tulare = df_all[df_all.county=='Tulare']
    df_kern = df_all[df_all.county=='Kern']
    df_kings = df_all[df_all.county=='Kings']
    df_fresno = df_all[df_all.county=='Fresno']

    county_commissioner_codes = pd.read_csv('~/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26/county_commissioner_crop_types.csv') 
    tree_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_orchard_crop == 1]
    annual_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_annual_crop == 1]
    forage_crops_cc = county_commissioner_codes.site_code_cc.loc[county_commissioner_codes.is_forage_crop == 1]

    crop_list = ['year', 'all_tree_crops', 'all_annual_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1980,2017)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_cc_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    for df_row, year in tqdm(enumerate(range(1980,2017))):
        year_date_time = pd.to_datetime(year, format='%Y')
        df_this_year = df[df.index == str(year) ]
        df_real_acreages_only = df_this_year[df_this_year.acres > 0 ]

        tree_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(tree_crops_cc)]  # Columns that are tree crops 
        annual_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(annual_crops_cc)]  # Columns that are tree crops 
        forage_crops_this_year_this_county = df_real_acreages_only[df_real_acreages_only.crop.isin(forage_crops_cc)]

        tree_crops_this_year = tree_crops_this_year_this_county.acres.sum()
        annual_crops_this_year = annual_crops_this_year_this_county.acres.sum()
        forage_crops_this_year = forage_crops_this_year_this_county.acres.sum()
        # pdb.set_trace()
        acreage_of_all_crops = tree_crops_this_year + annual_crops_this_year + forage_crops_this_year

        sum_cc_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_cc_crop_types.iloc[df_row]['all_tree_crops'] = str(tree_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_annual_crops'] = str(annual_crops_this_year)
        sum_cc_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)

        sum_cc_crop_types.iloc[df_row]['percent_tree_crops'] = str(tree_crops_this_year / acreage_of_all_crops * 100)
        sum_cc_crop_types.set_index('year')
        # pdb.set_trace()

    sum_cc_crop_types.to_csv(str('cc_data' + str(irrigation_district) + '.csv'), index = False) 
        # annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are tree crops 

    return sum_cc_crop_types


############## start of calPIP dataset functions #################

def load_calPIP_data_all_years(irrigation_district):  # loads the data already calculated rather than recalculate it all 
    all = np.load(str(irrigation_district + 'all_crops_compiled_with_crop_types.npy')).item()
    tree_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'tree_acreage_summed_for_year.csv'))
    annual_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'annual_acreage_summed_for_year.csv'))
    forage_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'forage_acreage_summed_for_year.csv'))
    percent_tree_acreage_summed_for_year = np.loadtxt(str(irrigation_district + 'percent_tree_acreage_summed_for_year.csv'))
    # pdb.set_trace()
    return all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year
    # print(read_dictionary['hello']) # displays "world"

def plot_dataset_comparison(irrigation_district, tree_acreage_summed_for_year,annual_acreage_summed_for_year, forage_acreage_summed_for_year, sum_crop_types, sum_cc_crop_types ): 
    year_list_array = np.arange(1990, 2017)
    fig, ax = plt.subplots()
    linestyles = ['-', '--', '-.', ':']
    # add calPIP data 
    ax.plot(year_list_array[1:27], tree_acreage_summed_for_year[1:27], color = 'g', linestyle = ':', label = 'calPIP tree crop acreage')
    ax.plot(year_list_array[1:27], annual_acreage_summed_for_year[1:27], color = 'y', linestyle = ':',  label = 'cal PIP annual crop acreage')
    # ax.plot(year_list_array[1:27], forage_acreage_summed_for_year[1:27], label = 'forage crop acreage')
    ax.set_title(str(irrigation_district + ' Crop Type Changes Dataset Comparison '))
    plt.ylabel('Total acres planted')

    add_droughts = 0 
    if add_droughts == 1 :
        logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
        collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule), facecolor='orange', alpha=0.3)
        ax.add_collection(collection)
        logic_rule2 =  ( (year_list_array < 1995) & (year_list_array > 1990)  )   
        collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=1000000, where=(logic_rule2), facecolor='orange', alpha=0.3)
        ax.add_collection(collection2)

    try:  # works when un-normalized
        # add calPUR data: 
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops.values
        # pdb.set_trace()
        ax.plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage')
    except: # occurs when data is normalized 
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops_normalized.values
        ax.plot(x_vals, y_vals, color = 'g', label = 'calPUR tree crop acreage')

    annual_crop_y_vals = sum_crop_types.all_annual_crops.values
    ax.plot(x_vals, annual_crop_y_vals, color = 'y', label = 'calPUR annual crop acreage')

    # add County Commissioner Data:
    x_vals_cc = sum_cc_crop_types.year.values
    y_vals_tree_cc = sum_cc_crop_types.all_tree_crops.values
    y_vals_annual_cc = sum_cc_crop_types.all_annual_crops.values
    ax.plot(x_vals_cc, y_vals_tree_cc, linestyle = '-.', color = 'g', label = 'County Commissioner tree crop acreage')
    ax.plot(x_vals_cc, y_vals_annual_cc, color = 'y', linestyle = '-.', label = 'County Commissioner annual crop acreage')    

    ax.plot()
    plt.legend()
    plt.show()

############## end of calPIP dataset functions #################


def plot_data_for_irrigation_district(irrigation_district, sum_crop_types, normalized):

    pdb.set_trace()
    if normalized == 0:
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops.values
    if normalized == 1:
        x_vals = sum_crop_types.year.values
        y_vals = sum_crop_types.all_tree_crops_normalized.values

    plt.plot(x_vals, y_vals)
    plt.xlabel('year')
    plt.ylabel('Acres of tree crop')
    plt.title(str(irrigation_district))
    plt.show()

def plot_tree_crop_percentages_for_irrigation_district(irrigation_district, sum_crop_types):
    # pdb.set_trace()
    year_array = np.int64(sum_crop_types.year.values)
    year_array_flattened = year_array.flatten()
    x_vals2 = pd.to_datetime(year_array_flattened, format='%Y')
    y_vals = sum_crop_types.percent_tree_crops.values
    plt.plot(x_vals2, y_vals)
    plt.xlabel('year')
    plt.ylabel('Percentage of calPIP permitted acreage that is tree crop')
    plt.title(str(irrigation_district))
    plt.show()  

# # Step 1: Add the comtrs column (already completed for 1974 - 1989)
# for year in range(1974,1990): 
#     add_comtrs_pre_1990(year)  # preliminary processing of 1974 - 1989 data

# pdb.set_trace()

# year = 1982
# add_comtrs_pre_1990(year)

# pdb.set_trace()
#Step 2: add the comtrs columns to 1990 - 2004 data (already completed for 1990-2002)
# for year in tqdm(range(1990,2005)):  # process post-1989 data by adding 'comtrs' row 
#     add_comtrs_1990_2004(year)
#     print(f'completed adding comtrs for year {year}')

# Step 2, repeated for years 1994 and 1995 since the section data had some glitches
# for year in tqdm(range(2008, 2017)):
#     add_comtrs_1990_2004(year)

# pdb.set_trace()

# add_comtrs_2005_2016(year)
######### MUST COMPILE BY COMTRS OR THIS REALLY WONT WORK ###########
# pdb.set_trace()
# for year in range(1990,2017):
#     compile_data_by_comtrs(year)  # compile 1974 - 1989 data by comtrs   - this is where it really depends how you slice it with the calculate_acreas() fuction
#         # attempted to use this function post 1989 as well - need to fix!!!
# pdb.set_trace()

# for year in tqdm(range(1974, 2017)):
#     compile_data_by_comtrs(year)

# pdb.set_trace()

# # step 3: add the comts from 2005 - 2016 data: 
# for year in range(2006,2017):
#     add_comtrs_2005_2016(year)

# irrigation_district = 'North Kern Water Storage District'
# irrigation_district = 'Dudley Ridge Water District'
# irrigation_district = 'Westlands Water District'

normalized = 1
compare_with_cc_and_pip_data = 1 
#Step 4: extract COMTRS values from a specific irrigation district


# Step 5: save data for a specific region: 
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Tulare_Lake_Basin_Water_Storage_District')
# pdb.set_trace()

# irrigation_district = 'Kings_County'
# irrigation_district = 'Kern_County'

# irrigation_district = 'Fresno_County'
irrigation_district = 'Tulare_County'
# irrigation_district = 'North_Kern_Water_Storage_District'
# irrigation_district = 'Cawelo_Water_District'
# irrigation_district = 'Wasco_Irrigation_District'
# irrigation_district = 'Buena_Vista_Water_Storage_District'

#### Run this to re-extrace data from this specific region:  
sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district(irrigation_district, normalized)

# irrigation_district = 'Tulare_County'
# sum_crop_types, sum_crop_types_normalized, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district(irrigation_district)


# plot_data_for_irrigation_district(irrigation_district, sum_crop_types, normalized)
# plot_tree_crop_percentages_for_irrigation_district(irrigation_district, sum_crop_types)

# Load calPUR dataset 
if normalized == 1:
    sum_crop_types_normalized = pd.read_csv(str('calPUR_data_normalized' + str(irrigation_district) + '.csv'))
else:
    sum_crop_types = pd.read_csv(str('calPUR_data' + str(irrigation_district) + '.csv'))


if compare_with_cc_and_pip_data == 1:
    # Load County Commissioner dataset 
    sum_cc_crop_types = county_commissioner_data(irrigation_district)
    # pdb.set_trace()

    # pdb.set_trace()
    print('go from here')
    # Load calPIP dataset 
    (all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, 
        percent_tree_acreage_summed_for_year) = load_calPIP_data_all_years(irrigation_district)

    # Plot combination of datasets: 
    if normalized == 1:
        plot_dataset_comparison(irrigation_district, tree_acreage_summed_for_year,annual_acreage_summed_for_year, forage_acreage_summed_for_year, sum_crop_types_normalized, sum_cc_crop_types )
    else:    
        plot_dataset_comparison(irrigation_district, tree_acreage_summed_for_year,annual_acreage_summed_for_year, forage_acreage_summed_for_year, sum_crop_types, sum_cc_crop_types )



if compare_with_cc_and_pip_data == 0: 
    # pdb.set_trace()
    if normalized == 1:
        plot_data_for_irrigation_district(irrigation_district, sum_crop_types_normalized, normalized)
    if normalized == 0:
        plot_data_for_irrigation_district(irrigation_district, sum_crop_types, normalized)





pdb.set_trace()