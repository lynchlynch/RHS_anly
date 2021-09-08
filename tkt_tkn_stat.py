def tkt_stat(raw_data,site_list,city_list):
    ct_list = [0,0,0,0,0]
    cm_list = [0,0,0,0,0]
    cu_list = [0,0,0,0,0]
    third_part_list = [0,0,0,0,0]
    sum_per_city_list = [0,0,0,0,0]
    stat_num = []
    for single_site in site_list:
        select_df = raw_data[raw_data['Site ID']==single_site]
        stat_num.append(len(select_df))

    for single_city_index in range(len(city_list)):
        single_city = city_list[single_city_index]
        # if single_city != 'Wuhan':
        ct_index = site_list.index('CT '+single_city)
        ct_list[single_city_index] = stat_num[ct_index]

        cm_index = site_list.index('CM ' +single_city)
        cm_list[single_city_index] = stat_num[cm_index]

        cu_index = site_list.index('CU ' + single_city)
        cu_list[single_city_index] = stat_num[cu_index]

        if single_city != 'Wuhan':
            if single_city == 'Chengdu':
                third_part_index = site_list.index('GDS ' + single_city)
            else:
                third_part_index = site_list.index('DR Peng ' + single_city)

            third_part_list[single_city_index] = stat_num[third_part_index]

        sum_per_city_list[single_city_index] = ct_list[single_city_index] + cm_list[single_city_index] + \
                                               cu_list[single_city_index] + third_part_list[single_city_index]

    return ct_list,cm_list,cu_list,third_part_list,sum_per_city_list

def token_stat(raw_data,site_list,city_list):
    '''
    stat_num_charged = []
    stat_num_un_charged = []

    for single_city in city_list:
        select_charged_df = raw_data[(raw_data['Site ID'].str.contains(single_city))&(raw_data['Token Type']!='Daily-A')]
        stat_num_charged.append(sum(select_charged_df['Number of Tokens'].tolist()))
        select_un_charged_df = raw_data[(raw_data['Site ID'].str.contains(single_city))&(raw_data['Token Type']=='Daily-A')]
        stat_num_un_charged.append(sum(select_un_charged_df['Number of Tokens'].tolist()))

    return stat_num_charged,stat_num_un_charged
    '''
    stat_num_daily = []
    stat_num_breakfix = []
    stat_num_deployment = []

    for single_city in city_list:
        select_breakfix_df = raw_data[
            (raw_data['Site ID'].str.contains(single_city)) & (raw_data['Token Type'] != 'Daily-A') &
            (raw_data['project'] == 'N')]
        stat_num_breakfix.append(sum(select_breakfix_df['Number of Tokens'].tolist()))

        select_deployment_df = raw_data[(raw_data['Site ID'].str.contains(single_city)) &
                                        (raw_data['Token Type'] != 'Daily-A') & (raw_data['project'] == 'Y')]
        stat_num_deployment.append(sum(select_deployment_df['Number of Tokens'].tolist()))

        select_daily_df = raw_data[(raw_data['Site ID'].str.contains(single_city)) &
                                   (raw_data['Token Type'] == 'Daily-A')]
        stat_num_daily.append(sum(select_daily_df['Number of Tokens'].tolist()))

    return stat_num_daily, stat_num_breakfix, stat_num_deployment


def cost_stat(raw_data,site_list,city_list):
    cost_baseline = [600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600]
    stat_cost_breakfix = []
    stat_cost_deployment = []
    stat_cost_baseline = []

    for single_city in city_list:
        select_breakfix_df = raw_data[
            (raw_data['Site ID'].str.contains(single_city)) & (raw_data['project'] == 'N')]
        stat_cost_breakfix.append(sum(select_breakfix_df['Cost'].tolist()))

        select_deployment_df = raw_data[(raw_data['Site ID'].str.contains(single_city)) & (raw_data['project'] == 'Y')]
        stat_cost_deployment.append(sum(select_deployment_df['Cost'].tolist()))

        select_total_df = raw_data[raw_data['Site ID'].str.contains(single_city)]
        select_site_list = list(set(select_total_df['Site ID'].tolist()))
        total_baseline_cost = 0
        for single_site in select_site_list:
            site_index = site_list.index(single_site)
            single_site_price = cost_baseline[site_index]
            total_month = len(select_total_df[select_total_df['Site ID']==single_site])
            total_baseline_cost = total_baseline_cost + single_site_price * total_month
        stat_cost_baseline.append(total_baseline_cost)

    return stat_cost_breakfix, stat_cost_deployment, stat_cost_baseline
