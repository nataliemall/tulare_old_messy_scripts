# Read a=nd graph the overall calPIP data 

import numpy as np 
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import matplotlib.collections as collections
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


def make_timeseries_plots():
    plot_wheat()
    plot_olives()
    plot_wine_grapes()
    plot_cherries()
    plot_broccoli()
    plot_blueberries()
    county_bean_data , county_bean_data2 = plot_beans()
    # pdb.set_trace()
    plot_alfalfa()
    plot_almonds()
    plot_tangerines_mandarins()
    plot_grapes() 
    plot_oranges()
    pdb.set_trace()


def define_tree_crops(overall_data):  # selects which crops are tree and which are annuals 
    '''0 = other, 1 = tree crop, 2 = annual crop; 3 = rangeland'''

    # crop_names = pd.DataFrame()
    overall_with_tree_crop_column = overall_data
    crop_names = overall_data.index
    series = np.zeros(len(overall_with_tree_crop_column.index))
    overall_with_tree_crop_column['product_type'] = series
  
    #next step: go through the 292 crop types and define the tree crops 
    overall_with_tree_crop_column.product_type['ALFALFA (FORAGE - FO acres'] = 2 # alfalfa
    overall_with_tree_crop_column.product_type['ALMOND acres'] = 1 # almonds
    overall_with_tree_crop_column.product_type['APPLE acres'] = 1 # apple trees
    overall_with_tree_crop_column.product_type['APRICOT acres'] = 1 # apricot trees
    overall_with_tree_crop_column.product_type['AVOCADO (ALL OR UNSP acres'] = 1 # avocado trees
    overall_with_tree_crop_column.product_type['BARLEY (FORAGE - FOD acres'] = 2 # barley 
    overall_with_tree_crop_column.product_type['BARLEY, GENERAL acres'] = 2 # barley
    overall_with_tree_crop_column.product_type['BASIL (BUSH, GARDEN, acres'] = 2 # basil 
    overall_with_tree_crop_column.product_type['BEAN, BROAD (FAVA, H acres'] = 2 # beans
    overall_with_tree_crop_column.product_type['BEANS (ALL OR UNSPEC acres'] = 2 # beans
    overall_with_tree_crop_column.product_type['BEANS, DRIED-TYPE acres'] = 2 # beans
    overall_with_tree_crop_column.product_type['BEANS, SUCCULENT (OT acres'] = 2 # beans
    overall_with_tree_crop_column.product_type['BEETS, GENERAL acres'] = 2 # beets
    overall_with_tree_crop_column.product_type['BEETS, TABLE, RED, O acres'] = 2 # beets
    overall_with_tree_crop_column.product_type['BERMUDAGRASS (FORAGE acres'] = 3 # bermuda grass
    overall_with_tree_crop_column.product_type['BLACKBERRY acres'] = 2 # blackberry
    overall_with_tree_crop_column.product_type['BLUEBERRY acres'] = 2 # blueberry
    overall_with_tree_crop_column.product_type['BROCCOLI acres'] = 2 # broccoli
    overall_with_tree_crop_column.product_type['CABBAGE acres'] = 2 # cabbage
    overall_with_tree_crop_column.product_type['CANTALOUPE acres'] = 2 # cantaloupe 
    overall_with_tree_crop_column.product_type['CARROTS, GENERAL acres'] = 2 # carrots
    overall_with_tree_crop_column.product_type['CAULIFLOWER acres'] = 2 # cauliflower
    overall_with_tree_crop_column.product_type['CELERY, GENERAL acres'] = 2 # celery
    overall_with_tree_crop_column.product_type['CHERRY acres'] = 1 # cherry
    overall_with_tree_crop_column.product_type['CHESTNUT acres'] = 1 # chestnut
    overall_with_tree_crop_column.product_type['CHINESE RADISH_DAIKO acres'] = 2 # chinese radish 
    overall_with_tree_crop_column.product_type['CHRISTMAS TREE PLANT acres'] = 1 # christmas tree
    overall_with_tree_crop_column.product_type['CILANTRO (CHINESE PA acres'] = 2 # cilantro
    overall_with_tree_crop_column.product_type['CITRUS FRUITS (ALL O acres'] = 1 # citrus fruit 
    overall_with_tree_crop_column.product_type['CORN (ALL OR UNSPEC) acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['CORN (FORAGE - FODDE acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['CORN, FIELD AND_OR F acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['CORN, FIELD, DENT (G acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['CORN, HUMAN CONSUMPT acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['CORN, SWEET (FRESH M acres'] = 2 # corn
    overall_with_tree_crop_column.product_type['COTTON (ALL OR UNSPE acres'] = 2 # cotton
    overall_with_tree_crop_column.product_type['COTTON (FIBER CROP)  acres'] = 2 # cotton
    overall_with_tree_crop_column.product_type['COTTON (FORAGE - FOD acres'] = 2 # cotton
    overall_with_tree_crop_column.product_type['COTTON, GENERAL acres'] = 2 # cotton
    overall_with_tree_crop_column.product_type['CUCUMBER (PICKLING,  acres'] = 2 # cucumber 
    overall_with_tree_crop_column.product_type['DAIRY FARM MILK HAND acres'] = 'test' # cucumber
    overall_with_tree_crop_column.product_type['EGGPLANT (ORIENTAL E acres'] = 2
    overall_with_tree_crop_column.product_type['FIG acres'] = 1
    overall_with_tree_crop_column.product_type['FORAGE - FODDER GRAS acres'] = 2
    overall_with_tree_crop_column.product_type['FOREST TREES, FOREST acres'] = 1
    overall_with_tree_crop_column.product_type['GARBANZOS (INCLUDING acres'] = 2
    overall_with_tree_crop_column.product_type['GARLIC acres'] = 2
    overall_with_tree_crop_column.product_type['GINGER (GINGER ROOT, acres'] = 2
    overall_with_tree_crop_column.product_type['GRAIN CROPS (ALL OR  acres'] = 2
    overall_with_tree_crop_column.product_type['GRAPEFRUIT acres'] = 1
    overall_with_tree_crop_column.product_type['GRAPES (ALL OR UNSPE acres'] = 1
    overall_with_tree_crop_column.product_type['GRAPES acres'] = 1
    overall_with_tree_crop_column.product_type['GRAPES, WINE acres'] = 1
    overall_with_tree_crop_column.product_type['GUAVA (SUBTROPICAL A acres'] = 1
    overall_with_tree_crop_column.product_type['HICKORY NUT acres'] = 1
    overall_with_tree_crop_column.product_type['JUJUBE acres'] = 1
    overall_with_tree_crop_column.product_type['KALE acres'] = 2
    overall_with_tree_crop_column.product_type['KIWI FRUIT acres'] = 1
    overall_with_tree_crop_column.product_type['KOHLRABI acres'] = 2
    overall_with_tree_crop_column.product_type['KUMQUAT (ALL OR UNSP acres'] = 1
    overall_with_tree_crop_column.product_type['LEGUMES & OTHER NONG acres'] = 2
    overall_with_tree_crop_column.product_type['LEMON acres'] = 1
    overall_with_tree_crop_column.product_type['LETTUCE, HEAD (ALL O acres'] = 2
    overall_with_tree_crop_column.product_type['LETTUCE, LEAF (ALL O acres'] = 2
    overall_with_tree_crop_column.product_type['LIME (MEXICAN LIME,  acres'] = 1
    overall_with_tree_crop_column.product_type['MANGO acres'] = 1
    overall_with_tree_crop_column.product_type['MELONS acres'] = 2
    overall_with_tree_crop_column.product_type['MUSTARD, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['N-GRNHS GRWN CUT FLW acres'] = 2
    overall_with_tree_crop_column.product_type['N-GRNHS GRWN PLANTS  acres'] = 2
    overall_with_tree_crop_column.product_type['N-GRNHS GRWN TRNSPLN acres'] = 2
    overall_with_tree_crop_column.product_type['N-OUTDR CONTAINER_FL acres'] = 2
    overall_with_tree_crop_column.product_type['N-OUTDR GRWN CUT FLW acres'] = 2
    overall_with_tree_crop_column.product_type['N-OUTDR GRWN TRNSPLN acres'] = 2
    overall_with_tree_crop_column.product_type['NECTARINE acres'] = 1
    overall_with_tree_crop_column.product_type['NUT CROPS, NUT TREES acres'] = 1
    overall_with_tree_crop_column.product_type['OATS (FORAGE - FODDE acres'] = 2
    overall_with_tree_crop_column.product_type['OATS, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['OKRA (GUMBO) acres'] = 2
    overall_with_tree_crop_column.product_type['OLIVE (ALL OR UNSPEC acres'] = 1
    overall_with_tree_crop_column.product_type['ONION (DRY, SPANISH, acres'] = 2
    overall_with_tree_crop_column.product_type['ORANGE (ALL OR UNSPE acres'] = 1
    overall_with_tree_crop_column.product_type['ORCHARDS (FRUIT_NUT  acres'] = 1
    overall_with_tree_crop_column.product_type['PAPAYA acres'] = 1
    overall_with_tree_crop_column.product_type['PARSLEY (LEAFY VEGET acres'] = 2
    overall_with_tree_crop_column.product_type['PASTURES (ALL OR UNS acres'] = 3
    overall_with_tree_crop_column.product_type['PEACH acres'] = 1
    overall_with_tree_crop_column.product_type['PEAR acres'] = 1
    overall_with_tree_crop_column.product_type['PEAR, ASIAN (ORIENTA acres'] = 1
    overall_with_tree_crop_column.product_type['PEAS, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['PECAN acres'] = 1
    overall_with_tree_crop_column.product_type['PEPPERS (CHILI TYPE) acres'] = 2
    overall_with_tree_crop_column.product_type['PEPPERS (FRUITING VE acres'] = 2
    overall_with_tree_crop_column.product_type['PERSIMMON acres'] = 1
    overall_with_tree_crop_column.product_type['PISTACHIO (PISTACHE  acres'] = 1
    overall_with_tree_crop_column.product_type['PLUM (INCLUDES WILD  acres'] = 1
    overall_with_tree_crop_column.product_type['PLUOT acres'] = 1
    overall_with_tree_crop_column.product_type['POME FRUITS (ALL OR  acres'] = 1
    overall_with_tree_crop_column.product_type['POMEGRANATE (MISCELL acres'] = 1
    overall_with_tree_crop_column.product_type['POMELO (SHADDOCK) (C acres'] = 1
    overall_with_tree_crop_column.product_type['POTATO (WHITE, IRISH acres'] = 2
    overall_with_tree_crop_column.product_type['PRUNE acres'] = 1
    overall_with_tree_crop_column.product_type['PUMPKIN acres'] = 2
    overall_with_tree_crop_column.product_type['QUINCE acres'] = 1
    overall_with_tree_crop_column.product_type['RADISH acres'] = 2
    overall_with_tree_crop_column.product_type['RANGELAND (ALL OR UN acres'] = 3
    overall_with_tree_crop_column.product_type['RUTABAGA (SWEDE, SWE acres'] = 2
    overall_with_tree_crop_column.product_type['RYE (ALL OR UNSPEC) acres'] = 2
    overall_with_tree_crop_column.product_type['RYEGRASS, PERENNIAL  acres'] = 2
    overall_with_tree_crop_column.product_type['SAFFLOWER, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['SMALL FRUITS (ALL OR acres'] = 1
    overall_with_tree_crop_column.product_type['SOIL APPLICATION, PR acres'] = 2 # 'SOIL APPLICATION, PREPLANT-OUTDOOR (SEEDBEDS,ETC.)'
    overall_with_tree_crop_column.product_type['SORGHUM (FORAGE - FO acres'] = 2
    overall_with_tree_crop_column.product_type['SORGHUM_MILO  GENERA acres'] = 2
    overall_with_tree_crop_column.product_type['SOYBEANS (ALL OR UNS acres'] = 2
    overall_with_tree_crop_column.product_type['SPINACH acres'] = 2
    overall_with_tree_crop_column.product_type['SQUASH (ALL OR UNSPE acres'] = 2   
    overall_with_tree_crop_column.product_type['SQUASH (SUMMER) acres'] = 2
    overall_with_tree_crop_column.product_type['SQUASH (ZUCCHINI) acres'] = 2
    overall_with_tree_crop_column.product_type['STONE FRUITS (ALL OR acres'] = 1
    overall_with_tree_crop_column.product_type['STRAWBERRY (ALL OR U acres'] = 2
    overall_with_tree_crop_column.product_type['SUDANGRASS (FORAGE - acres'] = 3
    overall_with_tree_crop_column.product_type['SUGARBEET, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['SUNFLOWER, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['TANGELO acres'] = 1
    overall_with_tree_crop_column.product_type['TANGERINE (MANDARIN, acres'] = 1
    overall_with_tree_crop_column.product_type['TARRAGON (ESTRAGON) acres'] = 2  # is a perrenial
    overall_with_tree_crop_column.product_type['TOMATILLO acres'] = 2
    overall_with_tree_crop_column.product_type['TOMATO acres'] = 2
    overall_with_tree_crop_column.product_type['TOMATOES, FOR PROCES acres'] = 2
    overall_with_tree_crop_column.product_type['TRITICALE (GRAIN CRO acres'] = 2 #wheat
    overall_with_tree_crop_column.product_type['TURNIP, GENERAL acres'] = 2
    overall_with_tree_crop_column.product_type['UNCULTIVATED AGRICUL acres'] = 3
    overall_with_tree_crop_column.product_type['VEGETABLES (ALL OR U acres'] = 2
    overall_with_tree_crop_column.product_type['WALNUT (ENGLISH WALN acres'] = 1
    overall_with_tree_crop_column.product_type['WATERMELONS acres'] = 2
    overall_with_tree_crop_column.product_type['WHEAT (FORAGE - FODD acres'] = 2
    overall_with_tree_crop_column.product_type['WHEAT, GENERAL acres'] = 2

    overall_with_tree_crop_column.loc[overall_with_tree_crop_column.product_type == 1].index
    tree_list = list(overall_with_tree_crop_column.loc[overall_with_tree_crop_column.product_type == 1].index)  # list of all tree crops 

    return overall_with_tree_crop_column, tree_list


# For year in range 1990:2016:
def group_by_crop_type(year): 
    filename = os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', (str(year) + 'files'), (str(year) + '_all_crops_compiled.csv') )
    year_all_crops_compiled = pd.read_csv(filename, sep = ',', index_col = 0)
    series = np.zeros(len(year_all_crops_compiled.index))
    year_all_crops_compiled['tree_crop_acreage'] = series
    year_all_crops_compiled['annual_crop_acreage'] = series
    year_all_crops_compiled['forage_crop_acreage'] = series
    COMTRS_list = year_all_crops_compiled.index
    for COMTRS in tqdm(COMTRS_list):
        tree_crops_summed = 0  # reset tree crop acreage to zero 
        annual_crops_summed = 0
        forage_crops_summed = 0 
        COMTRS_crop_breakdown = year_all_crops_compiled.loc[year_all_crops_compiled.index == COMTRS]
        COMTRS_crop_breakdown = COMTRS_crop_breakdown.transpose()

        # pdb.set_trace()
        for COMTRS_iter, value in enumerate(range(len(COMTRS_crop_breakdown) - 3)):   # only use [value] for the COMTRS_crop_breakdown subset 
            crop_name = COMTRS_crop_breakdown.index[value] 
            if overall_with_tree_crop_column.product_type[crop_name] == 1: # if it's a tree crop 
                # print(f'adding acreage from {crop_name} in the tree crops category')
                tree_crops_summed = tree_crops_summed + COMTRS_crop_breakdown[COMTRS][value] 
                # pdb.set_trace()
            if overall_with_tree_crop_column.product_type[crop_name] == 2: # if it's an annual crop 
                annual_crops_summed = annual_crops_summed + COMTRS_crop_breakdown[COMTRS][value] 
            if overall_with_tree_crop_column.product_type[crop_name] == 3: # if it's a forage crop 
                forage_crops_summed = forage_crops_summed + COMTRS_crop_breakdown[COMTRS][value] 
        # pdb.set_trace()
        year_all_crops_compiled.tree_crop_acreage[COMTRS] = tree_crops_summed
        year_all_crops_compiled.annual_crop_acreage[COMTRS] = annual_crops_summed
        year_all_crops_compiled.forage_crop_acreage[COMTRS] = forage_crops_summed

        # pdb.set_trace()

    total_tree_acreage = sum(year_all_crops_compiled.tree_crop_acreage)
    total_annual_acreage = sum(year_all_crops_compiled.annual_crop_acreage)
    total_forage_acreage = sum(year_all_crops_compiled.forage_crop_acreage)



    directory=os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', str(year) + 'files' )
    path_name = os.path.join(directory, (str(year) + '_complete_acreage_breakdown.csv')) 
    year_all_crops_compiled.to_csv(path_name, header = True, na_rep = '0', index = True)
    return total_tree_acreage, total_annual_acreage, total_forage_acreage, year_all_crops_compiled


def group_by_crop_type_all_year():   # Run this function if you want to recalculate the crop type grouping 
    all = {}
    total_tree_acreage_dict = {}
    tree_acreage_summed_for_year = np.zeros(len(range(1990,2017)))
    annual_acreage_summed_for_year = np.zeros(len(range(1990,2017)))
    forage_acreage_summed_for_year = np.zeros(len(range(1990,2017)))
    percent_tree_acreage_summed_for_year = np.zeros(len(range(1990,2017)))

    for year_iter, year in enumerate(tqdm(range(1990,2017))):
        total_tree_acreage, total_annual_acreage, total_forage_acreage, year_all_crops_compiled = group_by_crop_type(year) 
        all[year] = year_all_crops_compiled
        total_tree_acreage_dict[year] = total_tree_acreage
        tree_acreage_summed_for_year[year_iter] = total_tree_acreage
        annual_acreage_summed_for_year[year_iter] = total_annual_acreage
        forage_acreage_summed_for_year[year_iter] = total_forage_acreage
        percent_tree_acreage_summed_for_year[year_iter] = total_tree_acreage / (total_tree_acreage + total_annual_acreage + total_forage_acreage) 

        # pdb.set_trace()

    # Save
    np.save('all_crops_compiled_with_crop_types.npy', all) 
    np.savetxt('tree_acreage_summed_for_year.csv', tree_acreage_summed_for_year)
    np.savetxt('annual_acreage_summed_for_year.csv', annual_acreage_summed_for_year)
    np.savetxt('forage_acreage_summed_for_year.csv', forage_acreage_summed_for_year)
    np.savetxt('percent_tree_acreage_summed_for_year.csv', percent_tree_acreage_summed_for_year)

    # Load
    return all, total_tree_acreage_dict, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year

def load_crop_type_all_year():  # loads the data already calculated rather than recalculate it all 
    all = np.load('all_crops_compiled_with_crop_types.npy').item()
    tree_acreage_summed_for_year = np.loadtxt('tree_acreage_summed_for_year.csv')
    annual_acreage_summed_for_year = np.loadtxt('annual_acreage_summed_for_year.csv')
    forage_acreage_summed_for_year = np.loadtxt('forage_acreage_summed_for_year.csv')
    percent_tree_acreage_summed_for_year = np.loadtxt('percent_tree_acreage_summed_for_year.csv')

    return all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year
    # print(read_dictionary['hello']) # displays "world"



# year_list = total_tree_acreage_dict.keys()
# tree_acreage_list = total_tree_acreage_dict.values()
# plt.plot(year_list, tree_acreage_list)
# plt.plot(year_list, total_annual_acreage)


def plot_crop_comparison(tree_acreage_summed_for_year,annual_acreage_summed_for_year, forage_acreage_summed_for_year ): 
    year_list_array = np.arange(1990, 2017)
    fig, ax = plt.subplots()
    #plotted using the numpy arrays: 
    ax.plot(year_list_array[1:26], tree_acreage_summed_for_year[1:26], label = 'tree crop acreage')
    ax.plot(year_list_array[1:26], annual_acreage_summed_for_year[1:26], label = 'annual crop acreage')
    ax.plot(year_list_array[1:26], forage_acreage_summed_for_year[1:26], label = 'forage crop acreage')
    plt.legend()
    ax.set_title('Tulare County Crop Type Changes 1991 - 2016 with span_region ')
    plt.ylabel('Total acres planted')

    logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
    collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=2500000, where=(logic_rule), facecolor='orange', alpha=0.3)
    ax.add_collection(collection)
    logic_rule2 =  ( (year_list_array < 1995) & (year_list_array > 1990)  )   
    collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=2500000, where=(logic_rule2), facecolor='orange', alpha=0.3)
    ax.add_collection(collection2)

    plt.show()
    pdb.set_trace()


def crop_value_calcs(df): 
    # step 1: calculate average value of tree crops per acre  
    highest_valued = df[df.index=='2016'].sort_values(by='value', ascending=False).head(50)
    # nectarines = highest_valued[highest_valued.loc(highest_valued.crop == 'NECTARINES')]
    tree_crop_list = ['ORANGES NAVEL', 'GRAPES TABLE', 'TANGERINES & MANDARINS', 'PISTACHIOS', 'ALMONDS ALL', 'ORANGES VALENCIA',
                'WALNUTS ENGLISH', 'LEMONS ALL', 'NECTARINES', 'PLUMS','PEACHES FREESTONE','GRAPES RAISIN','GRAPES WINE',
                'KIWIFRUIT','BERRIES BLUEBERRIES','OLIVES','PLUMS DRIED','CHERRIES SWEET','GRAPEFRUIT ALL', 'PEACHES CLINGSTONE',
                'APRICOTS ALL', 'PERSIMMONS', 'POMEGRANATES', 'PECANS']
    annual_crop_list = ['CORN SILAGE', 'SILAGE', 'HAY ALFALFA', 'PASTURE IRRIGATED', 'COTTON LINT UNSPECIFIED',
             'VEGETABLES UNSPECIFIED', 'FIELD CROPS UNSPECIFIED', 'BEANS DRY EDIBLE UNSPECIFIED ', 'WHEAT ALL, HAY OTHER UNSPECIFIED',
             'CORN GRAIN', 'HAY SUDAN', 'BROCCOLI PROCESSING', 'BARLEY FEED', 'BEANS DRY EDIBLE UNSPEC.', 'WHEAT SEED', 'BARLEY UNSPECIFIED',
             'TOMATOES FRESH MARKET']
    # total_tree_crop_acreage = 0  # length of muber of years data is contained for (1984 - 2016)
    # total_weighted = 0
    tree_crop_revenue_per_acre = np.zeros(33) # length of muber of years data is contained for (1984 - 2016)
    annual_crop_revenue_per_acre = np.zeros(33) # length of muber of years data is contained for (1984 - 2016)
    year_list_array = np.zeros(33) # length of muber of years data is contained for (1984 - 2016)
    total_annual_crop_acreage = 0

    for num, year in tqdm(enumerate(range(1984,2017))):
        total_tree_crop_acreage = 0 
        total_annual_crop_acreage = 0 
        total_weighted_tree = 0
        total_weighted_annual = 0 
        for fruit in tqdm(tree_crop_list):
            # pdb.set_trace()
            tree_crop_revenue = df[df.crop == fruit].ppu *  ( df[df.crop == fruit]['yield'] )  # price/ acre 
            try:
                tree_crop_revenue_indiv_year = tree_crop_revenue[str(year)]  # tree crop revenue for the individual year
                tree_crop_acreage = df[df.crop == fruit].acres 
                tree_crop_acreage_indiv_year = tree_crop_acreage[str(year)]  # tree crop acreage for the individual year 
            except: 
                tree_crop_revenue_indiv_year = 0
                tree_crop_acreage_indiv_year = 0 
                print(f'no data for year {year} for crop {fruit}')

            print(f'total {fruit} acreage in year {year}: {tree_crop_acreage_indiv_year}')
            total_tree_crop_acreage = total_tree_crop_acreage + tree_crop_acreage_indiv_year
            weighted_individual_crop = tree_crop_revenue_indiv_year * tree_crop_acreage_indiv_year
            total_weighted_tree = total_weighted_tree + weighted_individual_crop

        print(f'total tree crop acreage in year {year}: {total_tree_crop_acreage}')
        tree_crop_revenue_per_acre[num] = total_weighted_tree / total_tree_crop_acreage  # gived the total weighted revenue of tree crops 
        print(f'Weighted total tree crop revenue for year {year}: {tree_crop_revenue_per_acre[num]}')

        for fruit in tqdm(annual_crop_list):
            # pdb.set_trace()
            annual_crop_revenue = df[df.crop == fruit].ppu *  ( df[df.crop == fruit]['yield'] )  # price/ acre 
            try:
                annual_crop_revenue_indiv_year = annual_crop_revenue[str(year)]  # tree crop revenue for the individual year
                annual_crop_acreage = df[df.crop == fruit].acres 
                annual_crop_acreage_indiv_year = annual_crop_acreage[str(year)]  # tree crop acreage for the individual year 
            except: 
                annual_crop_revenue_indiv_year = 0
                annual_crop_acreage_indiv_year = 0 
                print(f'no data for year {year} for crop {fruit}')

            print(f'total {fruit} acreage in year {year}: {annual_crop_acreage_indiv_year}')
            total_annual_crop_acreage = total_annual_crop_acreage + annual_crop_acreage_indiv_year
            
            # now, we have the total tree crop acreage as well as the acreage for each individual crop and the price of each individual crop 
            # calculate weighted average of revenue/acre: 
                # = ( sum for all crops: ( crop revenue x crop acreage )  ) / total_tree_crop_acreage (tree crops)
            weighted_individual_crop_annual = annual_crop_revenue_indiv_year * annual_crop_acreage_indiv_year
            total_weighted_annual = total_weighted_annual + weighted_individual_crop_annual

        print(f'total annual crop acreage in year {year}: {total_annual_crop_acreage}')
        annual_crop_revenue_per_acre[num] = total_weighted_annual / total_annual_crop_acreage  # gived the total weighted revenue of tree crops 
        print(f'Weighted total annual crop revenue for year {year}: {annual_crop_revenue_per_acre[num]}')

        year_list_array[num] = year
    price_difference = tree_crop_revenue_per_acre - annual_crop_revenue_per_acre
    pdb.set_trace()

    fig, ax = plt.subplots()
    ax.plot(year_list_array, tree_crop_revenue_per_acre, label = 'tree crop revenue per acre')
    ax.plot(year_list_array, annual_crop_revenue_per_acre, label = 'annual crop revenue per acre')
    ax.plot(year_list_array, price_difference, label = 'price difference')


    logic_rule = ( (year_list_array > 2010) & (year_list_array < 2016)) # or (year_list_array > 1991 & year_list_array < 1995))  
    collection = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=2500000, where=(logic_rule), facecolor='orange', alpha=0.3)
    ax.add_collection(collection)
    logic_rule2 =  ( (year_list_array < 1990) & (year_list_array > 1985)  )   
    collection2 = collections.BrokenBarHCollection.span_where(year_list_array, ymin=0, ymax=2500000, where=(logic_rule2), facecolor='orange', alpha=0.3)
    ax.add_collection(collection2)


    # collection = collections.BrokenBarHCollection.span_where(year_array, ymin=0, ymax=10000, where=year_array > 1994, facecolor='green', alpha=0.5)
    # ax.add_collection(collection)
    plt.legend()
    plt.show()

    return tree_crop_revenue, total_tree_crop_acreage, tree_crop_revenue_per_acre, price_difference

def plot_overall(tree_acreage_summed_for_year,annual_acreage_summed_for_year, price_difference ): 
    year_list_array = np.arange(1990, 2017)
    #plotted using the numpy arrays: 
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
    # plt.subplots(nrows = 2, sharex = True )
    ax0.plot(year_list_array[1:26], tree_acreage_summed_for_year[1:26], label = 'tree crop acreage')
    ax0.plot(year_list_array[1:26], annual_acreage_summed_for_year[1:26], label = 'annual crop acreage')
    plt.legend()
    ax0.set_title('total acres planted')
    # plt.ylabel('Total acres planted')

    # plt.subplots(2,2)
    ax1.plot(year_list_array[1:26], price_difference[7:32], label = 'difference in revenue per acre')
    plt.legend()
    ax1.plot('Tulare County Crop Type Changes 1991 - 2016 ')
    # plt.ylabel('Price difference')
    plt.show()
    pdb.set_trace()

def plot_revenue_v_percent_tree(percent_tree_acreage_summed_for_year, price_difference):
    x = price_difference[7:32]
    y = percent_tree_acreage_summed_for_year[1:26]
    plt.scatter(x,y)
    plt.xlabel('price difference between tree and annual crops')
    plt.ylabel('percent tree acreage in Tulare County')
    plt.show()


def orchard_crop_year_comparison(base_year, comparison_year, years_width):
    # pdb.set_trace()
    orchard_acreage_by_year_base = {}
    orchard_acreage_by_year_comp = {}

    for year in range(years_width):

        year_analysing = base_year + year
        # pdb.set_trace()
        base_year_percentages = pd.read_csv(os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', (str(year_analysing) + 'files' ), (str(year_analysing) + '_complete_acreage_breakdown.csv')  )) 
        base_year_percentages = base_year_percentages.rename(columns={"level_0": "COMTRS"})
        tree_crop_string =  "tree_crop_acreage_year" + str(year_analysing)
        base_year_percentages = base_year_percentages.rename(columns={"tree_crop_acreage": str(tree_crop_string)})  
        # base_year_percentages = base_year_percentages.set_index('COMTRS')
        base_year_data = base_year_percentages.ix[:, ['COMTRS',str(tree_crop_string)]]  # saves only the county ID and comtrs column 
        orchard_acreage_by_year_base[year_analysing] = base_year_data

        if year_analysing == base_year:
            base_years_orchard = orchard_acreage_by_year_base[base_year] # base year 
        else: 
            base_years_orchard = pd.merge(base_years_orchard, orchard_acreage_by_year_base[year_analysing]) # merges following years together 
            # pdb.set_trace()
        # pdb.set_trace()


        comparison_year_analysing = comparison_year + year
        comp_year_percentages = pd.read_csv(os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', (str(comparison_year_analysing) + 'files' ), (str(comparison_year_analysing) + '_complete_acreage_breakdown.csv')  )) 
        comp_year_percentages = comp_year_percentages.rename(columns={"level_0": "COMTRS"})
        tree_crop_string =  "tree_crop_acreage_year" + str(comparison_year_analysing)
        comp_year_percentages = comp_year_percentages.rename(columns={"tree_crop_acreage": str(tree_crop_string)})  
   
        comp_year_data = comp_year_percentages.ix[:, ['COMTRS',str(tree_crop_string)]]  # saves only the county ID and comtrs column 
        orchard_acreage_by_year_comp[comparison_year_analysing] = comp_year_data

        if comparison_year_analysing == comparison_year:
            comp_years_orchard = orchard_acreage_by_year_comp[comparison_year] # base year 
        else: 
            comp_years_orchard = pd.merge(comp_years_orchard, orchard_acreage_by_year_comp[comparison_year_analysing]) # merges following years together 
            # pdb.set_trace()
        # pdb.set_trace()



    # create a column where the 5 years are averaged 
    base_years_orchard = base_years_orchard.set_index('COMTRS')
    # base_years_orchard['average_orchard_acreage'] = np.mean(base_years_orchard.iloc[1,:])
    base_years_orchard_with_ave = base_years_orchard.copy()
    base_years_orchard_with_ave['average_orchard_acreage_base'] = base_years_orchard_with_ave.mean(numeric_only=True, axis=1)

    comp_years_orchard = comp_years_orchard.set_index('COMTRS')
    comp_years_orchard_with_ave = comp_years_orchard.copy()
    comp_years_orchard_with_ave['average_orchard_acreage_comp'] = comp_years_orchard_with_ave.mean(numeric_only=True, axis=1)
    pdb.set_trace()

    base_mean = base_years_orchard_with_ave.ix[:, ['average_orchard_acreage_base']] 
    base_mean = base_mean.reset_index()
    comp_mean = comp_years_orchard_with_ave.ix[:, ['average_orchard_acreage_comp']] 
    comp_mean = comp_mean.reset_index()
    # well_ids_with_comtrs = iter_data.ix[:, ['county_ID','co_mtrs']] 
    orchard_crop_acreage_difference = pd.merge(base_mean, comp_mean)
    orchard_crop_acreage_difference['orchard_acreage_difference'] = orchard_crop_acreage_difference.average_orchard_acreage_comp - orchard_crop_acreage_difference.average_orchard_acreage_base
    # ^ comparison - base  : shows growth in tree acreage. Large comparison year means positive expansion in tree acreage
    return base_year_percentages , base_years_orchard_with_ave, comp_years_orchard_with_ave, orchard_crop_acreage_difference


#extract calPIP data from file:
crop_time_series, overall_data, highest_acres_calPIP = extract_calPIP_data()

pdb.set_trace()
#extract commissioner data 
df, highest_valued, highest_acres = extract_commissioner_data()
print(highest_valued.crop)

make_timeseries_plots = 0 
if make_timeseries_plots == 1: 
    make_timeseries_plots()

overall_with_tree_crop_column, tree_list  = define_tree_crops(overall_data)

calPIP_crop_types = pd.read_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results_transposed.csv', sep = ',', index_col = 0)
## ^^ not actually used 

crop_compiling_option = 2
# Option 1: calculate all the data: 
if crop_compiling_option == 1:
    (all, total_tree_acreage_dict, tree_acreage_summed_for_year, annual_acreage_summed_for_year, 
        forage_acreage_summed_for_year, percent_tree_acreage_summed_for_year) = group_by_crop_type_all_year()

# Option 2: Load all the data to avoid re-calculating everything
if crop_compiling_option == 2: 
    (all, tree_acreage_summed_for_year, annual_acreage_summed_for_year, forage_acreage_summed_for_year, 
        percent_tree_acreage_summed_for_year) = load_crop_type_all_year()

plotting_overall_acreages = 0
if plotting_overall_acreages ==1:

    # Plot the comparisons of tree types 
    plot_crop_comparison(tree_acreage_summed_for_year,annual_acreage_summed_for_year, forage_acreage_summed_for_year )

    pdb.set_trace()
    # plots just for Tulary County 
    tree_crop_revenue, total_tree_crop_acreage, tree_crop_revenue_per_acre, price_difference = crop_value_calcs(df)

    plot_overall(tree_acreage_summed_for_year,annual_acreage_summed_for_year, price_difference )

    plot_revenue_v_percent_tree(percent_tree_acreage_summed_for_year, price_difference)

    pdb.set_trace() 



base_year = 1991 
comparison_year = 2010
years_width = 5 

base_year_percentages, base_years_orchard_with_ave, comp_years_orchard_with_ave, orchard_crop_acreage_difference = orchard_crop_year_comparison(base_year, comparison_year, years_width)
pdb.set_trace()


