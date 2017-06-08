import json
import os


_FILEPATH_DEFAULT_VALUES = "../../res/default_values.json"


def _get_value_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_DEFAULT_VALUES)
    with open(filepath) as file:
        return json.load(file)[value]


def id() -> str:
    return _get_value_from_file("identificator")


def encoding() -> str:
    return _get_value_from_file("encoding")


def training_values() -> float:
    return _get_value_from_file("training_values")


def format_db() -> str:
    return _get_value_from_file("format")


def reference_values() -> float:
    return _get_value_from_file("reference_values")


def delimiter() -> str:
    return _get_value_from_file("delimiter")


def keep_header() -> int:
    return _get_value_from_file("keep_header")


if __name__ == '__main__':
    pass
