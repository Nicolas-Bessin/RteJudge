from json import decoder
from converter import convert_instance, convert_solution
from loader import load_json
from solution_format_checker import solution_checker
from constraints import check_constraints
from cost import cost
from errors import InstanceError
import argparse


def parser(instance_path, solution_path):
    """
    Global function, does everything
    :param instance_path: file path to the instance
    :param solution_path: file path to the candidate's solution
    :return: errors if there are some, else score
    """

    try:
        # We import both files in variables
        raw_instance = load_json(instance_path)
        raw_solution = load_json(solution_path)

        # We check the validity of the solution's format
        solution_checker(raw_instance, raw_solution)

        # we convert the instance and the solution in order to manipulate them more easily
        converted_instance = convert_instance(raw_instance)
        converted_solution = convert_solution(raw_solution)

        # We check whether the solution verifies all constraints
        check_constraints(converted_solution, converted_instance)

        # We calculate its cost
        return cost(converted_instance, converted_solution)

    except FileNotFoundError:
        return "Error: File not found, parsing aborted"

    except decoder.JSONDecodeError:
        return "Error: File is not a valid Json"

    except InstanceError as errors:
        message = "Error: instance is not valid, traceback list for information:\n"
        for i in errors.list:
            message += i
            message += "\n"
        return message


if __name__ == "__main__":
    # The ArgumentParser method allows to create an object that will parse what is typed in the command line
    python_parser = argparse.ArgumentParser(
        description="Check if a solution is a valid solution of the Rte "
        "KIRO Problem and give it a score."
    )
    python_parser.add_argument("-i", "--instance", dest="instance_path", default=None)
    python_parser.add_argument("-s", "--solution", dest="solution_path", default=None)

    args = python_parser.parse_args()

    solution_path = None
    instance_path = None

    if args.instance_path:
        instance_path = args.instance_path
    else:
        exit(1)

    if args.solution_path:
        solution_path = args.solution_path
    else:
        exit(1)

    result = parser(instance_path, solution_path)

    # We should return a score and a list of errors at the end, printing it until then.
    # json_result = json.dumps({"score": score, "errors": errors})
    # print(json_result)
    if type(result) is not str:
        print(result)
    else:
        # There have been problems. We therefore negate the score and print the problems
        print(-1)
        print(result)
