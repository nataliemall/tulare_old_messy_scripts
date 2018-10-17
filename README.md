# Tulare Lake Basin's Shift from Annual to Permanent Crops 

Plotting the expansion of perennial crops in the southern central valley. 
Implications for Agricultural Water Shortage
Exploring trends from 1974 - 2016


## Antiquated repository - replaced as of October 2018 
### Refer to repository crop_acreages_CA_DPR_reports
Part 1: Download data at ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/
1. Unzip each folder from 1974-2016 (e.g. pur1978.zip)
2. save each folder as pur_data_raw/pur<year>   ( e.g. pur_data_raw/pur1975) 

Part 2: Clean the data -  Cleans up bad data and compiles data columns to create a comtrs value for each permit
1. Download clean_calPIP_data.py to the same folder that contains the pur_data_raw folder
2. Run the clean_calPIP_data.py script

Part 3: Compile the data by 1-mile section
1. Download compile_data_by_comtrs.py to the same folder as the previous two parts
2. Run the compile_data_by_comtrs.py script

Part 4: Create graphs comparing County Commissioner data with calPUR dataset
1. Run calPUR_county_comparison.py

Part 5, option a: Create several graphs for a chosen irrigation district or county within Tulare Lake Basin
1. Run acreage_calc_plots_single_irrigation_district.py 

Part 5, option b: Create a specific graph for all irrigation districts within the Tulare Lake Basin








### pur_data_compiler.py 
** Step-by-Step of one giant script; becoming obsolete starting late September 2018 ** 
Step 1: add_comtrs functions 
Add the comtrs values to each entry in the calPUR dataset. This has already been done and would only need repeating for debugging purposes. 

Step 2: compile_data_by_comtrs function 
Calls the calculate_acres functions for each year in the dataset. Calls different functions depending on if the data is pre-1990 or not.  This is due to a change in the way the data is stored in the calPUR archives and a change in the column labels starting in 1990. 

Step 3: retrieve_data_for_irrigation_disrict function 
Calls the respective file saved in irrigation_districts_with_comtrs that contains a list of COMTRS values within the chosen irrigation district 
Groups the data for each year by tree crop or annual crop 
Normalizes the data by forcing the total acreage in each COMTRS section to be 640 acres (the standard size of the 1-square-mile sections)
Saves file as cal_PUR_data<irrigation district>.csv 

Step 4: county_commissioner_data function
Extracts and sorts data from 'CA-crops-1980-2016.csv', which was compiled from the county commissioner spreadsheets 

Step 5: load_calPIP_data_all_years function
Loads the calPIP data compiled in a previous function (calPIP_overall_data_reader.py and calPIP_all_crops_compiler.py)  

Step 6: plot_data_comparison function
For any of the 4 counties, plots a comparison of the calPUR, calPIP, and county commissioner data


![perennial crop expansion](https://raw.githubusercontent.com/nataliemall/tulare_git_repo/master/abstract_figure_mall.png)


## Other tools:

### Processing the calPIP data (years 1990-2016 only):
Part 1: Download the data at https://calpip.cdpr.ca.gov/county.cfm 
1. Select desired counties (Fresno, Kern, Kings, and Tulare required for the following scripts)
2. Select desired year
3. Click 'Format Output'
4. Ensure 'AMOUNT_PLANTED', 'COUNTY_NAME', 'COMTRS', and 'SITE_NAME' are listed under 'Output Columns Selected:'
5. Click 'Submit Query'
6. Enter email address and click 'Send Query Now'
7. Save as 'calPIP_includes_crop_areas/calPIP<year>.csv'  e.g. 'calPIP_includes_crop_areas/calPIP2004.csv'
8. Repeat 35 times! Change desired year each time (1980 - 2016)

Part 2: Run calPIP_all_crops_compiler.py
Description: 
1. function that compiles data saved in calPIP_includes_crop_areas folder
2. sums calPIP data for all years 
3. saves compiled output files in calPIP_crop_acreages folder 
4. saves file (eg 2004crop_type_by_COMTRS.csv) for QGIS plotting 
5. saves summed yearly data for tulare county as overall_results.csv 

Part 3: Run calPIP_all_crops_compiler.py
Takes overall_results.csv and plots major crop types 



Repository contains 
1. Groundwater data, taken from CASGEM at https://www.casgem.water.ca.gov/OSS/(S(q4ytwloehqreoahtlcw0z1ia))/Public/SearchWells.aspx and processed via the groundwater_data_compiler.py file.

2. Crop data, taken from http://calpip.cdpr.ca.gov/main.cfm  and processed via the calPIP_all_crops_compiler.py file. 

3. Crop data taken from ftp://transfer.cdpr.ca.gov/pub/outgoing/pur_archives/ and processed via the pur_data_compiler.py file 

4. Aggregate crop data taken from county commissioner https://www.nass.usda.gov/Statistics_by_State/California/Publications/AgComm/index.php  
    - data taken for comparison 



