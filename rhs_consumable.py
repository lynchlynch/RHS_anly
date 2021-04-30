def rhs_consumable(rhs_log,site_id,raw_data):
    raw_data_first_year = int(raw_data['Key'].tolist()[0].split('-')[0])
    raw_data_first_month = int(raw_data['Key'].tolist()[0].split('-')[1])
    raw_data_last_year = int(raw_data['Key'].tolist()[-1].split('-')[0])
    raw_data_last_month = int(raw_data['Key'].tolist()[-1].split('-')[1])
    year_month_list = []
    for single_year in list(range(raw_data_first_year, raw_data_last_year + 1)):
        if single_year == raw_data_last_year:
            for single_month in list(range(1, raw_data_last_month + 1)):
                year_month_list.append(str(single_year) + '-' + str(single_month))
        elif single_year == raw_data_first_year:
            for single_month in list(range(raw_data_first_month, 13)):
                year_month_list.append(str(single_year) + '-' + str(single_month))
        else:
            for single_month in list(range(1, 13)):
                year_month_list.append(str(single_year) + '-' + str(single_month))

    rhs_times_index_list = []
    date_list_sample = []
    total_module_num_list = []
    for single_year_month in year_month_list:
        select_rhs_df = rhs_log[(rhs_log['Site ID'] == site_id) & (rhs_log['Request Year-Month'] == single_year_month) &
                                (rhs_log['project'] == 'N')]
        if int(single_year_month.split('-')[1]) < 10:
            new_single_year_month = single_year_month.split('-')[0] + '-0' + str(single_year_month.split('-')[1])
        else:
            new_single_year_month = single_year_month

        rhs_times_index_list.append(raw_data['Key'].tolist().index(new_single_year_month + '-15'))
        date_list_sample.append(new_single_year_month + '-15')

        # 统计模块总数
        total_module_num = 0
        for index in range(len(select_rhs_df)):
            if select_rhs_df['Module'].tolist()[index] != 'N':
                single_module_num = int(select_rhs_df['Module'].tolist()[index].split('个')[0])
                total_module_num += single_module_num
            else:
                continue

        total_module_num_list.append(total_module_num)
    # print(total_module_num_list)
    return date_list_sample, rhs_times_index_list, total_module_num_list