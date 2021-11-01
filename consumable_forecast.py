import pandas as pd
from matplotlib import pyplot as plt
import os
from tqdm import tqdm

result_path = '/Users/pei/pydir/RHS_anly/result/'
fault_rate_df = pd.read_csv(result_path + 'fault_rate_df.csv')

period = 3
sum_fault_rate_list = []
for index in range(len(fault_rate_df)):
    # print(rhs_log.loc[index].tolist())
    single_sum_fault_rate = sum(fault_rate_df.loc[index].tolist()[-period:])
    sum_fault_rate_list.append(single_sum_fault_rate)

fault_rate_df['fault_rate_sum'] = sum_fault_rate_list
# fault_rate_df = fault_rate_df.sort_values(by='fault_rate_sum')

consumable_forecast_df = pd.DataFrame([])
new_site_list = []
site_forecast = []
Optic_type_list = []
forecast_period_list = [period]*len(fault_rate_df)
for index in range(len(fault_rate_df)):
    site = fault_rate_df['Site_list'].tolist()[index]
    new_site_list.append(site)
    single_site_forecast = round(fault_rate_df['fault_rate_sum'].tolist()[index])
    site_forecast.append(single_site_forecast)
    Optic_type_list.append('Colorchip C100Q020CWDM403B')

consumable_forecast_df['Site'] = new_site_list
consumable_forecast_df['Consumable_Forecast'] = site_forecast
consumable_forecast_df['Consumable_PN'] = site_forecast
consumable_forecast_df['Forecast_Period'] = forecast_period_list

consumable_forecast_df.to_excel(result_path + 'consumable_forecast_df.xlsx',index=False)