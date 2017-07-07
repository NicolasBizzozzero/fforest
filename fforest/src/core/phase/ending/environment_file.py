import enum
from typing import List, Dict
import fforest.src.getters.environment as env
from fforest.src.file_tools.dialect import Dialect
from fforest.src.vrac.file_system import dump_dict, load_dict

_ENVIRONMENT_FILE_NAME = "environment.json"


def dump_environment_file(path: str = _ENVIRONMENT_FILE_NAME) -> None:
    content = _module_to_dict()
    _serialize_custom_classes(content)
    dump_dict(d=content, path=path)


def load_environment_file(path: str = _ENVIRONMENT_FILE_NAME) -> None:
    content = load_dict(path)


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


def _serialize_custom_classes(content: Dict) -> None:
    for key, value in content.items():
        if key in ("dialect_input", "dialect_output"):
            content[key] = value.__dict__
