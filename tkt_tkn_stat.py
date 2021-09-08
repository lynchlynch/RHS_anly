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
    # charged = [0,0,0,0,0]
    # un_charged = [0,0,0,0,0]
    stat_num_charged = []
    stat_num_un_charged = []
    # for single_site in site_list:
    for single_city in city_list:
        print(raw_data[single_city in raw_data['Site ID']])
        select_charged_df = raw_data[(single_city in raw_data['Site ID'])&(raw_data['Token Type']!='Daily-A')]
        stat_num_charged.append(sum(select_charged_df['Number of Tokens'].tolist()))
        select_un_charged_df = raw_data[(single_city in raw_data['Site ID'])&(raw_data['Token Type']=='Daily-A')]
        stat_num_un_charged.append(sum(select_un_charged_df['Number of Tokens'].tolist()))



    return stat_num_charged,stat_num_un_charged