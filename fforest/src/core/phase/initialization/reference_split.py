""" Split the train database into the subtrain and reference databases.
Store the number of instances of the reference and subtrain databases into the `instances_reference_database` and
`instances_subtrain_database` variables in the `env` module.
"""
import fforest.src.getters.environment as env
from fforest.src.core.splitting_methods.split import split2
from fforest.src.vrac.file_system import create_dir
from fforest.src.vrac.maths import convert_row_limit


def reference_split():
    """ Split the train database into the subtrain and reference databases.
    Store the number of instances of the reference and subtrain databases into the `instances_reference_database` and
    `instances_subtrain_database` variables in the `env` module.
    """
    create_dir(env.subtrain_directory_path)

    _calculate_row_limit(reference_value=env.reference_value, instances_in_train_database=env.train_database_instances)

    # Split the database
    env.reference_database_instances, env.subtrain_database_instances = \
        split2(input_path=env.train_database_path,
               row_limit=env.reference_value,
               method=env.reference_split_method,
               output_name_train=env.reference_database_path,
               output_name_test=env.subtrain_database_path,
               class_name=env.class_name,
               number_of_rows=env.train_database_instances,
               dialect=env.dialect_output)


def _create_subtrain_directory(main_directory: str, subtrain_directory: str):
    """ Construct the path to the subtrain directory then create it. """
    create_dir("{}/{}".format(main_directory, subtrain_directory))


def _calculate_row_limit(reference_value: str, instances_in_train_database: int):
    """ Convert the reference value into a number of instances to give to the reference database. """
    env.reference_value = convert_row_limit(reference_value, instances_in_train_database)
