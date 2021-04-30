import pandas as pd
def power_integrated(power_data):
    date_list = list(set(power_data['Key'].tolist()))
    date_list.sort()
    new_total_power_value_list = []
    avg_new_total_power_value_list = []
    for single_date in date_list:
        # new_total_power_value = power_data[power_data['Key'] == single_date]['Value'].tolist()[0] + \
        #                         power_data[power_data['Key'] == single_date]['Value'].tolist()[1]
        new_total_power_value = sum(power_data[power_data['Key'] == single_date]['Value'].tolist())
        new_total_power_value_list.append(new_total_power_value)
        avg_new_total_power_value_list.append(new_total_power_value/len(power_data[power_data['Key'] == single_date]['Value'].tolist()))
    power_integrated_data = pd.DataFrame([])
    power_integrated_data['Key'] = date_list
    power_integrated_data['Value'] = new_total_power_value_list
    power_integrated_data['Avg_Value'] = avg_new_total_power_value_list
    return power_integrated_data