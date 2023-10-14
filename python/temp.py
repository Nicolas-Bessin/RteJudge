from loader import load_json, save_json
from remove_spaces import clean_keys
from solution_format_checker import solution_checker

size = "tiny"

file_input = f"instances/input/{size}.json"
file_input_conv = f"instances/input/{size}_conv1.json"
file_output = f"instances/output/{size}_sol.json"
file_output_conv = f"instances/output/{size}_sol_conv1.json"

if __name__ == "__main__":
    raw_instance = load_json(file_input)
    raw_solution = load_json(file_output)
    solution = clean_keys(raw_solution)
    instance = clean_keys(raw_instance)
    solution_checker(instance, solution)