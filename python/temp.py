from loader import load_json, save_json
from remove_spaces import clean_keys
from solution_format_checker import solution_checker
from converter import convert_instance, convert_solution

size = "tiny"

file_input = f"instances/input/{size}.json"
file_input_conv = f"instances/input/{size}_conv1.json"
file_output = f"instances/output/{size}_sol.json"
file_output_conv = f"instances/output/{size}_sol_conv1.json"

if __name__ == "__main__":
    data_instance = load_json(file_input)
    data_solution = load_json(file_output)
    raw_solution = clean_keys(data_solution)
    raw_instance = clean_keys(data_instance)
    solution_checker(raw_instance, raw_solution)
    solution = convert_solution(raw_solution)
    instance = convert_instance(raw_instance)
