""" Split the subtrain database into multiple subsubtrain databases.
Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
module.
"""
from typing import List

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.splitting_methods.split import split
from ensemble_experimentation.src.vrac.file_system import create_dir
from ensemble_experimentation.src.vrac.iterators import subsubtrain_dir_path


def subsubtrain_split() -> None:
    """ Split the subtrain database into multiple subsubtrain databases.
    Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
    module.
    """
    # Create the subsubtrain directories
    subsubtrain_names = _create_subtrain_directories(env.trees_in_forest)

    # Split the database
    row_limit = env.instances_subtrain_database // env.trees_in_forest
    list_instances = \
        split(input_path=env.statistics[gsn.subtrain_path()],
              delimiter=env.cleaned_arguments[gpn.delimiter()],
              have_header=env.cleaned_arguments[gpn.have_header()],
              method=env.cleaned_arguments[gpn.subsubtrain_split_method()],
              encoding=env.cleaned_arguments[gpn.encoding()],
              class_name=env.cleaned_arguments[gpn.class_name()],
              number_of_rows=env.statistics[gsn.instances_in_subtrain()],
              tree_names=subsubtrain_names,
              subtrain_path=env.cleaned_arguments[gpn.main_directory()] + "/" + env.cleaned_arguments[gpn.subtrain_directory()],
              row_limit=row_limit)

    # Store the number of instances of each tree along with its name in the `env` module
    env.instances_subsubtrain_databases = dict(zip(subsubtrain_names, list_instances))


def _create_subtrain_directories(number_of_trees: int) -> List[str]:
    """ Create all needed directories which will each serves as a workplace for a single tree.
    Return all the names of the directories created.
    """
    subsubtrain_names = []
    for dir_name in subsubtrain_dir_path(number_of_trees, env.cleaned_arguments[gpn.main_directory()],
                                         env.cleaned_arguments[gpn.subtrain_directory()],
                                         env.cleaned_arguments[gpn.subsubtrain_directory_pattern()]):
        subsubtrain_names.append(dir_name)
        create_dir(dir_name)
    return subsubtrain_names
