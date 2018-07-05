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
    column_list = []
    # pdb.set_trace()
    return crop_list, column_list, calPIP_data


# crop_list, column_list, calPIP_data = read_data(1990)

# calPIP_data.to_csv('calPIP1990_attempt2.csv', sep = ',')

pdb.set_trace()


def read_overall_data():
	filename = overall_results.csv 
	file_name = os.path.join('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages', filename)
	calPIP_data_overall = pd.read_csv(file_name, sep = '\t')

	calPIP_data_overall.to_csv('/Users/nataliemall/Box Sync/herman_research_box/calPIP_crop_acreages/overall_results_separated.csv', sep = ',')
	return calPIP_data_overall

calPIP_data_overall = read_overall_data(): 


