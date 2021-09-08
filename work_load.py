import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

import tkt_tkn_stat as tts
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
stat_num_charged,stat_num_un_charged = tts.token_stat(rhs_log,site_list,city_list)
print(stat_num_charged)
print(stat_num_un_charged)