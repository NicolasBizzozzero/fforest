""" Split the train database into the subtrain and reference databases.
Store the number of instances of the `subtrain` and `reference` databases into the `statistics` dictionary, inside
the `env` module.
"""
import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.splitting_methods.split import split2
from ensemble_experimentation.src.vrac.file_system import create_dir
from ensemble_experimentation.src.vrac.maths import convert_row_limit


def reference_split():
    """ Split the train database into the subtrain and reference databases.
    Store the number of instances of the `subtrain` and `reference` databases into the `statistics` dictionary, inside
    the `env` module.
    """
    _create_subtrain_directory(main_directory=env.main_directory,
                               subtrain_directory=env.subtrain_directory)

    _calculate_row_limit(reference_value=env.reference_value, instances_in_train_database=env.instances_train_database)

    # Split the database
    env.instances_reference_database, env.instances_subtrain_database = \
        split2(input_path=env.train_database_path,
               delimiter=env.delimiter_output,
               row_limit=env.reference_value,
               method=env.reference_split_method,
               output_name_train=env.reference_database_path,
               output_name_test=env.subtrain_database_path,
               encoding=env.encoding_output,
               class_name=env.class_name,
               number_of_rows=env.instances_train_database,
               quoting=env.quoting_output,
               quote_char=env.quote_character_output)


def _create_subtrain_directory(main_directory: str, subtrain_directory: str):
    """ Construct the path to the subtrain directory then create it. """
    create_dir("{}/{}".format(main_directory, subtrain_directory))


def _calculate_row_limit(reference_value: str, instances_in_train_database: int):
    """ Convert the reference value into a number of instances to give to the reference database. """
    env.reference_value = convert_row_limit(reference_value, instances_in_train_database)
