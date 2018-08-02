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
# from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):


def add_comtrs(year): #adds the comtrs as a column # preliminary processing of 1974 - 1989 data

    overall_data = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) + '.txt'), sep = '\t')
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
    # for comtrs in range(len(tlb_overall_data)): 
    # pdb.set_trace()

    for num in tqdm(range(len_dataset)): 

        if (np.isreal(tlb_section[num]) and np.isreal(tlb_range[num]) and np.isreal(tlb_township[num])
            and np.absolute(tlb_section[num]) > - 50 and np.abs(tlb_range[num]) > - 50 and np.abs(tlb_township[num]) > -50) :

            tlb_overall_data.section.iloc[num] = str(tlb_section[num]).zfill(2)  #ensures section data is 2 characters long
            tlb_overall_data.range.iloc[num] = str(tlb_range[num]).zfill(2)  #ensures section data is 2 characters long
            tlb_overall_data.township.iloc[num] = str(tlb_township[num]).zfill(2)  #ensures section data is 2 characters long

            fields = (str(tlb_overall_data.county_cd.iloc[num]), str(tlb_overall_data.base_ln_mer.iloc[num]) 
                , str(tlb_overall_data.township.iloc[num]) , str(tlb_overall_data.tship_dir.iloc[num]) 
                , str(tlb_overall_data.range.iloc[num]) , str(tlb_overall_data.range_dir.iloc[num]) , str(tlb_overall_data.section.iloc[num])  )
            # pdb.set_trace()
            # test = str(tlb_overall_data.county_cd.iloc[num]).join( str(tlb_overall_data.base_ln_mer.iloc[num]) )
            # fields = [ str(tlb_overall_data.county_cd.iloc[num]), tlb_overall_data.base_ln_mer.iloc[num] ]
            # test = ''.join( str(tlb_overall_data.base_ln_mer.iloc[num]), str(tlb_overall_data.county_cd.iloc[num])  )

            tlb_overall_data['comtrs'].iloc[num] = ''.join(fields)
        else:
            tlb_overall_data['comtrs'].iloc[num]  = 'error'
        # tlb_overall_data['comtrs'].iloc[num] = COMTRS.comtrs[num]
    # pdb.set_trace()

    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = False )
    # pdb.set_trace()


def process_post_1989_data(year):#adds the comtrs as a column # preliminary processing of 1990 - 2004 data
    final_two_digits = str(year)
    final_two_digits = final_two_digits[-2:]
    # pdb.set_trace()
    # Extract data from counties 10, 15, 16, 54
    overall_data_fresno = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_10_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kern = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_15_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kings = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_16_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_tulare = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_54_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)

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
        dataset.township = tlb_township

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
        for num in tqdm(range(len_dataset)):   # range(len_dataset)
            if (np.isreal(tlb_section[num]) and np.isreal(tlb_range[num]) and np.isreal(tlb_township[num])
                and np.absolute(tlb_section[num]) > - 50 and np.abs(tlb_range[num]) > - 50 and np.abs(tlb_township[num]) > -50) :

                dataset.section.iloc[num] = str(tlb_section[num]).zfill(2)  #ensures section data is 2 characters long
                dataset.range.iloc[num] = str(tlb_range[num]).zfill(2)  #ensures section data is 2 characters long
                dataset.township.iloc[num] = str(tlb_township[num]).zfill(2)  #ensures section data is 2 characters long

                fields = (str(dataset.county_cd.iloc[num]), str(dataset.base_ln_mer.iloc[num]) 
                    , str(dataset.township.iloc[num]) , str(dataset.tship_dir.iloc[num]) 
                    , str(dataset.range.iloc[num]) , str(dataset.range_dir.iloc[num]) , str(dataset.section.iloc[num])  )
                # pdb.set_trace()
                # test = str(dataset.county_cd.iloc[num]).join( str(dataset.base_ln_mer.iloc[num]) )
                # fields = [ str(dataset.county_cd.iloc[num]), dataset.base_ln_mer.iloc[num] ]
                # test = ''.join( str(dataset.base_ln_mer.iloc[num]), str(dataset.county_cd.iloc[num])  )

                dataset['comtrs'].iloc[num] = ''.join(fields)
            else:
                dataset['comtrs'].iloc[num]  = 'error'
        dataset = dataset.set_index(['comtrs'])

        if dataset_num == 0:
            tlb_overall_data = dataset
        else:
            # pdb.set_trace()
            tlb_overall_data = pd.concat([tlb_overall_data, dataset])
        # pdb.set_trace()


    # pdb.set_trace()
    # pd.to_csv(tlb_overall_data)
    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = True )
    # overall_data_1 = pd.concat([overall_data_fresno, overall_data_kern], axis=1)
    # overall_data_2 = pd.concat([overall_data_kings, overall_data_tulare], axis=1)
    # test = pd.concat([overall_data_1, overall_data_2], axis=1)
    # merge these 4 datasets together, run a function similar to calculate_acres_pre_1990(), output should be acres in each comtrs for each crop type (site_code)


def add_comtrs_2005_2016(year): #adds the comtrs as a column # preliminary processing of 2004 - 2016 data
    '''relatively simple since this dataset already includes the comtrs'''
    final_two_digits = str(year)
    final_two_digits = final_two_digits[-2:]
    # pdb.set_trace()
    # Extract data from counties 10, 15, 16, 54
    overall_data_fresno = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_10_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kern = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_15_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_kings = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_16_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)
    overall_data_tulare = pd.read_csv(str('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/pur' + str(year) +'/udc' + final_two_digits + '_54_fixed.txt'), sep = ',', error_bad_lines = False, warn_bad_lines = True)

    full_dataset = [overall_data_fresno, overall_data_kern, overall_data_kings, overall_data_tulare]

    for dataset_num, dataset in tqdm(enumerate(full_dataset)):
        if dataset_num == 0:
            tlb_overall_data = dataset
        else:
            # pdb.set_trace()
            tlb_overall_data = pd.concat([tlb_overall_data, dataset])
    tlb_overall_data.to_csv(str('comtrs_pur_vals_year' + str(year) + '.csv'), index = True )


def read_data(year):
    if year < 1990:
        # pdb.set_trace()
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        directory='/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/data_with_comtrs'

        # directory = 
        tlb_overall_data = pd.read_csv(os.path.join(directory, str('comtrs_pur_vals_year' + year_two_digits + '.csv') ) )
        # tlb_overall_data = pd.read_csv(str('comtrs_pur_vals_year' + str(year[-2:]) + '.csv') )

        tlb_overall_data.acre_unit_treated = tlb_overall_data.acre_unit_treated.values / 100 # divide by 100 since original database does not include decimal point
            # year_file  = 'calPIP' + str(year) + '.csv'
        # file_name = os.path.join('calPIP_includes_crop_areas', year_file)
        # calPIP_data = pd.read_csv(file_name, sep = '\t')   #Pulls data from CSV file for the year
        crop_list = np.int64(tlb_overall_data.commodity_code.unique())
        # pdb.set_trace()
    if year > 1989:
        # pdb.set_trace()
        # print('stopped year, 1990-2016 in read_data function')
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        directory='/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/data_with_comtrs'
        tlb_overall_data = pd.read_csv(os.path.join(directory, str('comtrs_pur_vals_year' + year_string + '.csv') ) )
        crop_list = np.int64(tlb_overall_data.site_code.unique())
        # pdb.set_trace()
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
    # overall_data = pd.read_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results.csv', sep = '\t', index_col =0) 

    # total_skipped = 0 
    # calPIP_data
    # pdb.set_trace()
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
        if os.path.isdir("/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages"):
            print('folder does exist')
        else:
            os.mkdir('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages')
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
        # if crop_type_vals
        # if num_batches == 1: 
        #     total_in_COMTRS = everything_in_this_comtrs.acre_unit_treated.iloc[0]   # if only 1 value, just use that value 
        # else:
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
        crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 

        # crop_test = crop4_df.loc[crop4_df.index == '10M10S13E34']
        # pdb.set_trace()

        save_acres = 1     # Saves each crop's data for each COMTRS 
        if save_acres == 1:
            crop3_df = crop2_df.reset_index()
            crop3_df.columns = ['COMTRS', crop_column]
            year_string = str(year) 
            year_two_digits = year_string[-2:]
            # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages', str(year) + 'files' )
            directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages', year_two_digits + 'files' )
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
        if os.path.isdir("/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages"):
            print('folder does exist')
        else:
            os.mkdir('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages')
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
        # if crop_type_vals
        # pdb.set_trace()
        # if num_site_loc_IDs == 1: 
        #     total_in_COMTRS = everything_in_this_comtrs.acre_planted.iloc[0]   # if only 1 value, just use that value 
        # else:
        # pdb.set_trace()
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
    
    try:
        crop2_df[lambda crop2_df: crop2_df.columns[0]] = crop_acres_list  # crop acreage list for this specific crop 

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
        print('crop2_df make have been empty for this crop type')
    return crop2_df, directory, crop_column, crop_iter, crop_acres_tulare


def compile_data_by_comtrs(year): 
    '''Compiles 1974 - 1998 data by comtrs'''
    crop_list, tlb_overall_data = read_data(year)
    crop4_df, tulare_overall_by_crop = make_dataframe(year, tlb_overall_data, crop_list)    # make dataframe for the crop acreage summations     

    crop_iter = 0 
    if year < 1990:
        for crop_type in tqdm(crop_list):  # Runs for each crop type in calPIP database, then connects to larger calPIP array using COMTRS index 
            try:
                crop2_df, directory, crop_column, crop_iter, crop_acres_tulare = calculate_acres_pre_1990(year, crop_type, crop_iter, crop_list, tlb_overall_data)  # sum up acreages for each crop type 
                # pdb.set_trace()
                crop4_df[crop_column] = crop2_df[str(crop_column)].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 
                # tulare_overall_by_crop[crop_column] = crop_acres_tulare
            except:
                print(f'crop2 dataframe may have been empty for this crop type number {crop_type}')
    if year > 1989:
        for crop_type in tqdm(crop_list):  # Runs for each crop type in calPIP database, then connects to larger calPIP array using COMTRS index 
            try:
                crop2_df, directory, crop_column, crop_iter, crop_acres_tulare = calculate_acres_1990_2016(year, crop_type, crop_iter, crop_list, tlb_overall_data)  # sum up acreages for each crop type 
                # pdb.set_trace()
                crop4_df[crop_column] = crop2_df[str(crop_column)].loc[crop2_df.index]  # Puts the individual crop acreage list into the overall dataframe crop4_df 
                # tulare_overall_by_crop[crop_column] = crop_acres_tulare
            except:
                print(f'crop2 dataframe may have been empty for this crop type number {crop_type}')    
    # pdb.set_trace()    
    crop5_df = crop4_df.reset_index()
    # test = test.set_index('level_0')
    # test["column"] = test.index.str.replace(",","").astype(object)
    year_string = str(year) 
    year_two_digits = year_string[-2:]
    directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages_july26', year_two_digits + 'files' )
    # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages/pur_pre_1990/data_with_comtrs/')
    try:
        crop5_df.to_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False, sep = '\t')
    except:
        os.mkdir(directory)
        crop5_df.to_csv(os.path.join(directory, ('all_data_year' + year_two_digits + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False, sep = '\t')

    # crop3_df.to_csv(os.path.join(directory, (str(year) + 'crop' + str(crop_column) + '_by_COMTRS' + '.csv' ) ), header = True, na_rep = '0', index = False)

def retrieve_data_for_irrigation_district(irrigation_district):
    irrigation_district_data = os.path.join('~/Box Sync/herman_research_box/tulare_git_repo/irrigation_districts_with_comtrs', irrigation_district + '.csv')
    try:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['co_mtrs'])
    except:
        comtrs_in_irrigation_dist = pd.read_csv(irrigation_district_data, usecols = ['CO_MTRS']) 

    crop_list = ['year', 'alfalfa', 'almonds', 'cotton', 'all_tree_crops', 'all_crops', 'percent_tree_crops' ]
    df_shape = (len(range(1974,2004)), len(crop_list))
    zero_fillers = np.zeros(df_shape)
    sum_crop_types = pd.DataFrame(zero_fillers, columns = [ crop_list ] )

    codes_pre_1990 = pd.read_csv('~/Box Sync/herman_research_box/calPIP_PUR_crop_acreages/site_codes_with_crop_types.csv', usecols = ['site_code_pre_1990', 'site_name_pre_1990', 'is_orchard_crop_pre_1990', 'is_annual_crop_pre_1990']) # , index_col = 0)
    codes_1990_2016 = pd.read_csv('~/Box Sync/herman_research_box/calPIP_PUR_crop_acreages/site_codes_with_crop_types.csv', usecols = ['site_code_1990_2016', 'site_name_1990_2016', 'is_orchard_crop_1990_2016', 'is_annual_crop_1990_2016']) #, index_col = 0)
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


    # pdb.set_trace()
        # crop4_df = pd.DataFrame(array_zeros1, index = [all_COMTRS], columns = [ crop_list ] ) 
    for df_row, year in tqdm(enumerate(range(1974,2004))):
        year_string = str(year) 
        year_two_digits = year_string[-2:]
        year_date_time = pd.to_datetime(year, format='%Y')
        directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_PUR_crop_acreages', year_two_digits + 'files' )

        # directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/tulare_git_repo/pur_pre_1990/data_with_comtrs/')
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
            print(tree_crop_columns)
            # pdb.set_trace()

            annual_crop_columns =  crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_pre_1990)]
            sum_alfalfa = sum(crop_data_in_irrigation_district['3101'])
            sum_nectarine = sum(crop_data_in_irrigation_district['2303'])
        else:
            tree_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(tree_crops_1990_2016)]  # Columns that are tree crops 
            annual_crop_columns = crop_data_in_irrigation_district.columns[crop_data_in_irrigation_district.columns.isin(annual_crops_1990_2016)]  # Columns that are tree crops 
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

        # pdb.set_trace()
        # tlb_overall_data['comtrs'].iloc[num]
        if year == 1977 or year == 1983 or year == 1987:
            print(f'the year is paused at {year}')
            pdb.set_trace()
        sum_crop_types.iloc[df_row]['year'] = year_date_time.year 
        sum_crop_types.iloc[df_row]['alfalfa'] = str(sum_alfalfa)
        sum_crop_types.iloc[df_row]['all_tree_crops'] = str(acreage_of_all_tree_crops)
        sum_crop_types.iloc[df_row]['all_crops'] = str(acreage_of_all_crops)
        sum_crop_types.iloc[df_row]['percent_tree_crops'] = str(acreage_of_all_tree_crops / acreage_of_all_crops * 100)
        sum_crop_types.set_index('year')

        # sum_crop_types.year = pd.to_datetime(sum_crop_types.year, format='%Y')
        # sum_crop_types.year.to_datetime()
        # pdb.set_trace()
        print('check here')


    # pdb.set_trace()
    return sum_crop_types, crop_data_in_irrigation_district, irrigation_district


def load_crop_type_all_year():  # loads (from calPIP dataset 1990-2016) the data already calculated rather than recalculate it all 
    pdb.set_trace()
    all = np.load('all_crops_compiled_with_crop_types.npy').item()
    tree_acreage_summed_for_year = np.loadtxt('tree_acreage_summed_for_year.csv')
    annual_acreage_summed_for_year = np.loadtxt('annual_acreage_summed_for_year.csv')
    forage_acreage_summed_for_year = np.loadtxt('forage_acreage_summed_for_year.csv')
    percent_tree_acreage_summed_for_year = np.loadtxt('percent_tree_acreage_summed_for_year.csv')

    return all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year
    # print(read_dictionary['hello']) # displays "world"



def plot_data_for_irrigation_district(irrigation_district, sum_crop_types):
    x_vals = sum_crop_types.year.values
    y_vals = sum_crop_types.all_tree_crops.values
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

# Step 1: Add the comtrs column (already completed for 1974 - 1989)
# for year in range(75,90): 
#     add_comtrs(year)  # preliminary processing of 1974 - 1989 data
# pdb.set_trace()


# for year in range(1974,2004):
#     compile_data_by_comtrs(year)  # compile 1974 - 1989 data by comtrs   - this is where it really depends how you slice it with the calculate_acreas() fuction
# pdb.set_trace()

#Step 2: add the comtrs columns to 1989 - 2004 data (already completed for 1990-2002)
# for year in tqdm(range(2000,2008)):  # process post-1989 data by adding 'comtrs' row 
#     process_post_1989_data(year)
#     print(f'completed adding comtrs for year {year}')

# # step 3: add the comts from 2005 - 2016 data: 
# for year in range(2006,2017):
#     add_comtrs_2005_2016(year)

pdb.set_trace()
# print('Completed years 2000 - 2007')
# pdb.set_trace()

# pdb.set_trace()

# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Tulare_Lake_Basin_Water_Storage_District')
# pdb.set_trace()

# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Tulare_County')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Kern_County')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Kings_County')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Fresno_County')


# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Cawelo_Water_District')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('North_Kern_Water_Storage_District')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Wasco_Irrigation_District')
# sum_crop_types, crop_data_in_irrigation_district, irrigation_district = retrieve_data_for_irrigation_district('Buena_Vista_Water_Storage_District')

# plot_data_for_irrigation_district(irrigation_district, sum_crop_types)
# plot_tree_crop_percentages_for_irrigation_district(irrigation_district, sum_crop_types)


load_crop_type_all_year()


pdb.set_trace()








