import json
import os


_FILEPATH_PARAMS_NAMES = "../../res/parameters_names.json"


def _get_name_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_PARAMS_NAMES)
    with open(filepath) as file:
        return json.load(file)[value]


def identificator() -> str:
    return _get_name_from_file("identificator")


def encoding() -> str:
    return _get_name_from_file("encoding")


def training_value() -> str:
    return _get_name_from_file("training_value")


def trees_in_forest() -> str:
    return _get_name_from_file("trees_in_forest")


def format_db() -> str:
    return _get_name_from_file("format_db")


def reference_value() -> str:
    return _get_name_from_file("reference_value")


def delimiter() -> str:
    return _get_name_from_file("delimiter")


def have_header() -> str:
    return _get_name_from_file("have_header")


def database() -> str:
    return _get_name_from_file("database")


def initial_split_train_name() -> str:
    return _get_name_from_file("initial_split_train_name")


def initial_split_test_name() -> str:
    return _get_name_from_file("initial_split_test_name")


def initial_split_method() -> str:
    return _get_name_from_file("initial_split_method")


if __name__ == '__main__':
    pass
