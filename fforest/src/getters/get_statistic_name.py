""" This module defines functions to easily access values stored in the file `statistics_names.json`, located in the
`res` folder at the root of the program's package.
This file contains the name of the keys used by the environment dictionary containing all statistics related to the
program.

It follows the following strict guidelines:
- Any value stored in the file must have its own access function.
- All access functions must have the same name as its respective key in the file. The only exception is a key is named
after a built-in function or variable. In this case, the programmer is free to prepend a word to its access function
name.
- Except for the access functions, this module mustn't have any side-effect to the program's namespace nor the files it
tries to access.
"""
import json
import os


_PATH_STATISTICS_NAMES = "../../res/statistics_names.json"


def _get_stat_from_file(value):
    global _PATH_STATISTICS_NAMES

    path = os.path.join(os.path.dirname(__file__),
                        _PATH_STATISTICS_NAMES)
    with open(path) as file:
        return json.load(file)[value]


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


def instances_in_subsubtrain() -> str:
    return _get_stat_from_file("instances_in_subsubtrain")


if __name__ == '__main__':
    pass
