# groundwater_data_compiler_by_season


# http://wdl.water.ca.gov/waterdatalibrary/groundwater/index.cfm
# Same data reported here: 
# https://www.casgem.water.ca.gov/OSS/(S(q4ytwloehqreoahtlcw0z1ia))/Public/SearchWells.aspx
# takes data received from CASGEM and compiles it to plot lift heights and groundwater changes over time for all of  Tulare Lake Basin


import numpy as np 
import math 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import pdb
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):



def get_CASGEM_data(counties, include_elevation_changes):
    header_data = pd.read_csv('casgem_GW_data/gst_file.csv', index_col=0, parse_dates=True)
    
    # counties = 'Tulare'   # set equal to 'All' for all 4 counties in TLB 
    # counties = 'All'
    if counties == 'Tulare':    
    # From header_data GST_file: Extract all the data where "COUNTY_NAME" = Tulare  or Tulare Lake
        county_headers = header_data.loc[lambda df: df.COUNTY_NAME == 'Tulare', :]  # Prints x? rows 
    if counties == 'All': 
        tulare= header_data.loc[lambda df: df.COUNTY_NAME == 'Tulare', :]
        kern = header_data.loc[lambda df: df.COUNTY_NAME == 'Kern', :]
        kings = header_data.loc[lambda df: df.COUNTY_NAME == 'Kings', :]
        fresno = header_data.loc[lambda df: df.COUNTY_NAME == 'Fresno', :]
        county_headers = pd.concat([tulare, kern, kings, fresno])  # [14359 rows x 56 columns]
    pdb.set_trace()
    # tulare_county_headers2 = county_headers.loc[lambda df: df.CASGEM_STATION_USE_DESC == 'Irrigation', :]  # Prints x? rows 
    county_IDs_all = county_headers.index.tolist()        # all IDs in Tulare County 

    tlb_county_IDs_lat_lon = county_headers[['LATITUDE', 'LONGITUDE']]  # save this to a csv for arcGIS use 
    # tlb_county_IDs_lat_lon.to_csv('tlb_county_IDs_lat_lon.csv')
    # pdb.set_trace()

    def data_without_annual_lift_changes():  
        print('Current run: not calculating annual lift changes')
        try:   # Runs this if data already exists in correct folder 
        # if include_elevation_changes == 1:  # CSV includes elevation changes from year prior 
            # well_data_tulare_only = pd.read_csv('well_data_tulare_only2.csv', parse_dates=['MEASUREMENT_DATE'])
        # else: 
            well_data_tulare_only = pd.read_csv('well_data_tulare_only.csv', parse_dates=['MEASUREMENT_DATE']) #[113680 rows x 18 columns]
        
        except:   ############################# Creates the file trimmed to TLB only IF the file does not already exist ###########
            print('Current run: the TLB overall file wasn''t in the searched folder')
            well_data = pd.read_csv('casgem_GW_data/gwl_file.csv', 
                    encoding = 'latin1', parse_dates=['MEASUREMENT_DATE'],
                    date_parser = lambda x:pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')) #, parse_dates=True)
                 
            # locate data at the extracted CASGEM ID values
            well_data_tulare_only = well_data[well_data['CASGEM_STATION_ID'].isin(county_IDs_all)] # [113680 rows x 17 columns]
            well_data_tulare_only.to_csv('well_data_tulare_only.csv')
            print('Current progress: Made new file named "well_data_tulare_only.csv", which does not contain GW lift change')
        return well_data_tulare_only 

    if include_elevation_changes == 1:
    	print('not calculating elevation changes in this script')
        # well_data_tulare_only = data_with_annual_lift_changes()
    else:
        well_data_tulare_only = data_without_annual_lift_changes()

    return well_data_tulare_only, county_headers, county_IDs_all


def drawdown_any_years_comparison(base_year, year_evaluating, season):  # Compares 5 years (averaged) with the average of the 5 years prior
    '''Compares base year and 5 years prior with the chosen evaluating year and 5 years prior'''
    ''' Current depth - Base years depth = drawdown => Large drawdown rates means wells are currently much deeper '''

    base_start =  str(base_year - 5) + '-10-01 00:00:00'
    base_end =  str(base_year) + '-09-30 00:00:00'
    water_year_start = str(year_evaluating -5) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(base_start).year)
    ending = str(pd.to_datetime(water_year_end).year)
    print('experiment with plot_title here')
    # pdb.set_trace()
    plot_title = str(str(base_year -5) + '-' + str(base_year) + ' Groundwater Level Average Compared with ' + str(year_evaluating - 5) + '-' + str(year_evaluating))
    
    year_range_string = ('Water level difference in October',starting,'through September', ending)
    lats = np.empty(len(county_IDs_all))
    lats[:] = np.nan
    lons = np.empty(len(county_IDs_all))
    lons[:] = np.nan
    RP_difference = np.empty(len(county_IDs_all))
    RP_difference[:] = np.nan
    county_id_array = np.empty(len(county_IDs_all))
    county_id_array[:] = np.nan

    for well_iter, county_id in enumerate(tqdm(county_IDs_all)): 
        all_measurements_at_this_county_id = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :] #filters by well
        water_year_evaluating  = all_measurements_at_this_county_id.loc[all_measurements_at_this_county_id['MEASUREMENT_DATE'] >= water_year_start, :] #filters by year 
        water_year_evaluating = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'] <= water_year_end , :]
        # pdb.set_trace()
        water_year_prior  = all_measurements_at_this_county_id.loc[all_measurements_at_this_county_id['MEASUREMENT_DATE'] >= base_start, :]
        water_year_prior = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'] <= base_end , :]

        if season == 'dry':	# parses down to only dry season months (May - September)
            # pdb.set_trace()
            water_year_evaluating  = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'].dt.month > 4, :]  # locate data within May and September 
            water_year_evaluating  = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'].dt.month < 10, :]
            test = water_year_evaluating['MEASUREMENT_DATE'] #.dt.month 
            # pdb.set_trace()
            water_year_prior  = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'].dt.month > 4, :]  # locate data within May and September 
            water_year_prior  = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'].dt.month < 10, :]

            if not water_year_evaluating['MEASUREMENT_DATE'].empty:
                print(f'This month has a value {test } ' )

        if season == 'rainy':
            water_year_evaluating_early_months  = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'].dt.month < 5, :]  # locate data between october and May year + 1
            water_year_evaluating_late_months  = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'].dt.month > 9, :]
            water_year_evaluating = pd.concat([water_year_evaluating_early_months, water_year_evaluating_late_months], axis=0)
            
            if not (water_year_evaluating_early_months['MEASUREMENT_DATE'].empty or water_year_evaluating_late_months['MEASUREMENT_DATE'].empty) :
                print(f'This month has a value {water_year_evaluating } ' )

            water_year_prior_early_months  = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'].dt.month < 5 , :]  # locate data within May and September 
            water_year_prior_late_months  = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'].dt.month > 9, :]
            water_year_prior = pd.concat([water_year_prior_early_months, water_year_prior_late_months], axis=0)

            if not (water_year_evaluating_early_months['MEASUREMENT_DATE'].empty or water_year_evaluating_early_months['MEASUREMENT_DATE'].empty) :
                print(f'This month has a value {water_year_prior } ' )

        RP_average_recent = water_year_evaluating.RP_READING.mean()
        RP_average_base_year = water_year_prior.RP_READING.mean()

        # get lat & long of this county ID 
        lat_test = county_headers.loc[county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = county_headers.loc[county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values
        county_id_array[well_iter] = county_id

        RP_difference[well_iter] = RP_average_recent - RP_average_base_year  # If the water is depleting, this number should be increasing 
        
        remove_outliers = 1
        if remove_outliers ==1:
            if (RP_difference[well_iter] > 350) or (RP_difference[well_iter] < -350) :  # takes out outliers
                RP_difference[well_iter] = np.nan
                print('REMOVING OUTLIERS')

    gw_array = np.vstack((county_id_array, lats, lons, RP_difference))
    gw_array = np.transpose(gw_array)
    gw_df = pd.DataFrame(gw_array)
    gw_df.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df.set_index('county_ID')  # fix id value 
    # pdb.set_trace()
    gw_df.to_csv(   str('GW_change_comparison' + str(base_year) +'with' + str(year_evaluating) + '.csv'))
    # pdb.set_trace()

    return RP_difference, lats, lons, year_range_string, county_id_array, plot_title 


counties = 'All'  
include_elevation_changes = 0 

well_data_tulare_only, county_headers, county_IDs_all = get_CASGEM_data(counties, include_elevation_changes)
# pdb.set_trace()

seasonal_drawdown = 1
if seasonal_drawdown ==1: 
    base_year = 1995
    year_evaluating = 2010 
    # season = 'whole year'
    season = 'dry'     # 534.032005018674 
    # season = 'rainy' # sum of drawdown is -12047.331383899713 
    RP_difference, lats, lons, year_range_string, county_id_array, plot_title = drawdown_any_years_comparison(base_year, year_evaluating, season)
    print('pause year and test out stuff')
    print(f'sum of drawdown is {np.nansum(RP_difference)} ')
    print(f'median well drawdown in TLB over the given timeframe is {np.nanmedian(RP_difference)} ' )
    print(f'average drawdown over the timeframe is {np.nanmean(RP_difference)}')
    pdb.set_trace()
    print('Test manually from here')




