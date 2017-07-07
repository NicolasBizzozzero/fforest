import traceback
from typing import Callable

from fforest.src.core.phase.ending.environment_file import dump_environment_file


def ending() -> None:
    dump_environment_file()


def _function_post_failure():
    """ This function is called if an exception is raised inside a failure_safe code. """
    dump_environment_file()


def failure_safe(func: Callable) -> Callable:
    """ This decorator wrap a function with a 'try, except' catching all exceptions throws inside.
    If an exception is raised, the method `_function_post_failure` is called.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            _function_post_failure()
            traceback.print_exc()
    return wrapper
