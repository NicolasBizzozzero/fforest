from typing import List, Dict
import fforest.src.getters.environment as env
from fforest.src.file_tools.dialect import Dialect
from fforest.src.vrac.file_system import dump_dict

_ENVIRONMENT_FILE_NAME = "environment.json"


def _get_all_environment_variables() -> List[str]:
    return [variable for variable in dir(env) if not variable.startswith("__")]


def _load_environment_file() -> Dict:
    return {variable: getattr(env, variable) for variable in _get_all_environment_variables()}


def dump_environment_file(path: str = _ENVIRONMENT_FILE_NAME) -> None:
    content = _load_environment_file()
    dump_dict(d=content, path=path, dialect=Dialect())
