from constants import *
from math import dist
from errors import InstanceError


def cost(instance, solution):
    """
    Main function calculating the score of a given solution to an instance
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the candidates
    :return: int score: the cost associated with the solution
    """
    const_cost = construction_cost(instance, solution)
    oper_cost = operational_cost(instance, solution)
    return oper_cost + const_cost


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

    # Then the costs associated with the substation-substation cables
    # BEWARE, since we duplicated each cable to treat them as two one-way cables in the converter
    # We will count each true cable twice, thus we divide the costs by two !!!

    for id, cable in solution[SUBSTATION_SUBSTATION_CABLES].items():
        # We compute the distance
        id1 = id
        id2 = cable[OTHER_SUB_ID]
        cable_type = cable[CABLE_TYPE_SUBSUB]
        pos_sub1 = (
            instance[SUBSTATION_LOCATION][id1][X],
            instance[SUBSTATION_LOCATION][id1][Y],
        )
        pos_sub2 = (
            instance[SUBSTATION_LOCATION][id2][X],
            instance[SUBSTATION_LOCATION][id2][Y],
        )
        dis_sub_sub = dist(pos_sub1, pos_sub2)
        cost += instance[SUB_SUB_CABLE_TYPES][cable_type][FIX_COST] / 2
        cost += instance[SUB_SUB_CABLE_TYPES][cable_type][VAR_COST] * dis_sub_sub / 2

    return cost


def no_failure_curtailing(instance, solution, power):
    """Computes the no-failure curtailing given the instance, a solution and the power in this scenario
    (C^n(x, y, omega) in the mathematical notations)
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the canditate
    :param power: the power generation in the wind scenario under which we compute this cost
    :return: score: the curtailing associated with the solution under this scenario
    """
    curtailing = 0
    for id, substation in solution[SUBSTATIONS].items():
        # We first compute how many turbines are linked to this substation
        linked_turbines = [
            1 for tu in solution[TURBINES].values() if tu[SUBSTATION_ID] == id
        ]
        curtailing += power * len(linked_turbines)
        sub_type = substation[SUB_TYPE]
        cable_type = substation[LAND_CABLE_TYPE]
        curtailing -= min(
            instance[SUBSTATION_TYPES][sub_type][RATING],
            instance[LAND_SUB_CABLE_TYPES][cable_type][RATING],
        )
    return max(0, curtailing)


def curtailing_failed_substation(instance, sub_id, turbines, power, cable):
    """Computes the curtailing of a given failed substation
    (First part of the (6) equation)
    :param instance: the instance addressed by the solution
    :param sub_id: the id of the current substation, used to compute how many turbines are attached
    :param substation: the dictionnary for the failed substation
    :param turbines: the dictionnary of the turbines
    :param power: the power generated under the current scenario
    :param cable: the cable that links this substation to another, if applicable
    returns the curtailing of failed substation"""
    curtailing = 0
    # First add the received power
    nb_turbines = len([1 for tu in turbines.values() if tu[SUBSTATION_ID] == sub_id])
    curtailing += power * nb_turbines
    # Then substract the power that is sent to another substation if applicable
    # If there is no such cable, the argument passed should be cable = None
    if cable:
        cable_type = cable[CABLE_TYPE_SUBSUB]
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


def curtailing_given_failed_sub(instance, solution, power, fail_id):
    """Computes the total curtailing given the instance, a solution, the generated power and the id of the failed substation
    (C^n(x, y, omega) in the mathematical notations)
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the canditate
    :param power: the power generation in the wind scenario under which we compute this cost
    :param fail_id: id of the failed substation
    :return: score: the curtailing associated with the solution under this scenario
    """
    cost = 0
    substations = solution[SUBSTATIONS]
    turbines = solution[TURBINES]
    # Cable linking this substation to another one, might be None
    cable = solution[SUBSTATION_SUBSTATION_CABLES].get(fail_id, None)
    # Power sent
    power_sent = 0
    if cable != None:
        nb_turbines = len(
            [1 for tu in turbines.values() if tu[SUBSTATION_ID] == fail_id]
        )
        cable_capa = instance[SUB_SUB_CABLE_TYPES][cable[CABLE_TYPE_SUBSUB]][RATING]
        power_sent = min(power * nb_turbines, cable_capa)
    # First add the cost of the curtailing of the failed substation
    cost += curtailing_failed_substation(instance, fail_id, turbines, power, cable)
    # Then iterate through the rest of the substations
    for id, sub in substations.items():
        # We already took this cost into account
        if id == fail_id:
            continue
        # If this substation is receiving from the failed one, compute the power received
        elif not (cable == None) and id == cable[OTHER_SUB_ID]:
            cost += curtailing_non_failed_substation(
                instance, id, sub, turbines, power, power_sent
            )
        else:
            cost += curtailing_non_failed_substation(instance, id, sub, turbines, power)

    return cost


def cost_of_curtailing(instance, curtailing):
    """Computes the cost of the given curtailing
    using the formula c^c(C) = c⁰C + c^p[C-C_max]⁺
    :param instance: the instance addressed by the solution
    :param curtailing: the curtailing we want to know the cost of
    :return: cost: the cost of the curtailing
    """
    linear_cost = instance[GEN_PARAMETERS][CURTAILING_COST]
    pena_cost = instance[GEN_PARAMETERS][CURTAILING_PENA]
    max_curtailing = instance[GEN_PARAMETERS][MAX_CURTAILING]
    cost = linear_cost * curtailing
    cost += pena_cost * max(0, curtailing - max_curtailing)
    return cost


def prob_failure(instance, substation):
    """Computes the probability of failure for a given substation
    :param instance: the instance addressed by the solution
    :param substation: the dictionnary of the substation we compute p^f for
    :return: prob: the probability of failure of this substation"""
    prob = 0
    sub_type = substation[SUB_TYPE]
    cab_type = substation[LAND_CABLE_TYPE]
    prob += instance[SUBSTATION_TYPES][sub_type][PROB_FAIL]
    prob += instance[LAND_SUB_CABLE_TYPES][cab_type][PROB_FAIL]
    return prob


def operational_cost(instance, solution):
    """Computes the operationnal cost of a given solution, defined in (7)
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the candidate
    :return: the operational cost of the solution"""
    cost = 0
    # We will keep the failure probas in memory for
    failure_probas = {}
    substations = solution[SUBSTATIONS]
    for id, sub in substations.items():
        failure_probas[id] = prob_failure(instance, sub)
    no_fail_proba = max(0, 1 - sum(failure_probas.values()))
    if not (0 <= no_fail_proba <= 1):
        raise InstanceError(
            [
                f"The probability of a non-failure should be in [0,1], but it is {no_fail_proba}"
            ]
        )
    # We then enumerate through the scenarios
    scenarios = instance[WIND_SCENARIOS]
    for scenario in scenarios.values():
        scenario_cost = 0
        scenario_power = scenario[POWER_GENERATION]
        scenario_prob = scenario[PROBABILITY]
        for id in substations.keys():
            fail_curt = curtailing_given_failed_sub(
                instance, solution, scenario_power, id
            )
            scenario_cost += failure_probas[id] * cost_of_curtailing(
                instance, fail_curt
            )
        no_fail_curtailing = no_failure_curtailing(instance, solution, scenario_power)
        scenario_cost += no_fail_proba * cost_of_curtailing(
            instance, no_fail_curtailing
        )
        cost += scenario_prob * scenario_cost
    return cost
