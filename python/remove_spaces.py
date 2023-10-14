def remove_space_from_keys(dic):
    """Removes the spaces in the keys of dic.keys()"""
    clean_dic = {}
    for key in dic.keys():
        clean_dic[key.strip()] = dic[key]
    return clean_dic


def clean_keys(raw_data):
    """Function that removes the whitespaces from keys in the dictionnary given,
    Ony works with the formatting of instances in the 2023 KIRO editon
    """
    raw_data = remove_space_from_keys(raw_data)
    clean_data = {}
    # Remove spaces from every keys
    for key in raw_data.keys():
        if type(raw_data[key]) == dict:
            clean_data[key] = remove_space_from_keys(raw_data[key])
            for k in clean_data[key].keys():
                if type(clean_data[key][k]) == dict:
                    clean_data[key][k] = remove_space_from_keys(clean_data[key][k])
        else:
            lis = raw_data[key]
            clean_lis = []
            for dic in lis:
                clean_lis.append(remove_space_from_keys(dic))
            clean_data[key] = clean_lis
    return clean_data
