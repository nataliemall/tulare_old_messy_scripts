# debugging: comparing the old and new comtrs data compilation 


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




fast_compilation = pd.read_csv('comtrs_pur_vals_year1978.csv')
fast_compilation_comtrs = fast_compilation.comtrs
#find out how many nan comtrs permits there are 

num = 0 


fast_compilation_comtrs.isnull().sum()
# 2378 null values 


acres_fast = fast_compilation.acre_unit_treated


slow_compilation = pd.read_csv('comtrs_pur_vals_year78.csv')
slow_compilation_comtrs = slow_compilation.comtrs 

acres_slow = slow_compilation.acre_unit_treated

# slow_compilation_comtrs.to_csv('slow_compilation_comtrs.csv')
# fast_compilation_comtrs.to_csv('fast_compilation_comtrs.csv')



# read the datasets binned by crop type: 

fast_binned = pd.read_csv('all_data_year78_by_COMTRS_fast.csv', sep = '\t')
slow_binned = pd.read_csv('all_data_year78_by_COMTRS_slow.csv', sep = '\t')

cotton_fast = fast_binned['3201'].sum()
cotton_slow = slow_binned['3201'].sum()

peach_fast = fast_binned['2304'].sum()
peach_slow = slow_binned['2304'].sum()
pdb.set_trace()