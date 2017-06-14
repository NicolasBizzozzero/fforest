import traceback
from typing import Callable

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.vrac import dump_dict


def dump_statistics_dictionary():
    dump_dict(env.statistics, env.cleaned_arguments[gpn.main_directory()] + "/" + \
              env.cleaned_arguments[gpn.statistics_file_name()])


def function_post_failure():
    """ This function is called after en exception which happened inside a failure_safe code. """
    dump_statistics_dictionary()


def failure_safe(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            function_post_failure()
            traceback.print_exc()
    return wrapper
