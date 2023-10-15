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
    Function calculating the building cost of a given solution to an instance
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
    :return: score: the cost associated with the solution under this scenario"""
    cost = 0
    for id, substation in solution[SUBSTATIONS].items():
        # We first compute how many turbines are linked to this substation
        linked_turbines = [
            tu_id for tu_id, tu in solution[TURBINES].items() if tu[SUBSTATION_ID] == id
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
