from constants import *


def cost(instance, solution):
    """
    Main function calculating the score of a given solution to an instance
    :param instance: the instance addressed by the solution
    :param solution: the solution given by the candidates
    :return: int score: the cost associated with the solution
    """
    cost = 0
    alpha = instance[PARAMETERS][COSTS][UNIT_PENALTY]
    beta = instance[PARAMETERS][COSTS][TARDINESS]

    for job in instance[JOBS].values():
        weight_j = job[WEIGHT]
        task_sequence = job[SEQUENCE]
        last_task_indice = task_sequence[-1]
        completed_time = (
            solution[last_task_indice][START]
            + instance[TASKS][last_task_indice][PROCESSING_TIME]
        )  # Time when the job have been entirely completed
        tardiness = max([0, completed_time - job[DUE_DATE]])
        penalty = tardiness > 0
        cost += weight_j * (completed_time + alpha * penalty + beta * tardiness)
    return cost
