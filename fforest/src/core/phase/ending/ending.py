import traceback
from typing import Callable

import fforest.src.getters.environment as env
import fforest.src.getters.get_statistic_name as gsn
from fforest.src.file_tools.dialect import Dialect
from fforest.src.vrac.file_system import dump_dict


def dump_statistics_dictionary():
    # Dump instances dictionary
    instances_dictionary = {
        gsn.instances_in_database(): env.original_database_instances,
        gsn.instances_in_train(): env.train_database_instances,
        gsn.instances_in_test(): env.test_database_instances,
        gsn.instances_in_reference(): env.reference_database_instances,
        gsn.instances_in_subtrain(): env.subtrain_database_instances,
        gsn.instances_in_subsubtrain(): env.subsubtrain_databases_instances
    }

    if not env.statistics_file_path:
        filepath = "."
    else:
        filepath = env.statistics_file_path
    dump_dict(instances_dictionary, filepath, dialect=Dialect())


def _function_post_failure():
    """ This function is called if an exception is raised inside a failure_safe code. """
    dump_statistics_dictionary()


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
