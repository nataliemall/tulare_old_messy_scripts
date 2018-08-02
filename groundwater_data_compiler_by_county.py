 # Well data analysis - Change in groundwater levels 

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
    pdb.set_trace()

    
    def data_with_annual_lift_changes():
        try: 
            well_data_tulare_only = pd.read_csv('well_data_tulare_only2.csv', parse_dates=['MEASUREMENT_DATE'])
        except:   ############################# Creates the file trimmed to TLB only IF the file does not already exist ###########
            print('The TLB overall file wasn''t in the searched folder')
            well_data = pd.read_csv('casgem_GW_data/gwl_file.csv', 
                    encoding = 'latin1', parse_dates=['MEASUREMENT_DATE'],
                    date_parser = lambda x:pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')) #, parse_dates=True)
             
            # locate data at the extracted CASGEM ID values
            well_data_tulare_only = well_data[well_data['CASGEM_STATION_ID'].isin(county_IDs_all)] # [113680 rows x 17 columns]

            well_data_tulare_only.to_csv('well_data_tulare_only.csv') # Renames the well_data_tulare_only2.csv data to the main well_data_tulare_only csv  
            well_data_tulare_only = pd.read_csv('well_data_tulare_only.csv', parse_dates=['MEASUREMENT_DATE']) #[113680 rows x 18 columns]    # converts the newly made csv file to a variable 

            ###############################  Creates column for the yearly change ###########################################################

            change = np.empty((len(well_data_tulare_only),1,))
            change[:] = np.nan

            #array(['Irrigation', 'Industrial', 'Residential', 'Observation',# 'Stockwatering', 'Unknown']) - also Stockwater, Other, nan
            for row in tqdm(range(len(well_data_tulare_only))):
                if float('-inf') < float(well_data_tulare_only.RP_READING.iloc[row]) < float('inf'):
                    ID_no = well_data_tulare_only.CASGEM_STATION_ID.iloc[row]
                    current_station = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == ID_no, :]
                    # print(f'current station', current_station )
                    year_current = well_data_tulare_only.MEASUREMENT_DATE.iloc[row].year
                    month_current = well_data_tulare_only.MEASUREMENT_DATE.iloc[row].month 
                    len_current = current_station.shape[0]
                    for dates in range(len_current):  # problem: station 23279 
                        year_previous = current_station.MEASUREMENT_DATE.iloc[dates].year 
                        month_same = current_station.MEASUREMENT_DATE.iloc[dates].month

                        if (    0 < year_current < 2050 
                            and 0 < month_same < 14
                            and 0 < year_previous < 2050
                            and 0 < month_current < 14   # checks to make sure all month & year data is accurate
                            and year_current == year_previous + 1  # Goes through dates at this station ID and locates previous year
                            and month_current == month_same  # Goes through dates at this station ID and locates equivalent month
                            ):
                                previous_reading = current_station.RP_READING.iloc[dates]
                                if float('-inf') < float(previous_reading) < float('inf'):
                                    change[row] = well_data_tulare_only.RP_READING[row] -  previous_reading  # Calculates change in GW lift from the same month in th year prior 
                                    change_written = np.array2string(change[row])
            
            well_data_tulare_only['change_from_year_prior'] = change   # puts the depth change array into the overall array 
            well_data_tulare_only.to_csv('well_data_tulare_only2.csv') # creates data file with the changes included 
            print('Made new file named "well_data_tulare_only2.csv", which contains GW lift change ')
            
            pdb.set_trace()

        return well_data_tulare_only

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

        well_data_tulare_only = data_with_annual_lift_changes()
    else:
        well_data_tulare_only = data_without_annual_lift_changes()

    return well_data_tulare_only, county_headers, county_IDs_all


def compare_historical_with_2012(well_data_tulare_only): 
    ''' calculates necessar variables for comparing historical with 2012 data'''
    starting_datetime = '2012-07-01 00:00:00'   # ideally this will be variable  
    tulare_wells10 = well_data_tulare_only.loc[well_data_tulare_only['MEASUREMENT_DATE'] >= '2012-07-01 00:00:00', :]
    tulare_wells11 = tulare_wells10.loc[tulare_wells10['MEASUREMENT_DATE'] <= '2012-11-01 00:00:00', :]             # All the dates after a summer irrigation season (July - November)
    tulare_wells_1980 = well_data_tulare_only.loc[well_data_tulare_only['MEASUREMENT_DATE'] >= '1960-07-01 00:00:00', :]
    tulare_wells_1980_1985 = tulare_wells_1980.loc[tulare_wells_1980['MEASUREMENT_DATE'] <= '1985-11-01 00:00:00', :]  # All measurement dates between 1960 and 1985

    tulare_wells13 = tulare_wells11[0:1] # starts dataframe of well data 

    station_ids = tulare_wells11.CASGEM_STATION_ID.values.tolist()
    headers_selected_timeperiod = county_headers[county_headers.index.isin(station_ids)]  # extracts headers only of the Tulare wells within the timeframe
    tulare_wells16 = headers_selected_timeperiod.loc[headers_selected_timeperiod.index == county_IDs_all[0], :]   # starts dataframe of header data 

    # pdb.set_trace()
    missing_1980 = 0 # sanity check 
    elevation_column = ['CASGEM_STATION_ID', 'ave_80_85']
    water_level_ave_80_85 = pd.DataFrame(columns = elevation_column) # create dataframe column for the waterlevel change
    array_80_85 = np.zeros(1000)  # To be filled in function "seasonal_and_other_comparisons"
    array_80_85_wellIDs = np.zeros(1000, dtype=np.int32)

    return starting_datetime, tulare_wells11, tulare_wells_1980, tulare_wells_1980_1985, tulare_wells13, tulare_wells16, missing_1980, water_level_ave_80_85, array_80_85, array_80_85_wellIDs 


def average_depth_year_comparison(year_evaluating):   #compares a given year with the year before & saves it to a CSV 

    # year = year_evaluating - 1
    water_year_start = str(year_evaluating -1) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'
    year_prior_start =  str(year_evaluating - 2) + '-10-01 00:00:00'
    year_prior_end =  str(year_evaluating - 1) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(water_year_start).year)
    ending = str(pd.to_datetime(year_prior_end).year)

    year_range_string = ('Water level difference in October',starting,'through September', ending)

    lats = np.empty(len(county_IDs_all))
    lats[:] = np.nan
    lons = np.empty(len(county_IDs_all))
    lons[:] = np.nan
    RP_difference = np.empty(len(county_IDs_all))
    RP_difference[:] = np.nan
    county_id5 = np.empty(len(county_IDs_all))
    county_id5[:] = np.nan    

    well_iter = 0 
    for county_id in tqdm(county_IDs_all): 
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :] #filters by well
        water_year_evaluating  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= water_year_start, :] #filters by year 
        water_year_evaluating = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'] <= water_year_end , :]


        water_year_prior  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= year_prior_start, :]
        water_year_prior = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'] <= year_prior_end , :]

        # starting_datetime = '2012-07-01 00:00:00'

        # test3 = well_data_tulare_only.resample(well_data_tulare_only.RP_READING,'6M', on='MEASUREMENT_DATE')
        # (start='Sep-1939', end=' Sep-2018', freq='6M')
        # pd.resample(well_data_tulare_only.RP_READING,'6M')

        RP_average = water_year_evaluating.RP_READING.mean()
        RP_average_prior = water_year_prior.RP_READING.mean()

        # get lat & long of this county ID 
        lat_test = county_headers.loc[county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = county_headers.loc[county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values

        RP_difference[well_iter] = RP_average - RP_average_prior  # If the water is depleting, this number should be increasing 
        ## Bigger numbers are bad
        ## RP = depth to groundwater 
        ## if the new RP value is smaller, the water level rose and the RP_difference value is negative 
        if RP_difference[well_iter] < -600:
            RP_difference[well_iter] = np.nan
        np.mean(water_year_evaluating.RP_READING)
        # pdb.set_trace()
        county_id5[well_iter] = county_id

        well_iter = well_iter + 1
    gw_array7 = np.vstack((county_id5, lats, lons, RP_difference))
    gw_array7 = np.transpose(gw_array7)
    gw_df7 = pd.DataFrame(gw_array7)
    gw_df7.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df7.set_index('county_ID')
    gw_df7.to_csv('GW_change_2015.csv')
    return RP_difference, lats, lons , year_range_string


def average_depth_5year_comparison(year_evaluating):  # Compares 5 years (averaged) with the average of the 5 years prior

    # year = year_evaluating - 1
    water_year_start = str(year_evaluating -5) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'
    year_prior_start =  str(year_evaluating - 10) + '-10-01 00:00:00'
    year_prior_end =  str(year_evaluating  - 5) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(year_prior_start).year)
    ending = str(pd.to_datetime(water_year_end).year)
    print('experiment with plot_title here')
    pdb.set_trace()
    plot_title = str(str(year_evaluating -5) + '-' + str(year_evaluating) + ' Groundwater Level Average Compared with ' + str(year_evaluating -10) + '-' + str(year_evaluating -5))
    
    year_range_string = ('Water level difference in October',starting,'through September', ending)
    lats = np.empty(len(county_IDs_all))
    lats[:] = np.nan
    lons = np.empty(len(county_IDs_all))
    lons[:] = np.nan
    RP_difference = np.empty(len(county_IDs_all))
    RP_difference[:] = np.nan
    county_id5 = np.empty(len(county_IDs_all))
    county_id5[:] = np.nan

    # well_iter = 0 
    for well_iter, county_id in enumerate(tqdm(county_IDs_all)): 
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :] #filters by well
        water_year_evaluating  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= water_year_start, :] #filters by year 
        water_year_evaluating = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'] <= water_year_end , :]


        water_year_prior  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= year_prior_start, :]
        water_year_prior = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'] <= year_prior_end , :]

        RP_average = water_year_evaluating.RP_READING.mean()
        RP_average_prior = water_year_prior.RP_READING.mean()

        # get lat & long of this county ID 
        lat_test = county_headers.loc[county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = county_headers.loc[county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values
        county_id5[well_iter] = county_id

        RP_difference[well_iter] = RP_average - RP_average_prior  # If the water is depleting, this number should be increasing 
        if RP_difference[well_iter] > 100:  # takes out outliers
            RP_difference[well_iter] = np.nan
        # np.mean(water_year_evaluating.RP_READING)
        # well_iter = well_iter + 1
        # pdb.set_trace()

    gw_array7 = np.vstack((county_id5, lats, lons, RP_difference))
    gw_array7 = np.transpose(gw_array7)
    gw_df7 = pd.DataFrame(gw_array7)
    gw_df7.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df7.set_index('county_ID')  # fix id value 
    gw_df7.to_csv('GW_change_2015.csv')
    # pdb.set_trace()

    return RP_difference, lats, lons, year_range_string, county_id5, plot_title 


def drawdown_any_years_comparison(base_year, year_evaluating):  # Compares 5 years (averaged) with the average of the 5 years prior
    '''Compares base year and 5 years prior with the chosen evaluating year and 5 years prior'''
    ''' Current depth - Base years depth = drawdown => Large drawdown rates means wells are currently much deeper '''

    base_start =  str(base_year - 5) + '-10-01 00:00:00'
    base_end =  str(base_year) + '-09-30 00:00:00'

    water_year_start = str(year_evaluating -5) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(base_start).year)
    ending = str(pd.to_datetime(water_year_end).year)
    print('experiment with plot_title here')
    pdb.set_trace()
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
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :] #filters by well
        water_year_evaluating  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= water_year_start, :] #filters by year 
        water_year_evaluating = water_year_evaluating.loc[water_year_evaluating['MEASUREMENT_DATE'] <= water_year_end , :]


        water_year_prior  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'] >= base_start, :]
        water_year_prior = water_year_prior.loc[water_year_prior['MEASUREMENT_DATE'] <= base_end , :]

        RP_average_recent = water_year_evaluating.RP_READING.mean()
        RP_average_base_year = water_year_prior.RP_READING.mean()

        # get lat & long of this county ID 
        lat_test = county_headers.loc[county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = county_headers.loc[county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values
        county_id_array[well_iter] = county_id

        RP_difference[well_iter] = RP_average_recent - RP_average_base_year  # If the water is depleting, this number should be increasing 
        if RP_difference[well_iter] > 150:  # takes out outliers
            RP_difference[well_iter] = np.nan

    gw_array = np.vstack((county_id_array, lats, lons, RP_difference))
    gw_array = np.transpose(gw_array)
    gw_df = pd.DataFrame(gw_array)
    gw_df.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df.set_index('county_ID')  # fix id value 
    pdb.set_trace()
    print('line 356')
    gw_df.to_csv(   str('GW_change_comparison' + str(base_year) +'with' + str(year_evaluating) + '.csv'))
    # pdb.set_trace()

    return RP_difference, lats, lons, year_range_string, county_id_array, plot_title 

# Function that compiles the seasonal average right here 
def compile_seasonal_averages():
    print('Compiling seasonal averages- please wait')
    # Variables for yearly averages data 
    seasonal_average = np.empty((len(county_IDs_all),158,))
    seasonal_average[:] = np.nan
    seasonal_average[0] = 0  
    year_range = np.arange(1940,2017) # changed to just 1940 
    # well_iter = 0 
    pdb.set_trace()
    df_seasonal_by_year = {}

    for year in year_range:
        df_seasonal = pd.DataFrame(columns = ['well_ID', 'dry_season', 'rainy_season', 'drawdown']) # overall dataframe to add to
        df_seasonal.well_ID = np.zeros(len(county_IDs_all))
        df_seasonal.dry_season = np.zeros(len(county_IDs_all))
        df_seasonal.rainy_season = np.zeros(len(county_IDs_all))
        df_seasonal.drawdown = np.zeros(len(county_IDs_all))
        

        for well_iter, county_id in enumerate(tqdm(county_IDs_all)):   # runs through data for all Tulare County IDs 
            #Data for this specific well ID: 
            tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]
            df_seasonal.well_ID[well_iter] = county_id
            season_iter = 0 

             # for year in year_range:
            tulare_well_ID_year = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'].dt.year == year - 1 , :]
            tulare_well_ID_year = tulare_well_ID_year.loc[tulare_well_ID_year['MEASUREMENT_DATE'].dt.month > 9, :]  # locate data betwwen october and May of year prior
            
            tulare_well_ID_year_part2 = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'].dt.year == year, :]  # second half of rainy season
            tulare_well_ID_year_part2 = tulare_well_ID_year_part2.loc[tulare_well_ID_year_part2['MEASUREMENT_DATE'].dt.month < 5, :]  # before May 
            # pdb.set_trace()

            # tulare_rainy_combined = np.append(tulare_well_ID_year.RP_READING, tulare_well_ID_year_part2.RP_READING) # combines the season 
            # pdb.set_trace()
            part1 = tulare_well_ID_year.RP_READING.values
            part2 = tulare_well_ID_year_part2.RP_READING.values
            # pdb.set_trace()

            combined = np.append(part1, part2)
            average_rainy = np.empty(1)
            average_rainy[:] = np.nan
            if combined.size > 0:
                average_rainy = np.mean(combined)
            # pdb.set_trace()
            seasonal_average[well_iter, season_iter] = average_rainy  # compiles average for the rainy season and places it in seasonal_average dataframe
            df_seasonal.rainy_season[well_iter] = average_rainy
            # Dry season 
            tulare_well_ID_year_dry  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'].dt.year == year, :]
            tulare_well_ID_year_dry  = tulare_well_ID_year_dry.loc[tulare_well_ID_year_dry['MEASUREMENT_DATE'].dt.month > 4, :]  # locate data betwwen october and May year + 1
            tulare_well_ID_year_dry  = tulare_well_ID_year_dry.loc[tulare_well_ID_year_dry['MEASUREMENT_DATE'].dt.month < 10, :]  # locate data betwwen october and May year + 1

            dry_season_values = tulare_well_ID_year_dry.RP_READING.values 


            if dry_season_values.size > 0:
                seasonal_average[well_iter, season_iter + 1] = np.mean(tulare_well_ID_year_dry.RP_READING)
            df_seasonal.dry_season[well_iter] = dry_season_values.mean()

            df_seasonal.drawdown[well_iter] = df_seasonal.dry_season[well_iter] - df_seasonal.rainy_season[well_iter]
                # Create pandas dataframe here 
            season_iter = season_iter + 2

            # well_iter = well_iter + 1  
            # pdb.set_trace()
    
        df_seasonal_by_year[year] = df_seasonal
    
        title = str('seasonal_df_year' +  str(year) + '.csv')
        df_seasonal.to_csv(title )

    pdb.set_trace()
    np.savetxt("seasonal_averages.csv", seasonal_average, delimiter=",")
    np.savetxt("seasonal_averages_corresponding_IDs.csv", county_IDs_all, delimiter=",")


def import_seasonal_averages():
    print('importing seasonal averages calculated at a previous time')
    imported_seasonal_averages = np.loadtxt('seasonal_averages.csv', delimiter=',')  # array of all 2147 wells in Tulare county, averaged by season 

    return imported_seasonal_averages 

# Iterates through each of the well IDs in Tulare County 
def seasonal_and_other_comparisons(tulare_wells13, missing_1980, tulare_wells16, v, r, Y_irrigation, include_elevation_changes):
    print('Current progress: making seasonal comparisons')
    for well_iter, county_id in enumerate(tqdm(county_IDs_all)):   # runs through data for all Tulare County IDs 
        #Data for this specific well ID: 
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]

        # well_iter = well_iter + 1 
        seasonal_average_test = 'no longer calculated in this section'

        skip_id = 0 
        skip_id2 = 0

        tulare_wells80 = tulare_wells_1980_1985.loc[tulare_wells_1980_1985['CASGEM_STATION_ID'] == county_id, :]
        tulare_wells81 = tulare_wells80.RP_READING.mean()  # takes only first measurement in the time period 

        if tulare_wells80.empty:               # All values are empty (no data points between 80-85 for this ID)
            missing_1980 = missing_1980 + 1
            skip_id2 = 1  

        if skip_id2 == 0:
            tulare_wells9 = tulare_wells11.loc[tulare_wells11['CASGEM_STATION_ID'] == county_id, :]
            tulare_wells12 = tulare_wells9[0:1]   # takes only first measurement in the time period 
            tulare_wells13 = pd.merge(tulare_wells12, tulare_wells13, how='outer')  # merges ----  contains depths for all wells in October 2012 

        if tulare_wells9.empty:
            skip_id = 1  # skip when tulare_wells12 is empty
            skip_id2 = 1   # = 1 if either are empty

        # if tulare_wells80.empty:
            continue

        if skip_id2 == 0:
            tulare_wells15 = county_headers.loc[county_headers.index == county_id, :]
            tulare_wells16 = pd.merge(tulare_wells15, tulare_wells16, how='outer')   # before skipping: 2147 rows # just skipping when 2012 data missing: 257 rows. Skipping when both are missing: 120 
            # merge: adds values to the top row


            # include a row of 1960 - 1985 depth average data 
            array_80_85[v] = tulare_wells81  # average RP_reading 1980 - 1885 
            array_80_85_wellIDs[v] = county_id  # county id to merge correctly 
            # pdb.set_trace() # check how things are merging.  
            tulare_wells2 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]
            water_level = tulare_wells2.RP_READING

            # tulare_wells_oct_nov = tulare_wells2.MEASUREMENT_DATE.month 
            tulare_wells_oct = tulare_wells2.loc[tulare_wells2['MEASUREMENT_DATE'].dt.month == 10, :] #.unique()
            water_level_oct = tulare_wells_oct.RP_READING
            
            plotting_figs1_2 = 0
            if plotting_figs1_2 ==1:
                plt.figure(1)
                plt.plot(tulare_wells2.MEASUREMENT_DATE, water_level) 
                plt.xlabel('Measurement Date')
                plt.ylabel('Water levels for all data in Tulare County')
                # YAY tulare_wells13 and tulare_wells16 are equal!!! 

                # water_level2 = tulare_wells2.RP_READING  # Plot data for all October-November readings 
                plt.figure(2)
                plt.plot(tulare_wells_oct.MEASUREMENT_DATE, water_level_oct)
                plt.xlabel('Measurement Date')
                plt.ylabel('Water level for all October-November readings')
            # Plot ONLY october-november of each year 
            v = v + 1
        
        if include_elevation_changes == 1: 
            # Plotting elevation change from year prior: 
            tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]
            water_level_change2 = tulare_wells90.change_from_year_prior

        # tulare_wells13 = pd.merge(tulare_wells12, tulare_wells13, how='outer')  # merges ----  contains depths for all wells in October 2012 
        # pdb.set_trace()
        gw_changes_by_year = 0    # Plots elevations changes--  set include_elevation_changes == 1
        if gw_changes_by_year ==1: 
            plt.figure(50)  # plots water elevation change with year prior over time
            # figure50_data = go.Scatter(x = tulare_wells90.MEASUREMENT_DATE, y = water_level_change2, mode = 'markers')
            dats_fig_50 = tulare_wells90.MEASUREMENT_DATE
            # pdb.set_trace()
            plt.plot(dats_fig_50, water_level_change2, linestyle = '', marker = '.')
            # df.plot.scatter()
            # water_level_change2.plot()
                                                        # this one won't let me scatter
            plt.xlabel('Measurement Date')
            plt.ylabel('Water level change from previous year')
            plt.title('Monthly Comparison of Water Level Changes')

        plot_change_by_basin = 0 # if plotting,set include_elevation_changes == 1
        if plot_change_by_basin ==1:
            plt.figure(55) 
            basin_label1 = county_headers.BASIN_DESC[county_id]
            dats_fig_55 = tulare_wells90.MEASUREMENT_DATE
            if county_headers.BASIN_DESC[county_id] == 'Tule': 
                if plt_legend[40] ==1:
                    plt.plot(dats_fig_55, water_level_change2, linestyle = '', marker = '.', c = 'm')
                    # plt.scatter(x_values, y_values, c = 'g', alpha=0.7, label=basin_label)
                    plt_legend[40] = 0
                else: 
                    plt.plot(dats_fig_55, water_level_change2, linestyle = '', marker = '.', c = 'm')
            elif county_headers.BASIN_DESC[county_id] == 'Kaweah': 
                if plt_legend[42] ==1:
                    plt.plot(dats_fig_55, water_level_change2, c = 'r', linestyle = '', marker = '.')
                    plt_legend[42] = 0
                else:
                    plt.plot(dats_fig_55, water_level_change2, c = 'r', linestyle = '', marker = '.')
            else:
                plt.plot(dats_fig_55, water_level_change2, c = 'g', linestyle = '', marker = '.')
            plt.xlabel('Measurement Date')
            plt.ylabel('Water level change from previous year')
            plt.title('Monthly Comparison of Water Level Changes')
            # plt.legend()

        # if import_seasonal_averages ==1:
        def plot_seasonal_average(r, Y_irrigation):

            # x_values = np.arange(1939.5,2018.5, 0.5)                          # What is a better way? - Pandas resample
            x_values = pd.date_range(start='Sep-1939', end=' Sep-2018', freq='6M')
            # x_values = tulare_wells90.MEASUREMENT_DATE
            y_values = imported_seasonal_averages[well_iter,:]  # check to make sure it shouldn't be well_iter - 1 # june 29 
            plot_by_use = 1  #Plot averages by well use type 
            if plot_by_use == 1: 
                plt.figure(51)
                welltype_label = county_headers.CASGEM_STATION_USE_DESC[county_id]
                # array(['Unknown', 'Irrigation', 'Residential', 'Observation', 'Other',
                 #      'Stockwatering', 'Industrial'], dtype=object)
                if county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Irrigation': 

                    # X_irrigation[r,:] = x_values
                    Y_irrigation[r,:] = y_values 
                    r = r + 1
                    # pdb.set_trace()
                    if plt_legend[10] ==1:

                        plt.scatter(x_values, y_values, c = 'g', alpha=0.3, label=welltype_label)
                        # plt.figure(34) # extra figure 
                        # plt.scatter(x_values, y_values, c = 'g', alpha=0.3, label=welltype_label)

                        plt_legend[10] = 2          
                    else:
                        plt.scatter(x_values, y_values, c = 'g', alpha = 0.3)
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Residential': 
                    if plt_legend[11] ==1:
                        plt.scatter(x_values, y_values, c = 'b', alpha=0.5, label=welltype_label)
                        plt_legend[11] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'b', alpha = 0.5)
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Observation': 
                    if plt_legend[12] ==1:
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3, label=welltype_label)
                        plt_legend[12] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'c', alpha = 0.3)
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Other': 
                    if plt_legend[13] ==1:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3, label=welltype_label)
                        plt_legend[13] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'm', alpha = 0.3)
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Stockwatering': 
                    if plt_legend[14] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.7, label=welltype_label)
                        plt_legend[14] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha = 0.3)
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Industrial': 
                    if plt_legend[15] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=1, label=welltype_label)
                        plt_legend[15] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha = 1) 
                elif county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Unknown': 
                    if plt_legend[16] ==1:
                        plt.scatter(x_values, y_values, c = '0.5', alpha=0.7, label=welltype_label)
                        plt_legend[16] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = '0.5', alpha = 0.3) 
                else:
                    plt.scatter(x_values, y_values, c = 'k')
                plt.xlabel('Measurement Date')
                plt.ylabel('Water level seasonal average')
                plt.title('Tulare Lake County Wells - by Use')
                plt.legend()    # how legend 

            plot_by_basin = 0  # plot averages by basin
            if plot_by_basin ==1:
                plt.figure(53)
                basin_label = county_headers.BASIN_DESC[county_id]
                # if county_headers.CASGEM_STATION_USE_DESC[well_iter-1] == 'Irrigation': 
                #   print('this iteration is an irrigation well')   # Help here 
                
                if county_headers.BASIN_DESC[county_id] == 'Tulare Lake': 
                    if plt_legend[1] ==1:
                        plt.scatter(x_values, y_values, c = 'g', alpha=0.7, label=basin_label)
                        plt_legend[1] = 0
                    else: 
                        plt.scatter(x_values, y_values, c = 'g', alpha=0.7)
                elif county_headers.BASIN_DESC[county_id] == 'Kern County': 
                    if plt_legend[2] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.3, label=basin_label)
                        plt_legend[2] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.3)
                elif county_headers.BASIN_DESC[county_id] == 'Tule':    # mostly this basin
                    if plt_legend[3] ==1:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3, label=basin_label)
                        plt_legend[3] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3)
                elif county_headers.BASIN_DESC[county_id] == 'Westside': 
                    if plt_legend[4] ==1:
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3, label=basin_label)
                        plt_legend[4] = 0
                    else: 
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3)
                elif county_headers.BASIN_DESC[county_id] == 'Kaweah':  # and this basin
                    if plt_legend[5] ==1:
                        plt.scatter(x_values, y_values, c = 'r', alpha = 0.3,label=basin_label)
                        plt_legend[5] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'r', alpha=0.3) 
                elif county_headers.BASIN_DESC[county_id] == 'Kings': 
                    if plt_legend[6] ==1:
                        plt.scatter(x_values, y_values, c = 'b', alpha=0.3, label=basin_label)  
                        plt_legend[6] = 0
                    else: 
                        plt.scatter(x_values, y_values, c = 'b', alpha=0.3)     
                else:
                    plt.scatter(x_values, y_values, c = '0.3')

                    # 'Kern County', 'Tule', 'Tulare Lake', 'Westside', 'Kaweah', 'Kings'
                plt.xlabel('Measurement Date')
                plt.ylabel('Water level seasonal average')
                plt.title('Tulare County Wells: by Sub-basin')
                legend_labels = ['Tulare Lake','Kern County', 'Tule', 'Westside', 'Kaweah', 'Kings']
                plt.legend()  

            return r, Y_irrigation
        if compiling_seasonal_averages == 0: # function runs if seasonal averages have already been compiled 
            r, Y_irrigation= plot_seasonal_average(r, Y_irrigation)
            seasonal_average_test = 'Test- seasonal_average is already saved in the csv file'
    # Save seasonal_averages to a .csv file

    return seasonal_average_test, tulare_wells13, tulare_wells16


def water_drawdown_changes_1980_85():
    # Add tulare_wells13 columns to tulare_wells16 
    tulare_wells17 = pd.merge(tulare_wells13, tulare_wells16)

    # CASGEM_STATION_ID
    water_level_ave_80_85.CASGEM_STATION_ID = array_80_85_wellIDs[0:len(tulare_wells17)] 
    # water_level_ave_80_85.CASGEM_STATION_ID = water_level_ave_80_85.CASGEM_STATION_ID.tolist() # adds the station ID to the df 
    water_level_ave_80_85.ave_80_85 = array_80_85[0:len(tulare_wells17)]  # these values need to be inversed 
    # pdb.set_trace()

    tulare_wells18 = pd.merge(tulare_wells17, water_level_ave_80_85)  # merges the average vals with tulare_wells17 
    tulare_wells18['RP_change'] = tulare_wells18.RP_READING - tulare_wells18.ave_80_85  # smaller RP means water closer to surface

    water_drawdown_changes = tulare_wells18.RP_change.values
    # pdb.set_trace()
    # water_drawdown_ids = tulare_wells18.CASGEM_STATION_ID.values
    # well_ids_with_drawdown = pd.DataFrame(water_drawdown_changes, water_drawdown_ids)
    df_well_ids_with_drawdown = tulare_wells18.ix[:,['CASGEM_STATION_ID','RP_change']]

    ## Create pandas dataframe 

    if include_elevation_changes ==1:
        change_year_before = tulare_wells18.change_from_year_prior.values # FIX THIS - Should use tulare_wells2 or tulare_wells_oct # depends on date entered for recent timeframe - tulare_wells10  - originally tulare_wells18
    else:
        change_year_before = 'no change from year before calculated due to include_elevation_changes == 0 '
        print(change_year_before)

    lats = tulare_wells18.LATITUDE.values
    lons = tulare_wells18.LONGITUDE.values
    return df_well_ids_with_drawdown, water_drawdown_changes, change_year_before, lats, lons 


def gw_map_changes(water_drawdown_changes):  
    ''' Style option 1 for plotting- doesn't contain hard-coded max and mins to keep scaling the same'''

    ############# plotting the GW change  #####dfsf########
    # Groundwater plotting of (historical data average - 2012 levels)
    print('printing with qw_map_changes function')
    # create map background  
    plt.figure(3)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='i', area_thresh=25000.0)

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 5000, dpi=300, verbose= True)
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')

    x,y = m(lons,lats)
    variable_object = plt.cm.get_cmap('RdYlGn')
    m.scatter(x,y,s=30,c=water_drawdown_changes, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()

    plt.show()


def plot_map(RP_difference, lats, lons, range_string, plot_title): 
    '''Style option 2 for plotting '''
    print('Plotting')
    print(range_string)
    print('pause here')
    pdb.set_trace()
    # create map background  
    plt.figure(16)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='f', area_thresh=25000.0)  # change resolution to 'high' l

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 1000, dpi=300, verbose= True)
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')

    x,y = m(lons,lats)
    variable_object = plt.cm.get_cmap('bwr')
    m.scatter(x,y,s=30,c=RP_difference, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()

    plt.title(plot_title)
    # plt.title('2010 - 2015 Groundwater Level Average Compared with 2005 - 2010')
    plt.clim(-100,65)
    plt.savefig("comparison_GW.png", dpi = 300)
    plt.show()
    # pdb.set_trace()

def convert_to_cartesian(lats, lons ):
    '''https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
        WGS-84 longitude and latitude into Cartesian coordinates '''

    earth_rad = 6371   # radius of the earth in KM 
    lat_radians = lats * np.pi / 180  # http://www.geomidpoint.com/example.html
    lon_radians = lons * np.pi / 180 

    x_vals = earth_rad * np.cos(lat_radians) * np.cos(lon_radians)
    y_vals = earth_rad * np.cos(lat_radians) * np.sin(lon_radians)
    z_vals = earth_rad * np.sin(lat_radians)

    return x_vals, y_vals, z_vals 


def create_csv_for_arcgis(filename, county_id5, lats, lons, RP_difference): 
    # pdb.set_trace()
    gw_array = np.vstack((county_id5, lats, lons, RP_difference))
    gw_array = np.transpose(gw_array)
    gw_df = pd.DataFrame(gw_array)
    gw_df.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df.set_index('county_ID')  # fix id value 
    gw_df.to_csv(filename)   # saves file 

    print(f'Saved the file as {filename} ')

####################### Start of tree frame ##############################
# counties = 'Tulare'
counties = 'All'   ############# not yet complete: this doesn't actually implement since it first tries to use the cvs file already stored 
include_elevation_changes = 1 # include elevation compared to year before - will calculate these IF the file does not exist 
compiling_seasonal_averages = 1 # takes the data and compiles average RP_READING for each season (set equal to 1 if this hasn't already been done)

well_data_tulare_only, county_headers, county_IDs_all = get_CASGEM_data(counties, include_elevation_changes)

(starting_datetime, tulare_wells11, tulare_wells_1980, tulare_wells_1980_1985, tulare_wells13, 
    tulare_wells16, missing_1980, water_level_ave_80_85, array_80_85, array_80_85_wellIDs) = compare_historical_with_2012(well_data_tulare_only)

plotting_test_2013 = 0
if plotting_test_2013 == 1: 
    RP_difference, lats, lons, date_range_string = average_depth_year_comparison(2013)

v = 0 
plt_legend = np.ones(50)

# saving irrigation averages #### Fix the fact that this is hardcoded 
X_irrigation = np.empty([180,158])    #### delete this eventually? 
X_irrigation[:] = np.nan
Y_irrigation = np.empty([1800,158])    ### changed to 1800 so array is unlikely to fill
Y_irrigation[:] = np.nan
r = 0 
# well_iter = 0 

# Compile the data (set equal to zero if already done)
if compiling_seasonal_averages == 1:    # Compiles seasonal averages of the data and saves it as "seasonal_averages.csv"
    compile_seasonal_averages()
pdb.set_trace()

# import the data necessary 
# if compile_seasonal_averages
imported_seasonal_averages = import_seasonal_averages()   # imports the seasonal average data as imported_seasonal_averages
print('just imported seasonal data')
pdb.set_trace()

# well_iter = 0 
seasonal_average_test, tulare_wells13, tulare_wells16 = seasonal_and_other_comparisons(tulare_wells13, missing_1980, tulare_wells16, v, r, Y_irrigation, include_elevation_changes)

df_well_ids_with_drawdown, water_drawdown_changes, change_year_before, lats, lons = water_drawdown_changes_1980_85()
df_well_ids_with_drawdown.to_csv('df_well_ids_with_drawdown.csv', na_rep = "nan" , index = False  )

pdb.set_trace()

testing_june29 = 1
if testing_june29 ==1: 
    base_year = 1995
    year_evaluating = 2010 
    RP_difference, lats, lons, year_range_string, county_id_array, plot_title = drawdown_any_years_comparison(base_year, year_evaluating)
    print('pause year and test out stuff')
    pdb.set_trace()
    print('Test manually from here')


gw_map_changes(water_drawdown_changes)   # gives a figure that seems interpolatable 
print('paused here after making the first graph')
pdb.set_trace()

if include_elevation_changes == 1:   # this doesn't plot right now # Something about a bad gateway error FIX when there's time
    plt.figure(3)
    # varaible change_year_before: GW plotting of changes in water level from year prior -  for a certain year - set-up for only years with historical data
    gw_map_changes(change_year_before)


groundwater_map3 = 0  # should eventually delete this since it doesn't set the scale consistently 
if groundwater_map3 ==1:
    RP_difference, lats, lons, range_string = average_depth_year_comparison(2016)


    print(range_string)
    # create map background  
    plt.figure(13)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='i', area_thresh=25000.0)

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 5000, dpi=500, verbose= True)
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')
    x,y = m(lons,lats)

    # sdlfkj = mplc.Colormap('RdYlBu')
    variable_object = plt.cm.get_cmap('bwr')
    m.scatter(x,y,s=30,c=RP_difference, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()
    plt.title('2016 Groundwater Level Average Compared with 2015')

    plt.show()

groundwater_map7 = 1 # - attempt2  set colorbar scale plots the average for the 5 years leading up, and the previous 5
if groundwater_map7 ==1:
    RP_difference, lats, lons, range_string, county_id5, plot_title = average_depth_5year_comparison(2015)  # crunch numbers & saves to file for arcgis processing 
    plot_map(RP_difference, lats, lons, range_string, plot_title)   # plot it 

filename = 'RP_diff_for_arc_gis.csv'
create_csv_for_arcgis(filename, county_id5, lats, lons, RP_difference)

attempt_all_irrigation = 1  #plots all months of irrigation averages by season 
if attempt_all_irrigation ==1:
    # plt.plot(X_irrigation[1,:], Y_irrigation[1,:])  # WIll probably delete this - was previosly hardcoded in 


    irrigation_average_mean = np.empty(158)
    irrigation_average_mean[:] = np.nan

    for year in range(158):
        irrigation_average_mean[year] = np.nanmean(Y_irrigation[:,year])  # first year average
        irrigation_average_mean[year] = irrigation_average_mean[year] * (-1)  # reversed for "drawdown"

    x_values = pd.date_range(start='Sep-1939', end=' Sep-2018', freq='6M')
    plt.figure(100)
    plt.plot(x_values, irrigation_average_mean)
    plt.title('Average irrigation well drawdown')
    plt.ylabel('Average depth to Well water of irrigation wells')
    plt.show()


    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, 
                      names=cols, low_memory=False).fillna(-99)
    df = df[df.county=='Tulare']

    # first: what crops are highest value total (top 10 in 2016)
    print(df[df.index=='2016'].sort_values(by='value', ascending=False).head(10))

    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))

    df_TM = df[df.crop=='TANGERINES & MANDARINS']
    df_almonds = df[df.crop=='ALMONDS ALL']
    df_oranges = df[df.crop=='ORANGES NAVEL']
    df_table_grapes = df[df.crop=='GRAPES TABLE']
    df_pistachios = df[df.crop=='PISTACHIOS']
    df_corn_silage = df[df.crop=='CORN SILAGE']
    # df_corn_silage[['acres','ppu']].astype(float).plot(secondary_y='ppu')

    TM_years = pd.to_datetime(df_TM.index).year
    oranges_years = pd.to_datetime(df_oranges.index).year
    almonds_years = pd.to_datetime(df_almonds.index).year
    grapes_years = pd.to_datetime(df_table_grapes.index).year
    pistachios_years = pd.to_datetime(df_pistachios.index).year
    corn_years = pd.to_datetime(df_corn_silage.index).year

    TM_acres = np.array(df_TM.acres.values)
    corn_acres = np.array(df_corn_silage.acres.values)
    almonds_acres = np.array(df_almonds.acres.values)
    grapes_acres = np.array(df_table_grapes.acres.values)
    pistachios_acres = np.array(df_pistachios.acres.values)
    orange_acres = np.array(df_oranges.acres.values)


    corn_water_per_acre = 3.1  #(USDA 2013)
    orchards_water_per_acre = 2.7  #(USDA 2013)
    grapes_water_per_acre = 3.0  #(Vasquez et al. 2007)

    TM_water = TM_acres * orchards_water_per_acre / 1000 # TAF
    corn_water = corn_acres * corn_water_per_acre / 1000 # TAF
    almonds_water = almonds_acres * orchards_water_per_acre / 1000  # TAF
    grapes_water = grapes_acres * grapes_water_per_acre / 1000  # TAF
    pistachios_water = pistachios_acres * orchards_water_per_acre / 1000  # TAF
    oranges_water = orange_acres * orchards_water_per_acre / 1000  # TAF


    new_x_vals = x_values.year 

    plt.figure(101)
    plt.title('Primary Crops Grown in Tulare County and Average Well Depth')
    plt.subplot(2, 1, 1)

    plt.plot(TM_years, TM_water, label = 'tangerines and mandarins')
    plt.plot(oranges_years, oranges_water, label = 'oranges')
    plt.plot(almonds_years, almonds_water, label='almonds') #, c='r' )
    plt.plot(grapes_years, grapes_water, label = 'grapes')
    plt.plot(pistachios_years, pistachios_water, label = 'pistachios')
    plt.plot(corn_years, corn_water, label = 'corn')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Total Water Used [TAF]')

    plt.subplot(2, 1, 2)
    plt.plot(new_x_vals, irrigation_average_mean, label = 'Irrigation Drawdown')
    plt.ylabel('irrigation well average depth')
    plt.legend()

    plt.figure(105)
    plt.title('Primary Crops Grown in Tulare County')
    plt.plot(TM_years, TM_acres, label = 'tangerines and mandarins')
    plt.plot(oranges_years, orange_acres, label = 'oranges')
    plt.plot(almonds_years, almonds_acres, label='almonds') #, c='r' )
    plt.plot(grapes_years, grapes_acres, label = 'grapes')
    plt.plot(pistachios_years, pistachios_acres, label = 'pistachios')
    plt.plot(corn_years, corn_acres, label = 'corn')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Acres')  
    plt.show()


pdb.set_trace()

