def tkt_stat(raw_data,site_list):
    ct_list = []
    cm_list = []
    cu_list = []
    third_part_list = []
    stat_num = []
    for single_site in site_list:
        select_df = raw_data['Site ID'==single_site]
        stat_num.append(len(select_df))
