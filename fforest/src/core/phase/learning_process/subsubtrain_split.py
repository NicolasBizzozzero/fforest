""" Split the subtrain database into multiple subsubtrain databases.
Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
module.
"""
from typing import List

import fforest.src.getters.environment as env
from fforest.src.core.splitting_methods.split import split
from fforest.src.vrac.file_system import create_dir


def subsubtrain_split() -> None:
    """ Split the subtrain database into multiple subsubtrain databases.
    Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
    module.
    """
    # Create the subsubtrain directories
    _create_subsubtrain_directories(env.subsubtrain_directories_path)

    # Split the database
    row_limit = env.subtrain_database_instances // env.trees_in_forest
    list_instances = \
        split(input_path=env.subtrain_database_path,
              row_limit=row_limit,
              method=env.subsubtrain_split_method,
              class_name=env.class_name,
              number_of_rows=env.subtrain_database_instances,
              output_pathes=env.subsubtrain_databases_paths,
              dialect=env.dialect)

    # Store the number of instances of each tree along with its name in the `env` module
    env.subsubtrain_databases_instances = dict(zip(env.subsubtrain_directories_path, list_instances))


def _create_subsubtrain_directories(subsubtrain_directories: List[str]) -> None:
    """ Create all needed directories which will each serves as a workplace for a single tree. """
    for dir_name in subsubtrain_directories:
        create_dir(dir_name)
