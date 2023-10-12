from constants import *
from errors import InstanceError

# We create those constants to handle sites_occupied, they might move later


def check_constraints(solution, instance):
    """
    Main function checking the validity of a given solution according to subject constraints
    The solution and the instance should have been converted before entering this functions, i.e.
    it should contains dictionnaries and not lists. This is done in order to manipulate them more easily
    without checking if the elements were in the good order.
    :return: Nothing if everything goes right, raises an Error if something goes wrong
    """
    all_tasks_present(solution, instance)
    tasks_performed_on_compatible_machine(solution, instance)
    tasks_performed_by_comptetent_operator(solution, instance)
    jobs_effectued_after_release_date(solution, instance)
    tasks_of_a_job_done_in_order(solution, instance)
    no_conflict_with_same_machine_or_operator(solution, instance)


def all_tasks_present(solution, instance):
    """
    Function checking if all tasks are present in the solution
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []
    for task_id in range(1, instance[PARAMETERS][SIZE][NB_TASKS]):
        if task_id not in solution.keys():
            str_errors.append(f"Task {task_id} isn't present in your solution")

    if str_errors:
        raise InstanceError(str_errors)


def tasks_performed_on_compatible_machine(solution, instance):
    """
    Function checking if all tasks are allocated to a machine capable of
    treating this task.
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []
    for task_id, task_dictionnary in solution.items():
        if (
            task_dictionnary[MACHINE]
            not in instance[TASKS][task_id][
                MACHINES
            ].keys()  # List of compatibles machines' ID
        ):
            str_errors.append(
                f"Task {task_id} can't be performed on machine {task_dictionnary[MACHINE]}."
            )

    if str_errors:
        raise InstanceError(str_errors)


def tasks_performed_by_comptetent_operator(solution, instance):
    """
    Function checking if all tasks are performed by an operator capable of
    treating this task.
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []
    for task_id, task_dictionnary in solution.items():
        machine_id = task_dictionnary[MACHINE]
        if (
            task_dictionnary[OPERATOR]
            not in instance[TASKS][task_id][MACHINES][machine_id][OPERATORS]
        ):
            str_errors.append(
                f"Operator {task_dictionnary[OPERATOR]} is incompetent to perform task {task_id} on {task_dictionnary[MACHINE]})."
            )

    if str_errors:
        raise InstanceError(str_errors)


def jobs_effectued_after_release_date(solution, instance):
    """
    This function checks that the first task of each jobs begins after the release date of job j.
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """
    str_errors = []

    for job_id, job_dictionnary in instance[JOBS].items():
        first_task_id = job_dictionnary[SEQUENCE][0]
        release_date = job_dictionnary[RELEASE_DATE]
        begin_of_first_task = solution[first_task_id][START]
        if begin_of_first_task < release_date:
            str_errors.append(
                f"Job {job_id} is started before its release date (check the start of task {first_task_id})"
            )

    if str_errors:
        raise InstanceError(str_errors)


def tasks_of_a_job_done_in_order(solution, instance):
    """
    Functions checking that within each job, the task are done in the good order, and each task is started
    after the previous one is finished
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []

    for job_id, job_dictionnary in instance[JOBS].items():
        task_sequence = job_dictionnary[SEQUENCE]
        # if len(sequence)==1, we don't have to check
        for i in range(1, len(task_sequence)):
            current_task_id = task_sequence[i]
            previous_task_id = task_sequence[i - 1]
            current_task_dictionnary = solution[current_task_id]
            previous_task_dictionnary = solution[previous_task_id]
            end_of_previous_task = (
                previous_task_dictionnary[START]
                + instance[TASKS][previous_task_id][PROCESSING_TIME]
            )  # (exists because i >= 1)
            if current_task_dictionnary[START] < end_of_previous_task:
                str_errors.append(
                    f"Task {current_task_id} is started before the end of task {previous_task_id} in job {job_id}"
                )

    if str_errors:
        raise InstanceError(str_errors)


def no_conflict_with_same_machine_or_operator(solution, instance):
    """
    Functions checking that two tasks aren't performed at the same time on the same machine or with the same operator.
    :param solution: solution given by the candidate (with dictionnaries for tasks)
    :param instance: instance addressed by the solution previously converted (with dictionnaries and not lists for jobs, machines and tasks)
    :return: raises InstanceError with details in case it spots an error
    """

    str_errors = []
    nb_tasks = len(solution)

    for task1_id in range(1, nb_tasks + 1):
        task1 = solution[task1_id]
        processing_time_task1 = instance[TASKS][task1_id][PROCESSING_TIME]
        for task2_id in range(task1_id + 1, nb_tasks + 1):
            task2 = solution[task2_id]
            processing_time_task2 = instance[TASKS][task2_id][PROCESSING_TIME]
            task1_end = task1[START] + processing_time_task1
            task2_end = task2[START] + processing_time_task2
            if task1[OPERATOR] == task2[OPERATOR] or task1[MACHINE] == task2[MACHINE]:
                if (
                    task1_end > task2[START] >= task1[START]
                    or task2_end > task1[START] >= task2[START]
                ):
                    str_errors.append(
                        f"Tasks {task1_id} and {task2_id} are performed simultaneously on the same machine or by the same operator"
                    )

    if str_errors:
        raise InstanceError(str_errors)
