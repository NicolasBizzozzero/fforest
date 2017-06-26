""" Split the subtrain database into multiple subsubtrain databases.
Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
module.
"""
from typing import List

import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.splitting_methods.split import split
from ensemble_experimentation.src.vrac.file_system import create_dir
from ensemble_experimentation.src.vrac.iterators import subsubtrain_dir_path


def subsubtrain_split() -> None:
    """ Split the subtrain database into multiple subsubtrain databases.
    Store the number of instances of the databases into the `instances_subsubtrain_databases` variable in the `env`
    module.
    """
    # Create the subsubtrain directories
    subsubtrain_names = _create_subtrain_directories(number_of_trees=env.trees_in_forest,
                                                     main_directory=env.main_directory,
                                                     subtrain_directory=env.subtrain_directory,
                                                     subsubtrain_directory_pattern=env.subsubtrain_directory_pattern)

    # Split the database
    row_limit = env.instances_subtrain_database // env.trees_in_forest
    list_instances = \
        split(input_path=env.subtrain_database_path,
              delimiter=env.delimiter_output,
              row_limit=row_limit,
              method=env.subsubtrain_split_method,
              encoding=env.encoding_output,
              class_name=env.class_name,
              number_of_rows=env.instances_subtrain_database,
              tree_names=subsubtrain_names,
              quote_char=env.quote_character_output,
              quoting=env.quoting_output)

    # Store the number of instances of each tree along with its name in the `env` module
    env.instances_subsubtrain_databases = dict(zip(subsubtrain_names, list_instances))


def _create_subtrain_directories(number_of_trees: int, main_directory: str, subtrain_directory: str,
                                 subsubtrain_directory_pattern: str) -> List[str]:
    """ Create all needed directories which will each serves as a workplace for a single tree.
    Return all the names of the directories created.
    """
    subsubtrain_names = []
    for dir_name in subsubtrain_dir_path(number_of_trees, main_directory, subtrain_directory,
                                         subsubtrain_directory_pattern):
        subsubtrain_names.append(dir_name)
        create_dir(dir_name)
    return subsubtrain_names
