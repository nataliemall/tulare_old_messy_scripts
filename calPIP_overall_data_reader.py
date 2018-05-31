# Read a=nd graph the overall calPIP data 

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



def extract_calPIP_data():  # extrace calPIP data from file 
    overall_data = pd.read_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results.csv', sep = '\t', index_col =0) 
    crop_time_series = overall_data.transpose()
    crop_time_series.index = crop_time_series.index.astype('float')
    crop_time_series.index = crop_time_series.index.to_series().apply(lambda x: int(x))
    crop_time_series.index = pd.to_datetime(crop_time_series.index, format="%Y").year

    highest_acres_calPIP = overall_data.sort_values(by='2015.0', ascending=False).head(10)
    return crop_time_series, overall_data, highest_acres_calPIP



# highest_acres_calPIP.index 
       #  ['WHEAT (FORAGE - FODD acres', 'CORN (FORAGE - FODDE acres',
       # 'ORANGE (ALL OR UNSPE acres', 'ALMOND acres',
       # 'PISTACHIO (PISTACHE  acres', 'GRAPES acres',
       # 'ALFALFA (FORAGE - FO acres', 'WALNUT (ENGLISH WALN acres',
       # 'TANGERINE (MANDARIN, acres', 'SORGHUM (FORAGE - FO acres'],

# pdb.set_trace()
def extract_commissioner_data():
    cols = ['year', 'comcode', 'crop', 'coucode', 'county', 'acres', 'yield', 'production', 'ppu', 'unit', 'value']
    df = pd.read_csv('CA-crops-1980-2016.csv', index_col=0, parse_dates=True, names=cols, low_memory=False).fillna(-99)
    df = df[df.county=='Tulare']

    # first: what crops are highest value total (top 10 in 2016)
    print(df[df.index=='2016'].sort_values(by='value', ascending=False).head(10))
    highest_valued = df[df.index=='2016'].sort_values(by='value', ascending=False).head(10)
    # crops of greatest acreage
    print(df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10))
    highest_acres = df[df.index=='2016'].sort_values(by='acres', ascending=False).head(10)

    return df, highest_valued, highest_acres


def crop_type_data(crop):
    df_crop = df[df.crop==crop]
    return df_crop



def plot_calPIP_data(crop_calPIP_data, crop_county_data, title):
    plt.plot(crop_calPIP_data, label = 'calPIP data')
    plt.plot(crop_county_data.acres, label = 'County commissioner data')
    plt.xlabel(title)
    plt.ylabel('acres')
    plt.legend()
    # plt.show()
    title2 = title 

def get_county_data(county_crop_name):
    county_crop = df[df.crop==county_crop_name]  #crop_type_data(county_crop_name)

    county_crop.index = county_crop.index.astype('float')
    county_crop.index = county_crop.index.to_series().apply(lambda x: int(x))
    crop_county_data = county_crop
    return crop_county_data




def plot_alfalfa():
    crop_calPIP_data = crop_time_series['ALFALFA (FORAGE - FO acres']


        #           MILK MARKET FLUID
        #               ORANGES NAVEL
        # CATTLE & CALVES UNSPECIFIED
        #                GRAPES TABLE
        #      TANGERINES & MANDARINS
        #                  PISTACHIOS
        #                 ALMONDS ALL
        #                 CORN SILAGE
        #            ORANGES VALENCIA
        #                      SILAGE

        #     2016        PASTURE RANGE
        # 2016               SILAGE
        # 2016          CORN SILAGE
        # 2016    PASTURE IRRIGATED
        # 2016        ORANGES NAVEL
        # 2016          ALMONDS ALL
        # 2016           PISTACHIOS
        # 2016          HAY ALFALFA
        # 2016      WALNUTS ENGLISH
        # 2016         GRAPES TABLE
    county_crop_name = 'HAY ALFALFA'
    county_alfalfa_data = get_county_data(county_crop_name)

    crop_county_data = county_alfalfa_data
    title = 'Alfalfa acreage'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_almonds():
    crop_calPIP_data = crop_time_series['ALMOND acres']

    county_crop_name = 'ALMONDS ALL'
    county_almond_data = get_county_data(county_crop_name)

    crop_county_data = county_almond_data
    title = 'Almonds acreage'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_tangerines_mandarins():
    crop_calPIP_data = crop_time_series['TANGERINE (MANDARIN, acres']

    county_crop_name = 'TANGERINES & MANDARINS'
    county_tang_data = get_county_data(county_crop_name)

    crop_county_data = county_tang_data
    title = 'Tangerines and Mandarins acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_grapes():
    crop_calPIP_data = crop_time_series['GRAPES acres']

    county_crop_name = 'GRAPES TABLE'
    county_grape_data = get_county_data(county_crop_name)
    county_crop_name2 = 'GRAPES RAISIN'
    county_grape_data2 = get_county_data(county_crop_name2)

    crop_county_data = county_grape_data + county_grape_data2  # Add up raisins and table grapes 
    title = 'Grapes acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_wine_grapes():
    crop_calPIP_data = crop_time_series['GRAPES, WINE acres']

    county_crop_name = 'GRAPES WINE'
    county_wine_grape_data = get_county_data(county_crop_name)

    crop_county_data = county_wine_grape_data
    title = 'Wine grapes acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_oranges():
    crop_calPIP_data = crop_time_series['ORANGE (ALL OR UNSPE acres']

    county_crop_name = 'ORANGES NAVEL'
    county_crop_name2 = 'ORANGES VALENCIA'
    county_orange_data = get_county_data(county_crop_name)
    county_orange_data2 = get_county_data(county_crop_name2)

    crop_county_data = county_orange_data + county_orange_data2  # add up Navel and Valencia oranges 
    title = 'Oranges acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_beans():
    # crop_calPIP_data1 = crop_time_series['BEAN, BROAD (FAVA, H acres']
    # crop_calPIP_data2 = crop_time_series['BEANS, SUCCULENT (OT acres']
    crop_calPIP_data3 = crop_time_series['BEANS, DRIED-TYPE acres']
    crop_calPIP_data4 = crop_time_series['BEANS (ALL OR UNSPEC acres']
    
    crop_calPIP_data = crop_calPIP_data3 + crop_calPIP_data4
    
    county_crop_name = 'BEANS DRY EDIBLE UNSPEC.'
    county_crop_name2 = 'BEANS DRY EDIBLE UNSPECIFIED'

    county_bean_data = get_county_data(county_crop_name)
    county_bean_data2 = get_county_data(county_crop_name2)

    crop_county_data = county_bean_data
    title = 'Dried beans acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.plot(county_bean_data2.acres, label = 'continued commissioner data')
    plt.show()
    return county_bean_data , county_bean_data2 

def plot_blueberries():
    crop_calPIP_data = crop_time_series['BLUEBERRY acres']

    county_crop_name = 'BERRIES BLUEBERRIES'
    county_blueberry_data = get_county_data(county_crop_name)

    crop_county_data = county_blueberry_data
    title = 'Blueberry acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_broccoli():
    crop_calPIP_data = crop_time_series['BROCCOLI acres']

    county_crop_name = 'BROCCOLI PROCESSING'
    county_broccoli_data = get_county_data(county_crop_name)

    county_crop_name2 = 'BROCCOLI UNSPECIFIED'
    county_broccoli_data2 = get_county_data(county_crop_name2)   

    county_crop_name = 'BROCCOLI FRESH MARKET'
    county_broccoli_data3 = get_county_data(county_crop_name)

    crop_county_data = county_broccoli_data
    title = 'Broccoli acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.plot(county_broccoli_data2.acres, label = 'BROCCOLI UNSPECIFIED')
    plt.plot(county_broccoli_data3.acres, label = 'BROCCOLI FRESH MARKET')
    plt.legend()
    plt.show()

def plot_cherries():
    crop_calPIP_data = crop_time_series['CHERRY acres']

    county_crop_name = 'CHERRIES SWEET'
    county_cherry_data = get_county_data(county_crop_name)

    crop_county_data = county_cherry_data
    title = 'Cherries acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_olives():
    crop_calPIP_data = crop_time_series['OLIVE (ALL OR UNSPEC acres']

    county_crop_name = 'OLIVES'
    county_olive_data = get_county_data(county_crop_name)

    crop_county_data = county_olive_data
    title = 'Olives acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

def plot_wheat():
    crop_calPIP_data1 = crop_time_series['WHEAT (FORAGE - FODD acres']
    crop_calPIP_data2 = crop_time_series['WHEAT, GENERAL acres']
    crop_calPIP_data = crop_calPIP_data1 + crop_calPIP_data2

    county_crop_name = 'WHEAT ALL'
    county_wheat_data = get_county_data(county_crop_name)

    crop_county_data = county_wheat_data
    title = 'Wheat acreage comparison'
    plot_calPIP_data(crop_calPIP_data, crop_county_data, title)
    plt.show()

#extract calPIP data from file:
crop_time_series, overall_data, highest_acres_calPIP = extract_calPIP_data()

#extract commissioner data 
df, highest_valued, highest_acres = extract_commissioner_data()
print(highest_valued.crop)

plot_wheat()
plot_olives()
plot_wine_grapes()
plot_cherries()
plot_broccoli()
plot_blueberries()
county_bean_data , county_bean_data2 = plot_beans()
pdb.set_trace()
plot_alfalfa()
plot_almonds()
plot_tangerines_mandarins()
plot_grapes() 
plot_oranges()
pdb.set_trace()

crop = 'TANGERINES & MANDARINS'
df_crop = crop_type_data(crop)



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




