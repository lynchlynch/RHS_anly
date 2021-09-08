import pandas as pd
from matplotlib import pyplot as plt
import os
from tqdm import tqdm

import de_zero as dz
import rhs_times as rt
import power_integrated as pi
import rhs_consumable as rc
import chi_test as ct

raw_path = '/Users/pei/pydir/RHS_anly/raw_data/'
result_path = '/Users/pei/pydir/RHS_anly/result/'
# rhs_log = pd.read_csv(raw_path + 'RHS Usage Log-Summary-update 20210827.csv')
rhs_log = pd.read_excel(raw_path + 'RHS Usage Log-Summary-update 20210827.xlsx',engine='openpyxl',sheet_name='Log')
# print(rhs_log)
# print(rhs_log['Request Year-Month'].tolist())
max_cab_pwr = pd.read_csv(raw_path + 'max_cab_power.csv')
site_list = max_cab_pwr['Site ID'].tolist()
total_device_list = pd.read_csv(raw_path + 'network device list.csv')

