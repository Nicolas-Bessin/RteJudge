from constants import *
from errors import InstanceError


def solution_converter(solution):
    """Function that transforms the lists in the solution dictionnary into dictionnaries
    indexed by the ids of the objects in order to have access to the right task more easily."""
    str_errors = []

    converted_solution = {}
    for task_dictionnary in solution:
        task_id = task_dictionnary[TASK]
        if task_id in converted_solution.keys():
            str_errors.append(f"Task {task_id} is defined multiple time")
        converted_solution[task_id] = task_dictionnary

    if str_errors:
        raise InstanceError(str_errors)

    return converted_solution


def instance_converter(instance):
    """Function that transforms the lists in the instance dictionnary into dictionnaries
    indexed by the ids of the objects in order to have access to them more easily."""
    converted_instance = {}
    converted_instance[PARAMETERS] = instance[PARAMETERS]
    converted_instance[JOBS] = {}
    for job_dictionnary in instance[JOBS]:
        converted_instance[JOBS][job_dictionnary[JOB]] = job_dictionnary
    converted_instance[TASKS] = {}
    for task_dictionnary in instance[TASKS]:
        converted_instance[TASKS][task_dictionnary[TASK]] = {}
        converted_instance[TASKS][task_dictionnary[TASK]][TASK] = task_dictionnary[TASK]
        converted_instance[TASKS][task_dictionnary[TASK]][
            PROCESSING_TIME
        ] = task_dictionnary[PROCESSING_TIME]
        converted_instance[TASKS][task_dictionnary[TASK]][MACHINES] = {}
        for machine_dictionnary in task_dictionnary[MACHINES]:
            converted_instance[TASKS][task_dictionnary[TASK]][MACHINES][
                machine_dictionnary[MACHINE]
            ] = machine_dictionnary
    return converted_instance
