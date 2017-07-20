"""

"""
import traceback
from typing import Callable

from fforest.src.core.phase.ending.environment_file import dump_environment_file
import fforest.src.getters.environment as env
from fforest.src.core.phase.ending.exit_code import EXIT_SUCCESS


_PARSING_FUNCTIONS_PREFIX = "parse_args_"


def ending() -> None:
    # Makes sure that the environment file is dumped somewhere, even if the `main_directory_path` variable hasn't been
    # initialized inside the `environment` module.
    if env.main_directory_path:
        dump_environment_file(env.main_directory_path)
    else:
        dump_environment_file()
    exit(EXIT_SUCCESS)


def _function_post_failure(entry_point_name: str):
    """ This function is called if an exception is raised inside a failure_safe code. """
    global _PARSING_FUNCTIONS_PREFIX

    try:
        # In case the entry point has been wrongly called before the parsing phase
        import fforest.src.core.phase.preprocessing.args_parser as parsing_module
        parsing_function_name = "{}{}".format(_PARSING_FUNCTIONS_PREFIX, entry_point_name)
        parsing_function = getattr(parsing_module, parsing_function_name)
        parsing_function()
    except Exception:
        dump_environment_file()


def failure_safe(func: Callable) -> Callable:
    """ This decorator wrap a function with a 'try, except' catching all exceptions throws inside.
    If an exception is raised, the method `_function_post_failure` is called.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            _function_post_failure(entry_point_name=func.__name__)
            # traceback.print_exc()
    return wrapper
