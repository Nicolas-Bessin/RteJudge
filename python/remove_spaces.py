from constants import *
import json
import os

size = "tiny"
curr_path = os.path.dirname(__file__)
file_in = curr_path + f"/../instances/input/{size}.json"
file_out = curr_path + f"/../instances/output/{size}_sol.json"


def remove_space_from_keys(dic):
    clean_dic = {}
    for key in dic.keys():
        clean_dic[key.strip()] = dic[key]
    return clean_dic


def clean(filename):
    with open(filename) as f:
        raw_data = json.load(f)
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

    with open(filename, "w") as f:
        json.dump(clean_data, f, indent=4)

    return None


clean(file_in)
clean(file_out)
