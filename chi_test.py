import pandas as pd
from scipy import stats
import os
import numpy as np

import month_abbr as ma
import de_zero as dz
import rhs_times as rt
import power_integrated as pi

def chi_test():
    raw_path = '/Users/pei/pydir/RHS_anly/raw_data/'
    result_path = '/Users/pei/pydir/RHS_anly/result/'
    rhs_log = pd.read_csv(raw_path + 'RHS Usage Log-Summary-update 20210827.csv')
    max_cab_pwr = pd.read_csv(raw_path + 'max_cab_power.csv')
    total_device_list = pd.read_csv(raw_path + 'network device list.csv')
    site_list = max_cab_pwr['Site ID'].tolist()

    pwr_file_list = os.listdir(raw_path + 'yearly_power_data/')
    for single_file in pwr_file_list:
        if single_file.split('.')[1] != 'csv':
            os.remove(raw_path + 'yearly_power_data/' + single_file)
    pwr_file_list = os.listdir(raw_path + 'yearly_power_data/')

    # max_device_num = 100#假设每个站点最大的网络设备数为100，以便归一化处理
    power_rhs = [1,1,1,1,1,1,1,1]#变化率从20%-90%，共8档
    power_no_rhs = [1,1,1,1,1,1,1,1]#变化率从20%-90%，共8档
    amount_rhs = [1,1,1,1,1,1,1]#设备数量变化率从15%-35%，共5档
    amount_no_rhs = [1,1,1,1,1,1,1]#设备数量变化率从15%-45%，共5档


    #得到处理的前置条件，如日期等
    bjs_power_avg = pd.read_csv(raw_path + 'yearly_power_data/CU Beijing.csv')
    bjs_power_avg = pi.power_integrated(bjs_power_avg)
    bjs_power_avg = dz.de_zero(bjs_power_avg)
    date_list_sample, rhs_times_index_list, rhs_times_list = rt.rhs_times(rhs_log, 'CU Beijing', bjs_power_avg)

    for date_index in range(len(date_list_sample)):
        max_fault_rate = 0
        max_site = 'N'
        year_month = date_list_sample[date_index].split('-')[0] + '-' + str(int(date_list_sample[date_index].split('-')[1]))
        for single_site in site_list:
        #处理power data
            single_file = single_site + '.csv'
            if single_file in pwr_file_list:
                single_site_pwr = pd.read_csv(raw_path + 'yearly_power_data/' + single_site + '.csv')
                single_site_pwr = pi.power_integrated(single_site_pwr)
                single_site_pwr = dz.de_zero(single_site_pwr)
                date_list_sample, rhs_times_index_list, rhs_times_list = rt.rhs_times(rhs_log, single_site, single_site_pwr)
                pwr_avg = single_site_pwr[single_site_pwr['Key'] == date_list_sample[date_index]]['Avg_Value'].tolist()[0]
                single_cab_pwr = max_cab_pwr[max_cab_pwr['Site ID']==single_site]['max_power'].tolist()[0]
                if pwr_avg == 0:
                    single_utility_rate = round(1600/single_cab_pwr,3)
                else:
                    single_utility_rate = round(pwr_avg / single_cab_pwr, 3)
            else:#没有power data的情况
                single_utility_rate = round(1600 / single_cab_pwr, 3)
            # print(single_utility_rate)
            rhs_select_df = rhs_log[(rhs_log['Request Year-Month']==year_month) & (rhs_log['Site ID'] == single_site)]
            pwr_list_index = int((single_utility_rate * 100 - 20) / 10)
            if len(rhs_select_df) == 0:
                power_no_rhs[pwr_list_index] += 1
            else:
                power_rhs[pwr_list_index] += len(rhs_select_df)

        #处理设备数量
            single_site_amount = len(total_device_list[total_device_list['Site ID']==single_site])
            # print('single_site_amount=' + str(single_site_amount))
            amt_list_index = int((single_site_amount - 15) / 5)
            if len(rhs_select_df) == 0:
                amount_no_rhs[amt_list_index] += 1
            else:
                amount_rhs[amt_list_index] += len(rhs_select_df)

    #power卡方检验
    pwr_expect_rhs_list = []
    pwr_expect_no_rhs_list = []
    pwr_expected_rate = sum(power_rhs) / (sum(power_rhs) + sum(power_no_rhs))#假设故障率和耗电无关
    for index in range(len(power_rhs)):
        single_expect_rhs = (power_rhs[index] + power_no_rhs[index]) * pwr_expected_rate
        single_expect_no_rhs = (power_rhs[index] + power_no_rhs[index]) * (1 - pwr_expected_rate)
        pwr_expect_rhs_list.append(single_expect_rhs)
        pwr_expect_no_rhs_list.append(single_expect_no_rhs)

    chi_squared_stat_pwr = ((np.array(power_rhs)-np.array(pwr_expect_rhs_list))**2/np.array(pwr_expect_rhs_list)).sum() + \
                       ((np.array(power_no_rhs)-np.array(pwr_expect_no_rhs_list))**2/np.array(pwr_expect_no_rhs_list)).sum()

    print('chi_squared_stat_pwr = ' + str(chi_squared_stat_pwr) )

    crit = stats.chi2.ppf(q=0.95,df=7)  #90置信水平 df = 自由度
    print(crit) #临界值，拒绝域的边界 当卡方值大于临界值，则原假设不成立，备择假设成立
    # P_value_pwr = 1-stats.chi2.cdf(x=chi_squared_stat_pwr,df=7)
    # print('P_value_power')
    # print(P_value_pwr)

    #amount卡方检验
    amt_expect_rhs_list = []
    amt_expect_no_rhs_list = []
    amt_expected_rate = sum(amount_rhs) / (sum(amount_rhs) + sum(amount_no_rhs))#假设故障率和耗电无关
    for index in range(len(amount_rhs)):
        single_expect_rhs = (amount_rhs[index] + amount_no_rhs[index]) * amt_expected_rate
        single_expect_no_rhs = (amount_rhs[index] + amount_no_rhs[index]) * (1 - amt_expected_rate)
        amt_expect_rhs_list.append(single_expect_rhs)
        amt_expect_no_rhs_list.append(single_expect_no_rhs)

    chi_squared_stat_amt = ((np.array(amount_rhs)-np.array(amt_expect_rhs_list))**2/np.array(amt_expect_rhs_list)).sum() + \
                       ((np.array(amount_no_rhs)-np.array(amt_expect_no_rhs_list))**2/np.array(amt_expect_no_rhs_list)).sum()

    print('chi_squared_stat_amt = ' + str(chi_squared_stat_amt))

    pwr_amt_ratio_pwr = chi_squared_stat_pwr / (chi_squared_stat_pwr + chi_squared_stat_amt)
    print('pwr_amt_ratio_pwr = ' + str(pwr_amt_ratio_pwr))
    pwr_amt_ratio_amt = chi_squared_stat_amt / (chi_squared_stat_pwr + chi_squared_stat_amt)
    print('pwr_amt_ratio_amt = ' + str(pwr_amt_ratio_amt))
    return pwr_amt_ratio_pwr,pwr_amt_ratio_amt