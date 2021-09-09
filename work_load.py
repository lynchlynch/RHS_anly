import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import os

import tkt_tkn_stat as tts
import rhs_times as rt
import power_integrated as pi
import de_zero as dz
import chi_test as ct

raw_path = '/Users/pei/pydir/RHS_anly/raw_data/'
result_path = '/Users/pei/pydir/RHS_anly/result/'
# rhs_log = pd.read_excel(raw_path + 'RHS Usage Log-Summary-update 20210827的副本.xlsx',engine='openpyxl',sheet_name='Log')
rhs_log = pd.read_excel(raw_path + 'RHS Usage Log-Summary-update 20210827.xlsx',engine='openpyxl',sheet_name='Log')
# print(rhs_log['Request Year-Month'].tolist())
# print(rhs_log['Request Year-Month'].tolist())
max_cab_pwr = pd.read_csv(raw_path + 'max_cab_power.csv')
site_list = max_cab_pwr['Site ID'].tolist()
total_device_list = pd.read_csv(raw_path + 'network device list.csv')

city_list = ['Beijing','Shanghai','Guangzhou','Chengdu','Wuhan']

##工单量堆叠
ct_list,cm_list,cu_list,third_part_list,sum_per_city_list = tts.tkt_stat(rhs_log,site_list,city_list)

bar_width = 0.4
index_city_list = np.array(list(range(len(ct_list))))
bottom_cu = list(np.array(ct_list) + np.array(cm_list))
bottom_3p = list(np.array(bottom_cu) + np.array(cu_list))

plt.style.use('dark_background')
plt.bar(index_city_list+bar_width/2,height=ct_list,width=bar_width,color='red',label='CT')
plt.bar(index_city_list+bar_width/2,height=cm_list,bottom=ct_list,width=bar_width,color='lime',label='CM')
plt.bar(index_city_list+bar_width/2,height=cu_list,bottom=bottom_cu,width=bar_width,color='orange',label='CU')
plt.bar(index_city_list+bar_width/2,height=third_part_list,bottom=bottom_3p,width=bar_width,color='cyan',label='3-P')

for index in range(len(index_city_list)):
    plt.text(index_city_list[index]+bar_width/3,ct_list[index]/2,str('%.0f'%ct_list[index]))
    if index != city_list.index('Shanghai'):
        plt.text(index_city_list[index]+bar_width/3,ct_list[index]+cm_list[index]/2,str('%.0f'%cm_list[index]))
    plt.text(index_city_list[index]+bar_width/3,ct_list[index]+cm_list[index]+cu_list[index]/2, str('%.0f' % cu_list[index]))
    if index != city_list.index('Wuhan'):
        plt.text(index_city_list[index]+bar_width/3,ct_list[index]+cm_list[index]+cu_list[index]+third_part_list[index]/2,
                 str('%.0f' % third_part_list[index]))

    plt.text(index_city_list[index]+bar_width/3,sum_per_city_list[index]+1,str('%.0f'%sum_per_city_list[index]))

plt.legend()
city_simple_list = ['BJS','SHA','CAN','CTU','WUH']
plt.xticks(np.array(index_city_list)+bar_width/2,city_simple_list,rotation=45)
plt.title('Ticket QTY')
plt.savefig(result_path + 'work_load_ticket.png')

####Token量堆叠
stat_num_daily, stat_num_breakfix, stat_num_deployment = tts.token_stat(rhs_log,site_list,city_list)
total_token = list(np.array(stat_num_daily) + np.array(stat_num_breakfix) + np.array(stat_num_deployment))

bar_width = 0.4
index_city_list = np.array(list(range(len(stat_num_daily))))
bottom_deployment = list(np.array(stat_num_daily) + np.array(stat_num_breakfix))

plt.close()
plt.style.use('dark_background')
plt.bar(index_city_list+bar_width/2,height=stat_num_daily,width=bar_width,color='red',label='Daily Run')
plt.bar(index_city_list+bar_width/2,height=stat_num_breakfix,bottom=stat_num_daily,width=bar_width,color='lime',label='Breakfix')
plt.bar(index_city_list+bar_width/2,height=stat_num_deployment,bottom=bottom_deployment,width=bar_width,color='orange',label='Deployment')

for index in range(len(index_city_list)):
    plt.text(index_city_list[index]+bar_width/3,stat_num_daily[index]/2,str('%.0f'%stat_num_daily[index]))
    plt.text(index_city_list[index] + bar_width / 3, stat_num_daily[index] + stat_num_breakfix[index] / 2, str('%.0f' % stat_num_breakfix[index]))
    plt.text(index_city_list[index] + bar_width / 3, bottom_deployment[index] + stat_num_deployment[index] / 2, str('%.0f' % stat_num_deployment[index]))
    plt.text(index_city_list[index]+bar_width/3,total_token[index]+1,str('%.0f'%total_token[index]))

plt.legend()
city_simple_list = ['BJS','SHA','CAN','CTU','WUH']
plt.xticks(np.array(index_city_list)+bar_width/2,city_simple_list,rotation=45)
plt.title('Token QTY')
plt.savefig(result_path + 'work_load_token.png')

##统计成本
stat_cost_breakfix, stat_cost_deployment, stat_cost_baseline = tts.cost_stat(rhs_log,site_list,city_list)
total_cost = list(np.array(stat_cost_breakfix) + np.array(stat_cost_deployment) + np.array(stat_cost_baseline))

bar_width = 0.4
index_city_list = np.array(list(range(len(stat_cost_breakfix))))
bottom_deployment = list(np.array(stat_cost_baseline) + np.array(stat_cost_breakfix))

plt.close()
plt.style.use('dark_background')
plt.bar(index_city_list+bar_width/2,height=stat_cost_baseline,width=bar_width,color='red',label='Baseline Cost')
plt.bar(index_city_list+bar_width/2,height=stat_cost_breakfix,bottom=stat_cost_baseline,width=bar_width,color='lime',label='Breakfix Cost')
plt.bar(index_city_list+bar_width/2,height=stat_cost_deployment,bottom=bottom_deployment,width=bar_width,color='orange',label='Deployment Cost')

for index in range(len(index_city_list)):
    plt.text(index_city_list[index]-bar_width/10,stat_cost_baseline[index]/2,str('%.0f'%stat_cost_baseline[index]))
    plt.text(index_city_list[index]-bar_width/10, stat_cost_baseline[index] + stat_cost_breakfix[index] / 2, str('%.0f' % stat_cost_breakfix[index]))
    plt.text(index_city_list[index]-bar_width/10, bottom_deployment[index] + stat_cost_deployment[index] / 2, str('%.0f' % stat_cost_deployment[index]))
    plt.text(index_city_list[index]-bar_width/10,total_cost[index]+50,str('%.0f'%total_cost[index]))

plt.legend()
city_simple_list = ['BJS','SHA','CAN','CTU','WUH']
plt.xticks(np.array(index_city_list)+bar_width/2,city_simple_list,rotation=45)
plt.title('Cost(Yuan)')
plt.savefig(result_path + 'work_load_cost.png')

##画故障曲线
#利用卡方检验来动态计算设备功耗，设备数量的权重
fault_rate_df = ct.chi_test_workload(raw_path,rhs_log,site_list,max_cab_pwr,total_device_list)
month_list = fault_rate_df['Month'].tolist()

bjs_fault_list = []
sha_fault_list = []
can_fault_list = []
ctu_fault_list = []
wuh_fault_list = []
for single_month in month_list:
    single_bjs_fault = sum(fault_rate_df[(fault_rate_df['Month']==single_month) and
                                     (fault_rate_df['Site ID'].str.contains('Beijing'))]['Fault_Rate'])
    bjs_fault_list.append(single_bjs_fault)

    single_sha_fault = sum(fault_rate_df[(fault_rate_df['Month'] == single_month) and
                                         (fault_rate_df['Site ID'].str.contains('Shanghai'))]['Fault_Rate'])
    sha_fault_list.append(single_sha_fault)

    single_can_fault = sum(fault_rate_df[(fault_rate_df['Month'] == single_month) and
                                         (fault_rate_df['Site ID'].str.contains('Guangzhou'))]['Fault_Rate'])
    can_fault_list.append(single_can_fault)

    single_ctu_fault = sum(fault_rate_df[(fault_rate_df['Month'] == single_month) and
                                         (fault_rate_df['Site ID'].str.contains('Chengdu'))]['Fault_Rate'])
    ctu_fault_list.append(single_ctu_fault)

    single_wuh_fault = sum(fault_rate_df[(fault_rate_df['Month'] == single_month) and
                                         (fault_rate_df['Site ID'].str.contains('Wuhan'))]['Fault_Rate'])
    wuh_fault_list.append(single_wuh_fault)

plt.close()
plt.style.use('dark_background')
plt.plot(bjs_fault_list,color='red',label='BJS Fault')
plt.plot(sha_fault_list,color='lime',label='SHA Fault')
plt.plot(can_fault_list,color='orange',label='CAN Fault')
plt.plot(ctu_fault_list,color='deepskyblue',label='CTU Fault')
plt.plot(wuh_fault_list,color='sienna',label='WUH Fault')

plt.legend()
plt.xticks(list(range(len(wuh_fault_list))),month_list,rotation=45)
plt.title('Fault Trend')
plt.savefig(result_path + 'work_load_fault_trend.png')