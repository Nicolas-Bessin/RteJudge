import json


def load_json(file_path):
    """
    Load file at FILE_PATH into a dict by assuming it's format is JSON.
    Throw FileNotFoundError if file doesn't exist.
    Throw json.decoder.JSONDecodeError if file isn't valid JSON.
    :param file_path: The path to file we want to load.
    :return loaded_dict: A dict with file's data.
    """

    with open(file_path, "r") as file:
        return json.load(file)


def save_json(object, file_path):
    output_json = json.dumps(object, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(output_json)
