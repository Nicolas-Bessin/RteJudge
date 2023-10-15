from constants import *
from math import dist


def cost(instance, solution):
    """
    Main function calculating the score of a given solution to an instance
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the candidates
    :return: int score: the cost associated with the solution
    """
    return cost


def construction_cost(instance, solution):
    """
    Function calculating the construction cost of a given solution to an instance
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the candidates
    :return: int score: the cost associated with the solution
    """
    cost = 0
    # First we add the cost associated with the substations
    for id, substation in solution[SUBSTATIONS].items():
        # We first add the cost of building this substation
        cost += instance[SUBSTATION_TYPES][substation[SUB_TYPE]][COST]
        # We then compute the length of the substation-land cable
        sub_pos = (
            instance[SUBSTATION_LOCATION][id][X],
            instance[SUBSTATION_LOCATION][id][Y],
        )
        land_pos = (
            instance[GEN_PARAMETERS][MAIN_LAND_STATION][X],
            instance[GEN_PARAMETERS][MAIN_LAND_STATION][Y],
        )
        dis_sub_land = dist(sub_pos, land_pos)
        cable_type = substation[LAND_CABLE_TYPE]
        cost += instance[LAND_SUB_CABLE_TYPES][cable_type][FIX_COST]
        cost += instance[LAND_SUB_CABLE_TYPES][cable_type][VAR_COST] * dis_sub_land
        # We then add the cost of the substation- substation cable, if there is one.
        if not (substation[LINKED_TO_ANOTHER]):
            continue
        linked_id = substation[LINKED_SUB_ID]
        linked_sub_pos = (
            instance[SUBSTATION_LOCATION][linked_id][X],
            instance[SUBSTATION_LOCATION][linked_id][Y],
        )
        dis_sub_sub = dist(sub_pos, linked_sub_pos)
        link_cable_type = substation[LINKED_CABLE_TYPE]
        cost += instance[SUB_SUB_CABLE_TYPES][link_cable_type][FIX_COST]
        cost += instance[SUB_SUB_CABLE_TYPES][link_cable_type][VAR_COST] * dis_sub_sub

    # Then the costs associated with the turbines
    for id, turbine in solution[TURBINES].items():
        # We compute the distance to the substation
        sub_id = turbine[SUBSTATION_ID]
        sub_pos = (
            instance[SUBSTATION_LOCATION][sub_id][X],
            instance[SUBSTATION_LOCATION][sub_id][Y],
        )
        turb_pos = (instance[WIND_TURBINES][id][X], instance[WIND_TURBINES][id][Y])
        dis_turb_sub = dist(sub_pos, turb_pos)
        cost += instance[GEN_PARAMETERS][FIX_COST_CABLE]
        cost += instance[GEN_PARAMETERS][VAR_COST_CABLE] * dis_turb_sub

    return cost


def no_failure_cost(instance, solution, power):
    """Computes the no-failure cost given the instance, a solution and the power in this scenario
    (C^n(x, y, omega) in the mathematical notations)
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the canditate
    :param power: the power generation in the wind scenario under which we compute this cost
    :return: score: the cost associated with the solution under this scenario
    """
    cost = 0
    for id, substation in solution[SUBSTATIONS].items():
        # We first compute how many turbines are linked to this substation
        linked_turbines = [
            1 for tu in solution[TURBINES].values() if tu[SUBSTATION_ID] == id
        ]
        missing_capacity = power * len(linked_turbines)
        sub_type = substation[SUB_TYPE]
        cable_type = substation[LAND_CABLE_TYPE]
        missing_capacity -= min(
            instance[SUBSTATION_TYPES][sub_type][RATING],
            instance[LAND_SUB_CABLE_TYPES][cable_type][RATING],
        )
        cost += max(missing_capacity, 0)
    return cost


def curtailing_failed_substation(instance, sub_id, substation, turbines, power):
    """Computes the curtailing of a given failed substation
    (First part of the (6) equation)
    :param instance: the instance addressed by the solution
    :param sub_id: the id of the current substation, used to compute how many turbines are attached
    :param substation: the dictionnary for the failed substation
    :param turbines: the dictionnary of the turbines
    :param power: the power generated under the current scenario
    returns the curtailing of failed substation"""
    curtailing = 0
    # First add the received power
    nb_turbines = len([1 for tu in turbines.values() if tu[SUBSTATION_ID] == sub_id])
    curtailing += power * nb_turbines
    # Then substract the power that is sent to another substation if applicable
    if substation[LINKED_TO_ANOTHER]:
        cable_type = substation[LINKED_CABLE_TYPE]
        curtailing -= instance[SUB_SUB_CABLE_TYPES][cable_type][RATING]
    return max(0, curtailing)


def curtailing_non_failed_substation(
    instance, sub_id, substation, turbines, power, power_from_failed=0
):
    """Computes the curtailing of a given substation
    (First part of the (6) equation)
    :param instance: the instance addressed by the solution
    :param sub_id: the id of the current substation, used to compute how many turbines are attached
    :param substation: the dictionnary for the failed substation
    :param turbines: the dictionnary of the turbines
    :param power: the power generated under the current scenario
    :param power_from_failed: The power received from the failed substation (0 by default)
    :return: the curtailing of the substation"""
    curtailing = 0
    # First add the power from the turbines
    nb_turbines = len([1 for tu in turbines.values() if tu[SUBSTATION_ID] == sub_id])
    curtailing += power * nb_turbines
    # Then the power received from failed substation
    curtailing += power_from_failed
    # Then substract the capacity of this substation
    sub_type, cable_type = substation[SUB_TYPE], substation[LAND_CABLE_TYPE]
    sub_capacity = instance[SUBSTATION_TYPES][sub_type][RATING]
    cable_capacity = instance[LAND_SUB_CABLE_TYPES][cable_type][RATING]

    capacity = min(sub_capacity, cable_capacity)
    curtailing -= capacity

    return max(0, curtailing)


def failure_cost(instance, solution, power, fail_id):
    """Computes the failure cost given the instance, a solution, the generated power and the id of the failed substation
    (C^n(x, y, omega) in the mathematical notations)
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the canditate
    :param power: the power generation in the wind scenario under which we compute this cost
    :param fail_id: id of the failed substation
    :return: score: the cost associated with the solution under this scenario
    """
    cost = 0
    substations = solution[SUBSTATIONS]
    turbines = solution[TURBINES]
    # Linked station, might be None
    linked_id = substations[fail_id][LINKED_SUB_ID]
    # Power sent
    power_sent = 0
    if linked_id != None:
        nb_turbines = len(
            [1 for tu in turbines.values() if tu[SUBSTATION_ID] == fail_id]
        )
        cable_capa = instance[SUB_SUB_CABLE_TYPES][
            substations[fail_id][LINKED_CABLE_TYPE]
        ][RATING]
        power_sent = min(power * nb_turbines, cable_capa)
    # First add the cost of the curtailing of the failed substation
    cost += curtailing_failed_substation(
        instance, fail_id, substations[fail_id], turbines, power
    )
    # Then iterate through the rest of the substations
    for id, sub in substations.items():
        # We already took this cost into account
        if id == fail_id:
            continue
        # If this substation is receiving from the failed, compute the power received
        elif id == linked_id:
            cost += curtailing_non_failed_substation(
                instance, id, sub, turbines, power, power_sent
            )
        else:
            cost += curtailing_non_failed_substation(instance, id, sub, turbines, power)

    return cost
