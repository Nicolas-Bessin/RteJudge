from constants import *
from errors import InstanceError


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
    check_list_subsub_cables(solution)
    check_substations_content(solution, instance)
    check_turbines_content(solution, instance)
    check_subsub_cables_content(solution, instance)


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
            f"The solution must contain exactly three keys : '{SUBSTATIONS}' and '{TURBINES}' and '{SUBSTATION_SUBSTATION_CABLES}"
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
                str_errors.append(
                    f"In {SUBSTATIONS}, key '{key}' is missing from the substation {i+1}"
                )
            for key in extra_keys:
                str_errors.append(
                    f"In {SUBSTATIONS}, key '{key}' is not expected in the substationn {i+1}"
                )
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
                str_errors.append(
                    f"In {TURBINES}, key {key} is missing from the dictionnary {i+1}"
                )
            for key in extra_keys:
                str_errors.append(
                    f"In {TURBINES}, key {key} is not expected in the dictionnary {i+1}"
                )
    if str_errors:
        raise InstanceError(str_errors)


def check_list_subsub_cables(solution):
    """Function checking that the list of substation-substation cables is in the right format
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []
    sub_sub_cables = solution[SUBSTATION_SUBSTATION_CABLES]
    if type(sub_sub_cables) != list:
        str_errors.append(
            f"The element at key '{SUBSTATION_SUBSTATION_CABLES}' is not a list"
        )
        raise InstanceError(str_errors)

    for i, subsubcab_dict in enumerate(sub_sub_cables):
        if (type(subsubcab_dict)) != dict:
            str_errors.append(
                f"The list of substation-substation cables must contains dictionnaries"
            )
            raise InstanceError(str_errors)

        if set(KEYS_EXPECTED_SUB_SUB_CABLE) != set(subsubcab_dict.keys()):
            missing_keys = set(KEYS_EXPECTED_SUB_SUB_CABLE) - set(subsubcab_dict.keys())
            extra_keys = set(subsubcab_dict.keys()) - set(KEYS_EXPECTED_SUB_SUB_CABLE)
            for key in missing_keys:
                str_errors.append(
                    f"In {SUBSTATION_SUBSTATION_CABLES}, key {key} is missing from the dictionnary {i+1}"
                )
            for key in extra_keys:
                str_errors.append(
                    f"In {SUBSTATION_SUBSTATION_CABLES}, key {key} is not expected in the dictionnary {i+1}"
                )

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
    MATCHING = {
        ID: SUBSTATION_LOCATION,
        SUB_TYPE: SUBSTATION_TYPES,
        LAND_CABLE_TYPE: LAND_SUB_CABLE_TYPES,
    }
    for i, substation in enumerate(substations_list):
        # WE ASSUME THE IDS ARE 1 ... N, WITHOUT ANY SKIPS
        # Check the contents where the constraint is being an integer && 1 <= some_id <= max_id
        for key, instance_key in MATCHING.items():
            max_value = len(instance[instance_key])
            id = substation[key]
            if not (type(id)) == int:
                str_errors.append(f"The {key} of substation {i+1} must be an integer")
            elif not (1 <= id <= max_value):
                str_errors.append(
                    f"The {key} of substation {i+1} is not valid, it does not exist in the list of {instance_key}"
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


def check_subsub_cables_content(solution, instance):
    """
    Function checking that the data for substation-substation cables is valid
    -SUBSTATION_ID and OTHER_SUB_ID are within the ids where substations are built
    -CABLE_TYPE is within the allowed ids for sub-sub cable ids
    :param solution: the solution given by the candidate
    :param instance: the instance addressed by the solution
    :return raises InstanceError: if an error is found
    """
    str_errors = []
    # WE ASSUME TURBINE IDs ARE 1 ... N WITHOUT SKIPS
    max_id_cable = len(instance[SUB_SUB_CABLE_TYPES])
    built_substation_ids = set([sub[ID] for sub in solution[SUBSTATIONS]])
    cables_lis = solution[SUBSTATION_SUBSTATION_CABLES]
    for i, cable in enumerate(cables_lis):
        # Turbine ID
        id1 = cable[SUBSTATION_ID]
        id2 = cable[OTHER_SUB_ID]
        cable_type = cable[CABLE_TYPE_SUBSUB]
        if not type(id1) == int:
            str_errors.append(f"For cable {i+1}, {SUBSTATION_ID} must be an integer")
        if not type(id2) == int:
            str_errors.append(f"For cable {i+1}, {OTHER_SUB_ID} must be an integer")
        if not type(cable_type) == int:
            str_errors.append(
                f"For cable {i+1}, {CABLE_TYPE_SUBSUB} must be an integer"
            )

        if id1 not in built_substation_ids:
            str_errors.append(
                f"The cable {i+1} is linked to the substation {id1}, which does not exist."
            )
        if id2 not in built_substation_ids:
            str_errors.append(
                f"The cable {i+1} is linked to the substation {id2}, which does not exist."
            )
        if not (1 <= cable_type <= max_id_cable):
            str_errors.append(
                f"For cable {i+1}, the {CABLE_TYPE_SUBSUB} is not valid, it does not exist in the list of substation-substation cable types"
            )
    if str_errors:
        raise InstanceError(str_errors)
