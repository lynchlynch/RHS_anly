def de_zero(raw_data):
    delete_index_list = []
    for index in range(10,len(raw_data)-10):
        current_value = raw_data['Value'].tolist()[index]
        if current_value == 0 and raw_data['Value'].tolist()[index-10] != 0 and raw_data['Value'].tolist()[index+10] != 0:
            # delete_index_list.append(index)
            #pre_first_nonzero and post_first_nonzero
            pre_first = 0
            post_first = 0
            for i in range(1,10):
                if raw_data['Value'].tolist()[index-i] != 0 and pre_first ==0:
                    pre_first = raw_data['Value'].tolist()[index-i]
                if raw_data['Value'].tolist()[index+i] != 0 and post_first ==0:
                    post_first = raw_data['Value'].tolist()[index+i]
                if post_first * pre_first != 0:
                    break

            raw_data.loc[index,'Value'] = round((pre_first + post_first)/2,4)

    return raw_data