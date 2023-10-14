from errors import InstanceError
from constants import *


def list_to_dic(lis, key_of_list, str_list):
    """Converts a list of dictionnaries e containing an "id" key
    to a dictionnary where the keys are the values of "id" for each e in the list
    key_of_list is passed as argument have a coherent error message in case of a problem
    """
    return_dic = {}
    for i in range(len(lis)):
        dic = lis[i]
        if type(dic) != dict:
            str_list.append(
                f"In the list of {key_of_list}, the element {i} is not a dictionnary"
            )
            raise InstanceError(str_list)
        id = dic.pop(ID, None)
        if id == None:
            str_list.append(
                f"A {key_of_list[:-1]} is present but is missing an '{ID}' key"
            )
            raise InstanceError(str_list)
        if id in return_dic.keys():
            if key_of_list == SUBSTATIONS:
                str_list.append(f"Two or more substation are built on site {id}")
            elif key_of_list == TURBINES:
                str_list.append(f"There are two or more turbines with id {id}")
        return_dic[id] = dic
    return return_dic


def converter(dic):
    """Converts every list in the input / ouptut dictionnaries into a dictionnary,
    with the keys being the ids (We have list[i]["id"] = i+1 in 2023's instances),
    so that we don't have to take into account the fact that the ids begin at 1
    and list indices at 0.
    This year, the lists are always at depth 1 in the dictionnaries (e.g. outdata["turbines"], indata["substation_types"], etc)
    """
    str_errors = []  # List of errors
    converted = {}  # New dictionnary
    for key in dic.keys():
        data = dic[key]
        dic_from_list = {}
        if type(data) == list:
            converted[key] = list_to_dic(data, key, str_errors)
        else:
            converted[key] = data
    if str_errors:
        raise InstanceError(str_errors)
    return converted


if __name__ == "__main__":
    import os
    import loader

    size = "tiny"
    curr_path = os.path.dirname(__file__)
    file_in = curr_path + f"/../instances/input/{size}.json"
    file_out = curr_path + f"/../instances/output/{size}_sol.json"
    name, ext = os.path.splitext(file_out)
    file_out_conv = name + "_conv" + ext
    name, ext = os.path.splitext(file_in)
    file_in_conv = name + "_conv" + ext
    out_conv = converter(loader.load_json(file_out))
    in_conv = converter(loader.load_json(file_in))
    loader.save_json(out_conv, file_out_conv)
    loader.save_json(in_conv, file_in_conv)
