import json
import os


_FILEPATH_STATISTICS_NAMES = "../../res/statistics_names.json"


def _get_stat_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_STATISTICS_NAMES)
    with open(filepath) as file:
        return json.load(file)[value]


def output_dict(d: dict, path: str):
    with open(path, 'w') as file:
        return json.dump(d, file, indent=4, sort_keys=True)


def database_path() -> str:
    return _get_stat_from_file("database_path")


def database_name() -> str:
    return _get_stat_from_file("database_name")


def modified_database_path() -> str:
    return _get_stat_from_file("modified_database_path")


def train_path() -> str:
    return _get_stat_from_file("train_path")


def test_path() -> str:
    return _get_stat_from_file("test_path")


def instances_in_database() -> str:
    return _get_stat_from_file("instances_in_database")


def instances_in_train() -> str:
    return _get_stat_from_file("instances_in_train")


def instances_in_test() -> str:
    return _get_stat_from_file("instances_in_test")


def instances_in_reference() -> str:
    return _get_stat_from_file("instances_in_reference")


def instances_in_subtrain() -> str:
    return _get_stat_from_file("instances_in_subtrain")


if __name__ == '__main__':
    pass
