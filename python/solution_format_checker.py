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
    check_all_keys(solution)
    check_int(solution)
    existing_elements(solution, instance)


def check_format(solution):
    """
    Function checking if the solution is really a list and if
    all elements of this list are dictionnaries
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []

    # We first verify that the solution instance is indeed a list
    if type(solution) is not list:
        str_errors.append("The solution given isn't a list")
        raise InstanceError(str_errors)
    # Now that we know that it's a list we can check all its elements
    for element in solution:
        if type(element) is not dict:
            str_errors.append(f"Element {element} is not a dictionnary")

    if str_errors:
        raise InstanceError(str_errors)


def check_all_keys(solution):
    """
    Function checking if all keys are good ones for each dictionnary of the solution
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []

    for (i, task_dictionnary) in enumerate(solution):
        if set(KEYS_EXPECTED) != set(task_dictionnary.keys()):
            extra_keys = set(task_dictionnary.keys()) - set(KEYS_EXPECTED)
            missing_keys = set(KEYS_EXPECTED) - set(task_dictionnary.keys())
            for key in missing_keys:
                str_errors.append(f"Key {key} is missing from the dictionnary {i+1}")
            for key in extra_keys:
                str_errors.append(f"Key {key} is not expected in the dictionnary {i+1}")

    if str_errors:
        raise InstanceError(str_errors)


def check_int(solution):
    """
    Function checking that every field of every dictionnaries is a non-negative int
    :param solution: solution given by the candidate
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []

    for (i, task_dictionnary) in enumerate(solution):  # For each dictionnary
        for (
            key,
            value,
        ) in task_dictionnary.items():  # We check if each field is a non-negative int
            if type(value) is not int:
                str_errors.append(
                    f"Element {key} of your dictionnary {i+1} is not an int"
                )
            elif value < 0:
                str_errors.append(
                    f"Element {key} of your dictionnary {i+1} is negative"
                )

    if str_errors:
        raise InstanceError(str_errors)


def existing_elements(solution, instance):
    """
    Function checking if each machines, tasks and operators are defined in the instance
    :param solution: solution given by the candidate
    :param instance: instance addressed by the solution
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []

    for task_dictionnary in solution:
        for key, value in MATCHING.items():
            if not (1 <= task_dictionnary[key] <= instance[PARAMETERS][SIZE][value]):
                str_errors.append(
                    f"{key} {task_dictionnary[key]} isn't defined in the instance solution (id too high or equal to 0)"
                )

    if str_errors:
        raise InstanceError(str_errors)
