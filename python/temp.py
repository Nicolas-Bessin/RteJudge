from loader import load_json, save_json
from remove_spaces import clean_keys
from solution_format_checker import solution_checker
from converter import convert_instance, convert_solution
from cost import cost, construction_cost, operational_cost
from errors import InstanceError

size = "tiny3"

names = ["small", "medium", "large"]

if __name__ == "__main__":
    for size in names:
        print(size)
        file_input = f"instances/input/{size}.json"
        file_output = f"instances/output/{size}_sol.json"
        data_instance = load_json(file_input)
        data_solution = load_json(file_output)
        save_json(data_solution, file_output)
        save_json(data_instance, file_input)
        raw_solution = clean_keys(data_solution)
        raw_instance = clean_keys(data_instance)
        solution_checker(raw_instance, raw_solution)
        solution = convert_solution(raw_solution)
        instance = convert_instance(raw_instance)
        try:
            print(
                f"Construction cost for {size} : {construction_cost(instance, solution)}"
            )
            print(
                f"Operationnal cost for {size} : {operational_cost(instance, solution)}"
            )
        except InstanceError as e:
            print(e._errors_list)
            print(size)
