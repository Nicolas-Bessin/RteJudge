from constants import *
from errors import InstanceError


def solution_converter(solution):
    """Function that transforms the lists in the solution dictionnary into dictionnaries
    indexed by the ids of the objects in order to have access to the right task more easily.
    """
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


def converter(dic):
    """Converts every list in the input / ouptut dictionnaries into a dictionnary,
    with the keys being the ids (We have list[i]["id"] = i+1 in 2023's instances,
    so that we don't have to take into account the fact that the ids begin at 1
    and list indices at 0."""
    converted = {}
    for key in dic.keys():
        data = dic[key]
        if type(data) == list:
            new_dic = {id: data[id - 1] for id in range(1, len(data) + 1)}
            converted[key] = new_dic
        else:
            converted[key] = data
    return converted


if __name__ == "__main__":
    import os
    import loader

    size = "tiny"
    curr_path = os.path.dirname(__file__)
    file_in = curr_path + f"/../instances/input/{size}.json"
    file_out = curr_path + f"/../instances/output/{size}_sol.json"
    print(converter(loader.load_json(file_in)))
