from errors import InstanceError
from constants import *

def list_to_dic(lis, key_of_list, str_list):
    """Converts a list of dictionnaries dic containing an "id" key
    to a dictionnary where the keys are the values of "id" for each dic in the list
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


def convert_instance(raw_instance):
    

