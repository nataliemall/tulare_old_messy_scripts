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



slow_compilation = pd.read_csv('comtrs_pur_vals_year78.csv')
slow_compilation_comtrs = slow_compilation.comtrs 

# slow_compilation_comtrs.to_csv('slow_compilation_comtrs.csv')
# fast_compilation_comtrs.to_csv('fast_compilation_comtrs.csv')



pdb.set_trace()