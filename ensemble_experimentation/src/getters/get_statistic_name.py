import json
import os


_FILEPATH_DEFAULT_VALUES = "../../res/statistics_names.json"


def _get_stat_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_DEFAULT_VALUES)
    with open(filepath) as file:
        return json.load(file)[value]


def database_path() -> str:
    return _get_stat_from_file()["database_path"]


def database_name() -> str:
    return _get_stat_from_file()["database_name"]


def modified_database() -> str:
    return _get_stat_from_file()["modified_database"]


def train() -> str:
    return _get_stat_from_file()["train"]


def test() -> str:
    return _get_stat_from_file()["test"]


def instances_in_database() -> str:
    return _get_stat_from_file()["instances_in_database"]


def instances_in_train() -> str:
    return _get_stat_from_file()["instances_in_train"]


def instances_in_test() -> str:
    return _get_stat_from_file()["instances_in_test"]


def instances_in_reference() -> str:
    return _get_stat_from_file()["instances_in_reference"]


def instances_in_subtrain() -> str:
    return _get_stat_from_file()["instances_in_subtrain"]


if __name__ == '__main__':
    pass
