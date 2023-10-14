from constants import *
from errors import InstanceError
from converter import instance_converter


def solution_checker(instance, solution):
    """
    Verifies if the solution provided is correctly written
    :param instance: The instance it refers to
    :param solution: The solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    check_format(solution)
    check_list_substations(solution)
    check_list_turbines(solution)
    check_substations_content(solution, instance)
    check_turbines_content(solution, instance)


def check_format(solution):
    """
    Function checking if the solution is really dictionnary with two keys,
    SUBSTATIONS and TURBINES; for which the data is a list of dictionnaries,
    one for each substation built / for each turbine
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []

    # We first verify that the solution instance is indeed a dictionnary
    if type(solution) is not dict:
        str_errors.append(f"The solution isn't a dictionnary")
        raise InstanceError(str_errors)
    # Now that we know that it's a dictionnary, we must first check the keys
    if set(solution.keys()) != set(KEYS_EXPECTED):
        str_errors.append(
            f"The solution must contain exactly two keys : '{SUBSTATIONS}' and '{TURBINES}'"
        )

    if str_errors:
        raise InstanceError(str_errors)


def check_list_substations(solution):
    """Function checking that the list of substations is in the right format
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []
    substations = solution[SUBSTATIONS]
    if type(substations) != list:
        str_errors.append(f"The element at key '{SUBSTATIONS}' is not a list")

    for i, sub_dict in enumerate(substations):
        if (type(sub_dict)) != dict:
            str_errors.append(f"The list of substations must contains dictionnaries")

        if set(KEYS_EXPECTED_SUBSTATION) != set(sub_dict.keys()):
            missing_keys = set(KEYS_EXPECTED_SUBSTATION) - set(sub_dict.keys())
            extra_keys = set(sub_dict.keys()) - set(KEYS_EXPECTED_SUBSTATION)
            for key in missing_keys:
                str_errors.append(f"Key {key} is missing from the dictionnary {i+1}")
            for key in extra_keys:
                str_errors.append(f"Key {key} is not expected in the dictionnary {i+1}")
    if str_errors:
        raise InstanceError(str_errors)


def check_list_turbines(solution):
    """Function checking that the list of turbines is in the right format
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []
    turbines = solution[TURBINES]
    if type(turbines) != list:
        str_errors.append(f"The element at key '{TURBINES}' is not a list")
        raise InstanceError(str_errors)

    for i, tur_dict in enumerate(turbines):
        if (type(tur_dict)) != dict:
            str_errors.append(f"The list of turbines must contains dictionnaries")
            raise InstanceError(str_errors)

        if set(KEYS_EXPECTED_TURBINES) != set(tur_dict.keys()):
            missing_keys = set(KEYS_EXPECTED_TURBINES) - set(tur_dict.keys())
            extra_keys = set(tur_dict.keys()) - set(KEYS_EXPECTED_TURBINES)
            for key in missing_keys:
                str_errors.append(f"Key {key} is missing from the dictionnary {i+1}")
            for key in extra_keys:
                str_errors.append(f"Key {key} is not expected in the dictionnary {i+1}")
    if str_errors:
        raise InstanceError(str_errors)


def check_substations_content(solution, instance):
    """
    Function checking that every substation data is valid :
    -id is within the allowed IDs of building sites
    -substation type is within the IDs of substation types
    -land_cable_type is within the IDs of land-substation cables
    -linked_to_another is either 1 or 0
    -linked_substation_id is an integer, corresponding to another substation defined in the solution or is null
    -linked_cable_type is within the IDs of substation-substation cables or is null
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []
    substations_list = solution[SUBSTATIONS]
    # WE ASSUME THE IDS ARE 1 ... N, WITHOUT ANY SKIPS
    built_substation_ids = set([sub[ID] for sub in substations_list])
    max_id_sub_cable = len(instance[SUB_SUB_CABLE_TYPES])
    MATCHING = {
        ID: SUBSTATION_LOCATION,
        SUB_TYPE: SUBSTATION_TYPES,
        LAND_CABLE_TYPE: LAND_SUB_CABLE_TYPES,
    }
    for i, substation in substations_list:
        # First check the contents where the constraint is being an integer && 1 <= some_id <= max_id
        for key, instance_key in MATCHING.items():
            max_value = len(instance[instance_key])
            id = substation[key]
            if not (type(id)) == int:
                str_errors.append(f"The {key} of substation {i+1} must be an integer")
            if not (1 <= id <= max_value):
                str_errors.append(
                    f"The {key} of substation {i+1} is not valid, it does not exist in the list of {instance_key}"
                )
        # Linked to another
        linked = substation[LINKED_TO_ANOTHER]
        if not (0 <= linked <= 1 and type(linked) == int):
            str_errors.append(
                f"The {LINKED_TO_ANOTHER} paramater of substation {i+1} must be either 1 or 0"
            )
        # Id of linked substation
        linked_sub = substation[LINKED_SUB_ID]
        if not (linked_sub == None or type(linked_sub) == int):
            str_errors.append(
                f"The id for the linked substation of substation {i+1} must be an integer"
            )
        if not (linked_sub == None or linked_sub in built_substation_ids):
            str_errors.append(
                f"The substation {i+1} is linked to a substation that doesn't exist"
            )
        # Link cable type
        linked_cable = substation[LINKED_CABLE_TYPE]
        if not (linked_cable == None or type(linked_cable) == int):
            str_errors.append(
                f"The linked_cable_type for substation {i+1} must be an integer"
            )
        if not (linked_cable == None or 1 <= linked_cable <= max_id_sub_cable):
            str_errors.append(
                f"The link cable type of substation {i + 1} is not valid - it doesn't exist in the list of substation-substation cable types"
            )
        # Link cable type must be None if liked_sub is None and vice-versa
        if linked_sub == None != linked_cable == None:
            str_errors.append(
                f"In substation {i + 1}, one of '{LINKED_CABLE_TYPE}' and '{LINKED_SUB_ID}' is None and not the other. "
            )

    if str_errors:
        raise InstanceError(str_errors)


def check_turbines_content(solution, instance):
    """
    Function checking that the data for turbines is valid
    -id is within the allowed IDs of turbines
    -substation_id is within the IDs of the built substations
    -every turbine id is present
    """
    str_errors = []
    turbines_list = []
    # WE ASSUME TURBINE IDs ARE 1 ... N WITHOUT SKIPS
    max_id_turbine = len(instance[WIND_TURBINES])
    built_substation_ids = set([sub[ID] for sub in solution[SUBSTATIONS]])
    turbines_list = solution[TURBINES]
    expected_ids = set(range(1, max_id_turbine + 1))
    encountered_id = set()
    for i, turbine in enumerate(turbines_list):
        # Turbine ID
        tur_id = turbine[ID]
        if tur_id in encountered_id:
            str_errors.append(f"The turbine with id {tur_id} appears at least twice")
        else:
            encountered_id.add(tur_id)
        if not (type(tur_id) == int):
            str_errors.append(f"The id of turbine {i+1} must be an integer")
        if not (1 <= tur_id <= max_id_turbine):
            str_errors.append(
                f"The id of turbine {i + 1} is not valid - it doesn't exist in the list of turbines"
            )
        linked_sub = turbine[SUBSTATION_ID]
        if not (type(linked_sub) == int):
            str_errors.append(
                f"The id for the linked substation of turbine {i+1} must be an integer"
            )
        if not (linked_sub in built_substation_ids):
            str_errors.append(
                f"The turbine {i+1} is linked to a substation that doesn't exist"
            )
    missing_ids = expected_ids - encountered_id
    for id in missing_ids:
        str_errors.append(
            f"The turbine with id {id} does not appear in the list of turbines, but it should"
        )
    if str_errors:
        raise InstanceError(str_errors)
