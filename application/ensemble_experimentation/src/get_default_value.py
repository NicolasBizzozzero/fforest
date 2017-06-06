import json
import os


_FILEPATH_DEFAULT_VALUES = "../res/default_values.json"
_FILEPATH_PARAMS_NAMES = "../res/parameters_names.json"


def _get_value_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_DEFAULT_VALUES)
    with open(filepath) as file:
        return json.load(file)[value]


def id() -> str:
    return _get_value_from_file("identificator")


def pourcentage_train() -> float:
    return _get_value_from_file("%train")


if __name__ == '__main__':
    pass
