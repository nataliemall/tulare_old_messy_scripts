 # Well data analysis - Change in groundwater levels 
# https://www.casgem.water.ca.gov/OSS/(S(q4ytwloehqreoahtlcw0z1ia))/Public/SearchWells.aspx
# takes data received from CASGEM and compiles it to plot lift heights and groundwater changes over time for all of  Tulare Lake Basin


import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import pdb
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from tqdm import tqdm  # for something in tqdm(something something):

def get_CASGEM_data():
    header_data = pd.read_csv('casgem_GW_data/gst_file.csv', index_col=0, parse_dates=True)
    # From header_data GST_file: Extract all the data where "COUNTY_NAME" = Tulare  or Tulare Lake
    tulare_county_headers = header_data.loc[lambda df: df.COUNTY_NAME == 'Tulare', :]  # Prints x? rows 
    # tulare_county_headers2 = tulare_county_headers.loc[lambda df: df.CASGEM_STATION_USE_DESC == 'Irrigation', :]  # Prints x? rows 
    tulare_county_IDs_all = tulare_county_headers.index.tolist()        # all IDs in Tulare County 

    include_elevation_changes = 1 # include elevation changes calculated in changes_well_data.py 
    
    def data_with_annual_lift_changes():
        try: 
            well_data_tulare_only = pd.read_csv('well_data_tulare_only2.csv', parse_dates=['MEASUREMENT_DATE'])
        except:   ############################# Creates the file trimmed to TLB only IF the file does not already exist ###########
            print('The TLB overall file wasn''t in the searched folder')
            well_data = pd.read_csv('casgem_GW_data/gwl_file.csv', 
                    encoding = 'latin1', parse_dates=['MEASUREMENT_DATE'],
                    date_parser = lambda x:pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')) #, parse_dates=True)
             
            # locate data at the extracted CASGEM ID values
            well_data_tulare_only = well_data[well_data['CASGEM_STATION_ID'].isin(tulare_county_IDs_all)] # [113680 rows x 17 columns]

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
        try:   # Runs this if data already exists in correct folder 
        # if include_elevation_changes == 1:  # CSV includes elevation changes from year prior 
            # well_data_tulare_only = pd.read_csv('well_data_tulare_only2.csv', parse_dates=['MEASUREMENT_DATE'])
        # else: 
            well_data_tulare_only = pd.read_csv('well_data_tulare_only.csv', parse_dates=['MEASUREMENT_DATE']) #[113680 rows x 18 columns]
        
        except:   ############################# Creates the file trimmed to TLB only IF the file does not already exist ###########
            print('The TLB overall file wasn''t in the searched folder')
            well_data = pd.read_csv('casgem_GW_data/gwl_file.csv', 
                    encoding = 'latin1', parse_dates=['MEASUREMENT_DATE'],
                    date_parser = lambda x:pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')) #, parse_dates=True)
                 
            # locate data at the extracted CASGEM ID values
            well_data_tulare_only = well_data[well_data['CASGEM_STATION_ID'].isin(tulare_county_IDs_all)] # [113680 rows x 17 columns]
            well_data_tulare_only.to_csv('well_data_tulare_only.csv')
            print('Made new file named "well_data_tulare_only.csv", which does not contain GW lift change')
        return well_data_tulare_only 

    if include_elevation_changes == 1:
        pdb.set_trace()
        well_data_tulare_only = data_with_annual_lift_changes()
    else:
        well_data_tulare_only = data_without_annual_lift_changes()

    return well_data_tulare_only, tulare_county_headers, tulare_county_IDs_all


well_data_tulare_only, tulare_county_headers, tulare_county_IDs_all = get_CASGEM_data()
pdb.set_trace()

# variables for comparing historical with 2012 data: 
starting_datetime = '2012-07-01 00:00:00'   # ideally this will be variable  
tulare_wells10 = well_data_tulare_only.loc[well_data_tulare_only['MEASUREMENT_DATE'] >= '2012-07-01 00:00:00', :]
tulare_wells11 = tulare_wells10.loc[tulare_wells10['MEASUREMENT_DATE'] <= '2012-11-01 00:00:00', :]             # All the dates after a summer irrigation season (July - November)
tulare_wells_1980 = well_data_tulare_only.loc[well_data_tulare_only['MEASUREMENT_DATE'] >= '1960-07-01 00:00:00', :]
tulare_wells_1980_1985 = tulare_wells_1980.loc[tulare_wells_1980['MEASUREMENT_DATE'] <= '1985-11-01 00:00:00', :]  # All measurement dates between 1960 and 1985

tulare_wells13 = tulare_wells11[0:1] # starts dataframe of well data 

station_ids = tulare_wells11.CASGEM_STATION_ID.values.tolist()
headers_selected_timeperiod = tulare_county_headers[tulare_county_headers.index.isin(station_ids)]  # extracts headers only of the Tulare wells within the timeframe
tulare_wells16 = headers_selected_timeperiod.loc[headers_selected_timeperiod.index == tulare_county_IDs_all[0], :]   # starts dataframe of header data 

# pdb.set_trace()
missing_1980 = 0 # sanity check 
elevation_column = ['CASGEM_STATION_ID', 'ave_80_85']
water_level_ave_80_85 = pd.DataFrame(columns = elevation_column) # create dataframe column for the waterlevel change
array_80_85 = np.zeros(1000)
array_80_85_wellIDs = np.zeros(1000, dtype=np.int32)

############ ATTEMPT TO MAKE FUNCTION #############
# pdb.set_trace()

def average_depth_year_comparison(year_evaluating):

    # year = year_evaluating - 1
    water_year_start = str(year_evaluating -1) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'
    year_prior_start =  str(year_evaluating - 2) + '-10-01 00:00:00'
    year_prior_end =  str(year_evaluating - 1) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(water_year_start).year)
    ending = str(pd.to_datetime(year_prior_end).year)

    year_range_string = ('Water level difference in October',starting,'through September', ending)

    lats = np.empty(len(tulare_county_IDs_all))
    lats[:] = np.nan
    lons = np.empty(len(tulare_county_IDs_all))
    lons[:] = np.nan
    RP_difference = np.empty(len(tulare_county_IDs_all))
    RP_difference[:] = np.nan
    county_id5 = np.empty(len(tulare_county_IDs_all))
    county_id5[:] = np.nan    

    well_iter = 0 
    for county_id in tqdm(tulare_county_IDs_all): 
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
        lat_test = tulare_county_headers.loc[tulare_county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = tulare_county_headers.loc[tulare_county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values

        RP_difference[well_iter] = RP_average - RP_average_prior  # If the water is depleting, this number should be increasing 
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


def average_depth_5year_comparison(year_evaluating):

    # year = year_evaluating - 1
    water_year_start = str(year_evaluating -6) + '-10-01 00:00:00'  # start of water year: Oct 1 of previos year 
    water_year_end = str(year_evaluating) + '-09-30 00:00:00'
    year_prior_start =  str(year_evaluating - 10) + '-10-01 00:00:00'
    year_prior_end =  str(year_evaluating  - 6) + '-09-30 00:00:00'

    starting = str(pd.to_datetime(year_prior_start).year)
    ending = str(pd.to_datetime(water_year_end).year)

    year_range_string = ('Water level difference in October',starting,'through September', ending)
    lats = np.empty(len(tulare_county_IDs_all))
    lats[:] = np.nan
    lons = np.empty(len(tulare_county_IDs_all))
    lons[:] = np.nan
    RP_difference = np.empty(len(tulare_county_IDs_all))
    RP_difference[:] = np.nan
    county_id5 = np.empty(len(tulare_county_IDs_all))
    county_id5[:] = np.nan

    well_iter = 0 
    for county_id in tqdm(tulare_county_IDs_all): 
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
        lat_test = tulare_county_headers.loc[tulare_county_headers.index == county_id,:] 
        lats[well_iter] = lat_test.LATITUDE.values

        lon_test = tulare_county_headers.loc[tulare_county_headers.index == county_id,:] 
        lons[well_iter] = lon_test.LONGITUDE.values
        county_id5[well_iter] = county_id

        RP_difference[well_iter] = RP_average - RP_average_prior  # If the water is depleting, this number should be increasing 
        if RP_difference[well_iter] > 100:  # takes out outliers
            RP_difference[well_iter] = np.nan
        # np.mean(water_year_evaluating.RP_READING)
        well_iter = well_iter + 1
        # pdb.set_trace()

    gw_array7 = np.vstack((county_id5, lats, lons, RP_difference))
    gw_array7 = np.transpose(gw_array7)
    gw_df7 = pd.DataFrame(gw_array7)
    gw_df7.columns = ['county_ID', 'latitudes', 'longitudes', 'RP_difference']
    gw_df7.set_index('county_ID')  # fix id value 
    gw_df7.to_csv('GW_change_2015.csv')
    # pdb.set_trace()

    return RP_difference, lats, lons, year_range_string, county_id5


plotting_test_2013 = 0
if plotting_test_2013 == 1: 
    RP_difference, lats, lons, date_range_string = average_depth_year_comparison(2013)

compiling_seasonal_averages = 1 # takes the data and compiles average RP_READING for each season (set equal to 1 if this hasn't already been done)
# doesn't currently work if set to zero (some variables won't be defined)
if compiling_seasonal_averages == 1: 
    # Variables for yearly averages data 
    seasonal_average = np.empty((len(tulare_county_IDs_all),158,))
    seasonal_average[:] = np.nan
    seasonal_average[0] = 0  
    year_range = np.arange(1940,2018)

# import_seasonal_averages = 1
if compiling_seasonal_averages == 0:
    imported_seasonal_averages = np.loadtxt('seasonal_averages.csv', delimiter=',')  # array of all 2147 wells in Tulare county, averaged by season 

# pdb.set_trace()
v = 0 
plt_legend = np.ones(50)

# saving irrigation averages 
X_irrigation = np.empty([180,158])
X_irrigation[:] = np.nan
Y_irrigation = np.empty([180,158])
Y_irrigation[:] = np.nan
r = 0 

well_iter = 0 
# Iterates through each of the well IDs in Tulare County 

def seasonal_and_other_comparisons(well_iter, tulare_wells13, missing_1980, tulare_wells16, v, r):
    for county_id in tqdm(tulare_county_IDs_all):   # runs through data for all Tulare County IDs 
        #Data for this specific well ID: 
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]

        if compiling_seasonal_averages == 1:  # Will iterate through the years if compilation hasn't already been done
            # Yearly averages data collection: 
            season_iter = 0 
            for year in year_range:
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
                seasonal_average[well_iter, season_iter] = average_rainy

                # Dry season 
                tulare_well_ID_year_dry  = tulare_wells90.loc[tulare_wells90['MEASUREMENT_DATE'].dt.year == year, :]
                tulare_well_ID_year_dry  = tulare_well_ID_year_dry.loc[tulare_well_ID_year_dry['MEASUREMENT_DATE'].dt.month > 4, :]  # locate data betwwen october and May year + 1
                tulare_well_ID_year_dry  = tulare_well_ID_year_dry.loc[tulare_well_ID_year_dry['MEASUREMENT_DATE'].dt.month < 10, :]  # locate data betwwen october and May year + 1

                dry_season_values = tulare_well_ID_year_dry.RP_READING.values 

                if dry_season_values.size > 0:
                    seasonal_average[well_iter, season_iter + 1] = np.mean(tulare_well_ID_year_dry.RP_READING)

                season_iter = season_iter + 2

            well_iter = well_iter + 1  
        else:
            well_iter = well_iter + 1 

        # pdb.set_trace()
        skip_id = 0 
        skip_id2 = 0

        tulare_wells80 = tulare_wells_1980_1985.loc[tulare_wells_1980_1985['CASGEM_STATION_ID'] == county_id, :]
        tulare_wells81 = tulare_wells80.RP_READING.mean()  # takes only first measurement in the time period 

        if tulare_wells80.empty:               # does this mean all the values are empty? 
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
            tulare_wells15 = tulare_county_headers.loc[tulare_county_headers.index == county_id, :]
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
        
        # Plotting elevation change from year prior: 
        tulare_wells90 = well_data_tulare_only.loc[well_data_tulare_only['CASGEM_STATION_ID'] == county_id, :]
        water_level_change2 = tulare_wells90.change_from_year_prior
        # tulare_wells13 = pd.merge(tulare_wells12, tulare_wells13, how='outer')  # merges ----  contains depths for all wells in October 2012 
        # pdb.set_trace()
        gw_changes_by_year = 0    # Plots elevations changes  
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

        plot_change_by_basin = 0
        if plot_change_by_basin ==1:
            plt.figure(55) 
            basin_label1 = tulare_county_headers.BASIN_DESC[county_id]
            dats_fig_55 = tulare_wells90.MEASUREMENT_DATE
            if tulare_county_headers.BASIN_DESC[county_id] == 'Tule': 
                if plt_legend[40] ==1:
                    plt.plot(dats_fig_55, water_level_change2, linestyle = '', marker = '.', c = 'm')
                    # plt.scatter(x_values, y_values, c = 'g', alpha=0.7, label=basin_label)
                    plt_legend[40] = 0
                else: 
                    plt.plot(dats_fig_55, water_level_change2, linestyle = '', marker = '.', c = 'm')
            elif tulare_county_headers.BASIN_DESC[county_id] == 'Kaweah': 
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
        def import_seasonal_average(r):

            # x_values = np.arange(1939.5,2018.5, 0.5)                          # What is a better way? - Pandas resample
            x_values = pd.date_range(start='Sep-1939', end=' Sep-2018', freq='6M')
            # x_values = tulare_wells90.MEASUREMENT_DATE
            y_values = imported_seasonal_averages[well_iter-1,:]
            plot_by_use = 1  #Plot averages by well use type 
            if plot_by_use == 1: 
                plt.figure(51)
                welltype_label = tulare_county_headers.CASGEM_STATION_USE_DESC[county_id]
                # array(['Unknown', 'Irrigation', 'Residential', 'Observation', 'Other',
                 #      'Stockwatering', 'Industrial'], dtype=object)
                if tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Irrigation': 

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
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Residential': 
                    if plt_legend[11] ==1:
                        plt.scatter(x_values, y_values, c = 'b', alpha=0.5, label=welltype_label)
                        plt_legend[11] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'b', alpha = 0.5)
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Observation': 
                    if plt_legend[12] ==1:
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3, label=welltype_label)
                        plt_legend[12] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'c', alpha = 0.3)
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Other': 
                    if plt_legend[13] ==1:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3, label=welltype_label)
                        plt_legend[13] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'm', alpha = 0.3)
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Stockwatering': 
                    if plt_legend[14] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.7, label=welltype_label)
                        plt_legend[14] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha = 0.3)
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Industrial': 
                    if plt_legend[15] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=1, label=welltype_label)
                        plt_legend[15] = 0          
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha = 1) 
                elif tulare_county_headers.CASGEM_STATION_USE_DESC[county_id] == 'Unknown': 
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
                basin_label = tulare_county_headers.BASIN_DESC[county_id]
                # if tulare_county_headers.CASGEM_STATION_USE_DESC[well_iter-1] == 'Irrigation': 
                #   print('this iteration is an irrigation well')   # Help here 
                
                if tulare_county_headers.BASIN_DESC[county_id] == 'Tulare Lake': 
                    if plt_legend[1] ==1:
                        plt.scatter(x_values, y_values, c = 'g', alpha=0.7, label=basin_label)
                        plt_legend[1] = 0
                    else: 
                        plt.scatter(x_values, y_values, c = 'g', alpha=0.7)
                elif tulare_county_headers.BASIN_DESC[county_id] == 'Kern County': 
                    if plt_legend[2] ==1:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.3, label=basin_label)
                        plt_legend[2] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'y', alpha=0.3)
                elif tulare_county_headers.BASIN_DESC[county_id] == 'Tule':    # mostly this basin
                    if plt_legend[3] ==1:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3, label=basin_label)
                        plt_legend[3] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'm', alpha=0.3)
                elif tulare_county_headers.BASIN_DESC[county_id] == 'Westside': 
                    if plt_legend[4] ==1:
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3, label=basin_label)
                        plt_legend[4] = 0
                    else: 
                        plt.scatter(x_values, y_values, c = 'c', alpha=0.3)
                elif tulare_county_headers.BASIN_DESC[county_id] == 'Kaweah':  # and this basin
                    if plt_legend[5] ==1:
                        plt.scatter(x_values, y_values, c = 'r', alpha = 0.3,label=basin_label)
                        plt_legend[5] = 0
                    else:
                        plt.scatter(x_values, y_values, c = 'r', alpha=0.3) 
                elif tulare_county_headers.BASIN_DESC[county_id] == 'Kings': 
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

            return r
        if compiling_seasonal_averages == 0: 
            r = import_seasonal_average(r)
    # Save seasonal_averages to a .csv file

    return seasonal_average, well_iter, tulare_wells13

seasonal_average, well_iter, tulare_wells13, tulare_wells16 = seasonal_and_other_comparisons(well_iter, tulare_wells13, missing_1980, tulare_wells16, v, r)
if compiling_seasonal_averages == 1:
    # csv.writer()
    np.savetxt("seasonal_averages.csv", seasonal_average, delimiter=",")
    np.savetxt("seasonal_averages_corresponding_IDs.csv", tulare_county_IDs_all, delimiter=",")

s1 = tulare_wells16.SITE_CODE  
s2 = tulare_wells13.SITE_CODE
s1 == s2   # sanity check 

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
change_year_before = tulare_wells18.change_from_year_prior.values # FIX THIS - Should use tulare_wells2 or tulare_wells_oct # depends on date entered for recent timeframe - tulare_wells10  - originally tulare_wells18
lats = tulare_wells18.LATITUDE.values
lons = tulare_wells18.LONGITUDE.values

############# plotting the GW change  #############
groundwater_map1 = 0  # Groundwater plotting of (historical data average - 2012 levels)
if groundwater_map1 == 1:
    # create map background  
    plt.figure(3)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='i', area_thresh=25000.0)

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 5000, dpi=5000, verbose= True)
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')

    x,y = m(lons,lats)
    variable_object = plt.cm.get_cmap('RdYlGn')
    m.scatter(x,y,s=30,c=water_drawdown_changes, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()

    # plt.savefig('map.svg')
    plt.show()
    # pdb.set_trace()

groundwater_map2 = 0  # Groundwater plotting of changes in water level from year prior -  for a certain year - set-up for only years with historical data
# currently using change_year_before file 
if groundwater_map2 == 1:
    # create map background  
    plt.figure(3)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='i', area_thresh=25000.0)

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 5000, dpi=500, verbose= True)
    # m.arcgisimage(service='World_Street_Map', xpixels = 18000, dpi=4000, verbose= True)
    # m.arcgisimage(service='World_Transportation', xpixels=1000, dpi=75, verbose= True)
    # m.drawcounties(linewidth=0.1, color='gray')
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')
    # load reservoir data and scatterplot (lat,lon,elev)
    # df = pd.read_csv('all-reservoirs.csv')
    # lons = df.Longitude.values
    # lats = df.Latitude.values
    # elev = df.Elevation.values

    x,y = m(lons,lats)

    # sdlfkj = mplc.Colormap('RdYlBu')
    variable_object = plt.cm.get_cmap('RdYlGn')
    m.scatter(x,y,s=30,c=change_year_before, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()

    # add in demographics eventually?

    # plt.savefig('map.svg')
    plt.show()
    # pdb.set_trace()

groundwater_map3 = 0
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

groundwater_map7 = 0 # - attempt2  set colorbar scale plots the average for the 5 years leading up, and the previous 5
if groundwater_map7 ==1:
    RP_difference, lats, lons, range_string, county_id5t = average_depth_5year_comparison(2015)

    print(range_string)
    # create map background  
    plt.figure(16)
    m = Basemap(llcrnrlon=-125.6, llcrnrlat=31.7, urcrnrlon=-113.2,
                urcrnrlat=43.2, projection='cyl', resolution='f', area_thresh=25000.0)  # change resolution to 'high' l

    m.drawmapboundary(fill_color='steelblue', zorder=-99)
    m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 10000, dpi=1000, verbose= True)
    m.drawstates(zorder=6, color='gray')
    m.drawcountries(zorder=6, color='gray')
    m.drawcoastlines(color='gray')

    x,y = m(lons,lats)
    variable_object = plt.cm.get_cmap('bwr')
    m.scatter(x,y,s=30,c=RP_difference, marker='o', edgecolor='None', cmap=variable_object)
    plt.colorbar()
    plt.title('2010 - 2015 Groundwater Level Average Compared with 2005 - 2010')
    plt.clim(-100,65)
    plt.savefig("comparison_GW.png", dpi = 300)
    plt.show()
    pdb.set_trace()


attempt_all_irrigation = 1  #plots all months of irrigation averages by season 
if attempt_all_irrigation ==1:
    plt.plot(X_irrigation[1,:], Y_irrigation[1,:])


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



