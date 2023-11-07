from errors import InstanceError
from constants import *


def list_to_dic_ids(lis, key_of_list, str_list):
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
            # key_of_list[:-1] to remove the s, I hate that I coded that, this is ugly
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


def list_to_dic_pairs(lis, key_of_list, str_list):
    """Converts a list of dictionnaries dic containing two ids
    to a dictionnaries of two one-way cables per initial cable, with ids as keys.
    :param list: The list we want to convert
    :param key_of_list: The name of this list, needed for error messages
    :param str_list: list of errors
    :returns a converted dictionnary as described:
    """
    return_dic = {}

    for i in range(len(lis)):
        dic = lis[i]
        if type(dic) != dict:
            str_list.append(
                f"In the list of {key_of_list}, the element {i} is not a dictionnary"
            )
            raise InstanceError(str_list)
        id1 = dic.pop(SUBSTATION_ID, None)
        id2 = dic.pop(OTHER_SUB_ID, None)
        if id1 == None or id2 == None:
            str_list.append(
                f"A {key_of_list[:-1]} is present but is missing either a {SUBSTATION_ID} or a {OTHER_SUB_ID} key "
            )
            raise InstanceError(str_list)

        if id1 in return_dic.keys():
            str_list.append(
                f"The substation {id1} is linked to two or more substations, this is not allowed"
            )
        if id2 in return_dic.keys():
            str_list.append(
                f"The substation {id2} is linked to two or more substations, this is not allowed"
            )
        # Add a dictionnary for the (fictionnal) one way cable from id1 to id2
        # Makes it easier to compute the cost -> we just grab the cable at id, and see its type and where it goes.
        return_dic[id1] = {OTHER_SUB_ID: id2, CABLE_TYPE_SUBSUB: dic[CABLE_TYPE_SUBSUB]}
        # The same, symetrically.
        # We effectively treat our two ways cable as two one way cable, one each way.
        return_dic[id2] = {OTHER_SUB_ID: id1, CABLE_TYPE_SUBSUB: dic[CABLE_TYPE_SUBSUB]}

    return return_dic


def convert_instance(raw_instance):
    """Convert the lists in raw_instance, all containing dictionnaries with a key 'id'
    to a dictionnary with keys being the value of 'id'
    :param solution: The solution given by the candidate
    :returns a converted dictionnary as described
    :raises InstanceError with details in case it spots an error
    """
    return_dic = {}
    return_dic[GEN_PARAMETERS] = raw_instance[GEN_PARAMETERS]
    str_errors = []
    # List of keys in instance where the data is a list of dictionnaries with an "id" key
    keys_with_list = [
        SUBSTATION_TYPES,
        LAND_SUB_CABLE_TYPES,
        SUB_SUB_CABLE_TYPES,
        SUBSTATION_LOCATION,
        WIND_TURBINES,
        WIND_SCENARIOS,
    ]
    for key in keys_with_list:
        return_dic[key] = list_to_dic_ids(raw_instance[key], key, str_errors)

    if str_errors:
        raise InstanceError(str_errors)

    return return_dic


def convert_solution(raw_solution):
    """Convert the lists in raw_instance, all containing dictionnaries with a key 'id'
    to a dictionnary with keys being the value of 'id'
    :param solution: The solution given by the candidate
    :returns a converted dictionnary as described
    :raises InstanceError with details in case it spots an error
    NOTA BENE : This function is checking constraint (1), it raises an exception if two or more
    substations have the same id (i.e. are built on the same site)
    NOTA BENE : This function is checking constraint (4), it raises an exception if a substation
    is linked to two or more other substations.
    """
    return_dic = {}
    str_errors = []
    for key in KEYS_EXPECTED_IDS:
        return_dic[key] = list_to_dic_ids(raw_solution[key], key, str_errors)
    for key in KEYS_EXPECTED_PAIRS:
        return_dic[key] = list_to_dic_pairs(raw_solution[key], key, str_errors)

    if str_errors:
        raise InstanceError(str_errors)

    return return_dic
