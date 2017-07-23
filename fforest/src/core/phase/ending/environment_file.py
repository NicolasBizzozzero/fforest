""" This module contains utilities to load/save the environment file from/into the `environment` module. """
import enum
import os
from typing import List, Dict

import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.entropy_measures import EntropyMeasure
from fforest.src.core.phase.performance_evaluation.quality_computing_method.quality_computing_method import \
    QualityComputingMethod
from fforest.src.core.phase.phase import Phase
from fforest.src.core.splitting_methods.split import SplittingMethod
from fforest.src.file_tools.dialect import Dialect
from fforest.src.file_tools.format import Format
from fforest.src.getters.get_output_message import Verbosity
from fforest.src.vrac.file_system import dump_dict, load_dict

ENVIRONMENT_FILE_NAME = "environment.json"


def dump_environment_file(directory: str = ".", file_name: str = ENVIRONMENT_FILE_NAME) -> None:
    """ Dump the environment file at the specified directory. This method stores all user-created variables from the
    `environment` module in a dictionary, serialize some of its variables (enum converted to int or str, classes to
    multiple variables) then dump it.
    """
    content = _module_to_dict()
    _serialize_custom_classes(content)
    dump_dict(d=content, path=os.path.join(directory, file_name))


def load_environment_file(path: str = ENVIRONMENT_FILE_NAME) -> None:
    """ Load the environment file. This method retrieve the JSON file from the disk, convert it to a dictionary,
    deserialize some of its content (int or str converted to enums, multiples variables to classes) then load it inside
    the `environment` module.
    """
    content = load_dict(path)
    _deserialize_custom_classes(content)
    _deserialize_enums(content)
    _dict_to_module(content)


def _get_all_environment_variables() -> List[str]:
    """ Retrieve all variables user-created inside the `environment` module. This method ignores all variables
    automatically created by Python during the module's creation (eg: the variables starting with "__").
    """
    return [variable for variable in dir(env) if not variable.startswith("__")]


def _module_to_dict() -> Dict:
    """ Store all user-created variables from the `environment` module inside a dictionary, then return it. """
    file = {}
    for variable in _get_all_environment_variables():
        value = getattr(env, variable)

        # Serialize Enums to their corresponding value
        if issubclass(enum.Enum, type(value)):
            value = value.value

        file[variable] = value
    return file


def _dict_to_module(d: dict) -> None:
    """ Set all values contained inside `d` to the corresponding keys inside the `environment` module. """
    for key, value in d.items():
        setattr(env, key, value)


def _serialize_custom_classes(content: dict) -> None:
    """ Convert all custom classes contained in `content` into a dictionary of their variables. """
    for key, value in content.items():
        if key in ("dialect_input", "dialect_output"):
            content[key] = value.__dict__


def _deserialize_custom_classes(content: dict) -> None:
    """ Convert all dictionary of variables of a custom classes contained in `content` into the initial class. """
    for key, value in content.items():
        if key in ("dialect_input", "dialect_output"):
            content[key] = Dialect(**value)


def _deserialize_enums(content: dict) -> None:
    """ Convert int or str values contained in `content` and correspond to an Enum to the initial Enum. """
    for key, value in content.items():
        if key in ("current_phase", "last_phase"):
            content[key] = Phase(value)
        elif key == "entropy_measure":
            content[key] = EntropyMeasure(value)
        elif key in ("format_input", "format_output"):
            content[key] = Format(value)
        elif key in ("initial_split_method", "reference_split_method", "subsubtrain_split_method"):
            content[key] = SplittingMethod(value)
        elif key == "quality_computing_method":
            content[key] = QualityComputingMethod(value)
        elif key == "verbosity":
            content[key] = Verbosity(value)
