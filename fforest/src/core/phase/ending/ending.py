""" This module takes care of the termination of the software. It must dump the environment file (whose content is
detailed inside the `environment_file` module) by any means at the end of the process. In other words, it should handle
a usual termination without any error, but also specific cases in which the software miserably fail at its task.
Thus the `ending` method should be called manually as the last phase, like all the others, and the `failure_safe`
decorator should be wrapping all entry points, intercepting every exceptions occurring during the execution and call as
a last resort the `_function_post_failure` method.
"""
import traceback
from typing import Callable

from fforest.src.core.phase.ending.environment_file import dump_environment_file
import fforest.src.getters.environment as env
from fforest.src.core.phase.ending.exit_code import EXIT_SUCCESS, EXIT_FAILURE, EXIT_CRITICAL_FAILURE


_PARSING_FUNCTIONS_PREFIX = "parse_args_"


def ending() -> None:
    # Makes sure that the environment file is dumped somewhere, even if the `main_directory_path` variable hasn't been
    # initialized inside the `environment` module.
    if env.main_directory_path:
        dump_environment_file(env.main_directory_path)
    else:
        dump_environment_file()

    exit(EXIT_SUCCESS)


def failure_safe(func: Callable) -> Callable:
    """ This decorator wrap a function with a 'try, except' catching all exceptions thrown inside.
    If an exception is raised, the method `_function_post_failure` is called.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            _function_post_failure(entry_point_name=func.__name__)
            traceback.print_exc()
    return wrapper


def _function_post_failure(entry_point_name: str):
    """ This function is called by the `failure_safe` decorator if an exception is raised during the execution of the
    code it's wrapping.
    """
    try:
        # In case the entry point has been wrongly called BEFORE the parsing phase
        parsing_function = _retrieve_parsing_function(entry_point_name)

        # Call the parsing function to, at least, let `docopt` print the usage of the corresponding entry point. If this
        # statement fails, then the exception is catch and the software ends in a 'critical failure' state.
        parsing_function()

        exit(EXIT_FAILURE)

    except Exception:

        # The software is not even capable of parsing the arguments entirely. It'll dump the environment file to make
        # the impression that he's doing something useful and to give him a false-sense of accomplishment. (the
        # environment file can also be used as a debugging tool, so that's cool I guess)
        dump_environment_file()
        exit(EXIT_CRITICAL_FAILURE)


def _retrieve_parsing_function(entry_point_name: str) -> Callable:
    """ Try to retrieve the parsing function located inside the `args_parser` module with its entry point name. It can
    be done because each entry point has its own parsing function, and each parsing function is named in the following
    format :
        _PARSING_FUNCTIONS_PREFIX + entry_point_name
    """
    global _PARSING_FUNCTIONS_PREFIX

    import fforest.src.core.phase.preprocessing.args_parser as parsing_module
    parsing_function_name = "{}{}".format(_PARSING_FUNCTIONS_PREFIX, entry_point_name)
    return getattr(parsing_module, parsing_function_name)
