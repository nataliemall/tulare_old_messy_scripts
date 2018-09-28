
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


# files = 'pur_pre_1990/pur1990'

def replace_bad_characters():
	directory = 'tulare_git_repo/pur_data_raw/'
	os.mkdir('pur_data_cleaned')  #make cleaned directory 
	new_directory = 'pur_data_cleaned'
	# 'pur1990/'

	# 'udc90_54.txt'

	file_years = np.arange(1990,2017)
	file_numbers = [10, 15, 16, 54]  # fixes only the necessary counties (Tulare, Kern, Kings, Fresno)

	for year in file_years:
	    for file in file_numbers:

	        # pdb.set_trace()
	        final_two_digits = str(year)
	        final_two_digits = final_two_digits[-2:]

	        # file_to_change = pd.read_csv(os.path.join(directory, ( 'pur' + str(year)), 'udc' + str(final_two_digits) + '_' + str(file) + '.txt')) #, header = True, na_rep = '0', index = False) 
	        file_to_change = (os.path.join(directory, ( 'pur' + str(year)), 'udc' + str(final_two_digits) + '_' + str(file) )) #, header = True, na_rep = '0', index = False) 
	        new_file_with_location = (os.path.join(new_directory, ( 'pur' + str(year)), 'udc' + str(final_two_digits) + '_' + str(file) ))

	        new = open(file_to_change + '.txt').read().replace('?','0')
	        open(new_file_with_location + '_fixed.txt', 'w').write(new)

