import json
import os


_FILEPATH_DEFAULT_VALUES = "../../res/default_values.json"


def _get_value_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_DEFAULT_VALUES)
    with open(filepath) as file:
        return json.load(file)[value]


def identificator() -> str:
    return _get_value_from_file("identificator")


def encoding() -> str:
    return _get_value_from_file("encoding")


def training_value() -> float:
    return _get_value_from_file("training_value")


def format_db() -> str:
    return _get_value_from_file("format")


def reference_value() -> float:
    return _get_value_from_file("reference_value")


def delimiter() -> str:
    return _get_value_from_file("delimiter")


def have_header() -> int:
    return _get_value_from_file("have_header")


def initial_split_train_name() -> str:
    return _get_value_from_file("initial_split_train_name")


def initial_split_test_name() -> str:
    return _get_value_from_file("initial_split_test_name")


def initial_split_method() -> str:
    return _get_value_from_file("initial_split_method")


def statistics_file_name() -> str:
    return _get_value_from_file("statistics_file_name")


if __name__ == '__main__':
    pass
