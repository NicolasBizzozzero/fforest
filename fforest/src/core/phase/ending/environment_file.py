import enum
import os
from typing import List, Dict
import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.entropy_measures import EntropyMeasure
from fforest.src.core.phase.performance_evaluation.quality_computing_method.quality_computing_method import \
    str_to_qualitycomputingmethod, QualityComputingMethod
from fforest.src.core.phase.phase import str_to_phase, Phase
from fforest.src.core.splitting_methods.split import str_to_splittingmethod, SplittingMethod
from fforest.src.file_tools.dialect import Dialect
from fforest.src.file_tools.format import string_to_format, Format
from fforest.src.getters.get_output_message import string_to_verbosity, Verbosity
from fforest.src.vrac.file_system import dump_dict, load_dict


ENVIRONMENT_FILE_NAME = "environment.json"


def dump_environment_file(directory: str = ".") -> None:
    content = _module_to_dict()
    _serialize_custom_classes(content)
    dump_dict(d=content, path=os.path.join(directory, ENVIRONMENT_FILE_NAME))


def load_environment_file(path: str = ENVIRONMENT_FILE_NAME) -> None:
    content = load_dict(path)
    _deserialize_custom_classes(content)
    _deserialize_enums(content)
    _dict_to_module(content)


def _get_all_environment_variables() -> List[str]:
    return [variable for variable in dir(env) if not variable.startswith("__")]


def _module_to_dict() -> Dict:
    file = {}
    for variable in _get_all_environment_variables():
        value = getattr(env, variable)
        if issubclass(enum.Enum, type(value)):
            value = value.value
        file[variable] = value
    return file


def _dict_to_module(d: dict) -> None:
    for key, value in d.items():
        setattr(env, key, value)


def _serialize_custom_classes(content: dict) -> None:
    for key, value in content.items():
        if key in ("dialect_input", "dialect_output"):
            content[key] = value.__dict__


def _deserialize_custom_classes(content: dict) -> None:
    for key, value in content.items():
        if key in ("dialect_input", "dialect_output"):
            content[key] = Dialect(**value)


def _deserialize_enums(content: dict) -> None:
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
