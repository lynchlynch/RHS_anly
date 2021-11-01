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
rhs_log = pd.read_excel(raw_path + 'RHS Usage Log-Summary-update.xlsx',engine='openpyxl',sheet_name='Log')
# print(rhs_log)
# print(rhs_log['Request Year-Month'].tolist())
max_cab_pwr = pd.read_csv(raw_path + 'max_cab_power.csv')
site_list = max_cab_pwr['Site ID'].tolist()
total_device_list = pd.read_csv(raw_path + 'network device list.csv')

pwr_file_list = os.listdir(raw_path + 'yearly_power_data/')
for single_file in pwr_file_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(raw_path + 'yearly_power_data/' + single_file)
pwr_file_list = os.listdir(raw_path + 'yearly_power_data/')

#每个站点功率和RHS维修次数的关系
for single_site in tqdm(site_list,desc='pwr-rhs'):
    # print(single_site)
    if (single_site + '.csv') in pwr_file_list:
        single_site_pwr = pd.read_csv(raw_path + 'yearly_power_data/' + single_site + '.csv')
        single_site_pwr = pi.power_integrated(single_site_pwr)
        single_site_pwr = dz.de_zero(single_site_pwr)
        plt.figure()
        plt.style.use('dark_background')
        plt.plot(single_site_pwr['Value'].tolist(),label='power')
        plt.xlabel('Month')
        plt.ylabel('Power/W')
        plt.legend()
        date_list_sample, rhs_times_index_list, rhs_times_list = rt.rhs_times(rhs_log, single_site, single_site_pwr)
        plt.xticks(rhs_times_index_list, date_list_sample, color='blue', rotation=60)
        plt.twinx()
        plt.plot(rhs_times_index_list, rhs_times_list, 'ro-',label='RHS')
        plt.ylabel('RHS times')
        plt.title(single_site + '_power-RHS')
        plt.legend()
        # plt.legend(loc=2)
        plt.savefig(result_path + single_site + '_power-RHS.png', bbox_inches='tight')
        plt.close()

bjs_power_avg = pd.read_csv(raw_path + 'yearly_power_data/CU Beijing.csv')
bjs_power_avg = pi.power_integrated(bjs_power_avg)
bjs_power_avg = dz.de_zero(bjs_power_avg)
date_list_sample, rhs_times_index_list, rhs_times_list = rt.rhs_times(rhs_log, 'CU Beijing', bjs_power_avg)

#遍历所有站点power，计算归一化的故障率，然后排序，计算每个月故障最多的站点
#利用卡方检验来动态计算设备功耗，设备数量的权重
pwr_amt_ratio_pwr,pwr_amt_ratio_amt = ct.chi_test(rhs_log)
max_fault_rate_list = []
max_site_list = []
# print(date_list_sample)
fault_rate_df = pd.DataFrame([])
fault_rate_df['Site_list'] = site_list
# year_month_list = []
for date_index in tqdm(range(len(date_list_sample)),desc='fault'):
    max_fault_rate = 0
    max_site = 'N'
    year_month = date_list_sample[date_index].split('-')[0] + '-' + str(int(date_list_sample[date_index].split('-')[1]))
    fault_per_month_list = []
    for single_site in site_list:
        # print(single_site)
        single_file = single_site + '.csv'
        if single_file in pwr_file_list:
            single_site_pwr = pd.read_csv(raw_path + 'yearly_power_data/' + single_site + '.csv')
            single_site_pwr = pi.power_integrated(single_site_pwr)
            single_site_pwr = dz.de_zero(single_site_pwr)
            date_list_sample, rhs_times_index_list, rhs_times_list = rt.rhs_times(rhs_log, single_site, single_site_pwr)
            # print(rhs_times_list)
            pwr_avg = single_site_pwr[single_site_pwr['Key'] == date_list_sample[date_index]]['Avg_Value'].tolist()[0]
            single_cab_pwr = max_cab_pwr[max_cab_pwr['Site ID']==single_site]['max_power'].tolist()[0]
            if pwr_avg == 0:
                single_max_fault_rate_pwr = round(rhs_times_list[date_index]/(1600/single_cab_pwr),3)
            else:
                single_max_fault_rate_pwr = round(rhs_times_list[date_index] / (pwr_avg / single_cab_pwr), 3)
        else:#没有power data的情况
            rhs_times = len(rhs_log[(rhs_log['Site ID'] == single_site) & (rhs_log['Request Year-Month'] == year_month) &
                    (rhs_log['project'] == 'N')])
            # print(rhs_log[rhs_log['Request Year-Month'] == year_month])
            # print('rhs_times=' + str(rhs_times))
            single_cab_pwr = max_cab_pwr[max_cab_pwr['Site ID'] == single_site]['max_power'].tolist()[0]
            single_max_fault_rate_pwr = round(rhs_times / (1600 / single_cab_pwr), 0)
        # print('single_max_fault_rate_pwr=' + str(single_max_fault_rate_pwr))
        #处理设备数量
        # rhs_select_df = rhs_log[(rhs_log['Request Year-Month'] == year_month) & (rhs_log['Site ID'] == single_site)]
        single_site_amount = len(total_device_list[total_device_list['Site ID'] == single_site])
        # print('single_site_amount=' + str(single_site_amount))
        single_max_fault_rate_amt = single_site_amount/100#按100归一化
        # print('single_max_fault_rate_amt=' + str(single_max_fault_rate_amt))
        # amt_list_index = int((single_site_amount - 15) / 5)
        single_max_fault_rate = pwr_amt_ratio_amt * single_max_fault_rate_pwr + pwr_amt_ratio_pwr * single_max_fault_rate_amt
        fault_per_month_list.append(single_max_fault_rate)
        if single_max_fault_rate > max_fault_rate:
            max_fault_rate = single_max_fault_rate
            max_site = single_site
    # fault_rate_add_df = pd.DataFrame(fault_per_month_list)
    # fault_rate_df = fault_rate_df.append(fault_rate_add_df)
    # print(fault_per_month_list)
    fault_rate_df.insert(loc=len(fault_rate_df.columns),column=year_month,value=fault_per_month_list)

    max_fault_rate_list.append(max_fault_rate)
    max_site_list.append(max_site)
#储存详细的fault_rate
# print(fault_rate_df)
fault_rate_df.to_csv(result_path + 'fault_rate_df.csv',index=False)

plt.figure()
plt.style.use('dark_background')
plt.plot(rhs_times_index_list,max_fault_rate_list,'r^-')
plt.xticks(rhs_times_index_list,date_list_sample,color='white',rotation=60)

for annote_index in range(len(rhs_times_index_list)):
    plt.annotate(max_site_list[annote_index], xy=(rhs_times_index_list[annote_index], max_fault_rate_list[annote_index]),
                 xytext=(rhs_times_index_list[annote_index], max_fault_rate_list[annote_index] + (-1)**(annote_index%2) * 0.5),
                 xycoords='data',arrowprops=dict(facecolor='blue', shrink=0.05))
plt.title('highest_fault_rate')
# plt.show()
plt.savefig(result_path + 'highest_fault_rate.png',bbox_inches='tight')
plt.close()

###画MBR的故障率图
date_list_sample_mbr = ['2021-4','2021-5','2021-6','2021-7','2021-8','2021-9']
rhs_times_index_list_mbr = rhs_times_index_list[-6:]
max_fault_rate_list_mbr = max_fault_rate_list[-6:]
max_site_list_mbr = max_site_list[-6:]
plt.figure()
plt.style.use('dark_background')
plt.plot(rhs_times_index_list_mbr,max_fault_rate_list_mbr,'r^-')
plt.xticks(rhs_times_index_list_mbr,date_list_sample_mbr,color='white',rotation=45)
for annote_index in range(len(rhs_times_index_list_mbr)):
    plt.annotate(max_site_list_mbr[annote_index], xy=(rhs_times_index_list_mbr[annote_index], max_fault_rate_list_mbr[annote_index]),
                 xytext=(rhs_times_index_list_mbr[annote_index], max_fault_rate_list_mbr[annote_index] + (-1)**((annote_index+1)%2) * 0.1),
                 xycoords='data',arrowprops=dict(facecolor='blue', shrink=0.05))
plt.title('highest_fault_rate')
# plt.show()
plt.savefig(result_path + 'highest_fault_rate_mbr.png',bbox_inches='tight')
plt.close()

#计算单个工单需要的模块量
total_csmb_tkt_list = []
for date_index in tqdm(range(len(date_list_sample)),desc='consumable'):
    year_month = date_list_sample[date_index].split('-')[0] + '-' + str(int(date_list_sample[date_index].split('-')[1]))
    select_df = rhs_log[(rhs_log['Request Year-Month'] == year_month) & (rhs_log['project'] == 'N')]
    total_csmb = 0
    if len(select_df) == 0:
        total_csmb_tkt_list.append(0)
    else:
        for index in range(len(select_df)):
            if select_df['Module'].tolist()[index] != 'N':
                total_csmb += int((select_df['Module'].tolist()[index]).split('个')[0])
        total_csmb_tkt_list.append(round(total_csmb/len(select_df),3))

plt.figure()
plt.style.use('dark_background')
plt.plot(rhs_times_index_list, total_csmb_tkt_list,'r*:')
plt.title('consumale/ticket')
plt.xticks(rhs_times_index_list,date_list_sample,color='blue',rotation=60)
plt.savefig(result_path + 'ticket-consumale.png',bbox_inches='tight')
plt.close()

current_year = int((rhs_log['Request Year-Month'].tolist()[-1]).split('-')[0])
current_month = int((rhs_log['Request Year-Month'].tolist()[-1]).split('-')[1])
process_period = 6
current_year_month_list = []
for index in range(process_period):
    if (current_month - index) < 1:
        current_year_month = str(current_year-1) + '-' + str(12-current_month+1)
    else:
        current_year_month = str(current_year) + '-' + str(current_month-index)
        # print(current_year_month)
    current_year_month_list.append(current_year_month)

#ticket-token量
rhs_times_list = []
token_qty_list = []
for index in range(process_period):
    current_year_month = current_year_month_list[process_period-index-1]
    rhs_times = len(rhs_log[rhs_log['Request Year-Month']==current_year_month])
    rhs_times_list.append(rhs_times)
    token_num_per_month = sum(rhs_log[rhs_log['Request Year-Month']==current_year_month]['Number of Tokens'].tolist())
    # print('current_year_month = ' + str(token_num_per_month))
    token_qty_list.append(token_num_per_month)

# print(rhs_times_list)
# print(token_qty_list)

plt.close()
plt.figure()
plt.style.use('dark_background')
plt.plot(list(range(process_period)),rhs_times_list,'o-',color='orange',label='Ticket')
plt.plot(list(range(process_period)),token_qty_list,'v-',color='cyan',label='Token')
# print(current_year_month_list)
current_year_month_list_reverse = []
for index in range(process_period):
    current_year_month_list_reverse.append(current_year_month_list[process_period-index-1])
    plt.text(index,rhs_times_list[index]-0.6,rhs_times_list[index])
    plt.text(index,token_qty_list[index]+0.2, token_qty_list[index])
# print(current_year_month_list_reverse)
# print(list(range(process_period)))
x_index = list(range(process_period))
plt.xticks(x_index,current_year_month_list_reverse,rotation=45)
plt.legend()

plt.title('Ticket-Token')
plt.savefig(result_path + 'ticket_token')