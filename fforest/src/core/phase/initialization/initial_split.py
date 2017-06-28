""" Split the initial database into the train and test databases.
Store the number of instances of the original, train and test databases into the `instances_original_database`,
`instances_train_database` and `instances_test_database` variables in the `env` module.
"""
import fforest.src.getters.environment as env
from fforest.src.core.splitting_methods.split import split2
from fforest.src.file_tools.csv_tools import get_number_of_rows
from fforest.src.vrac.maths import convert_row_limit


def initial_split() -> None:
    """ Split the initial database into the train and test databases.
    Store the number of instances of the original, train and test databases into the `instances_original_database`,
    `instances_train_database` and `instances_test_database` variables in the `env` module.
    """
    # Count instances in initial database to convert the training value into a number of instances to give to the train
    # database.
    env.original_database_instances = get_number_of_rows(env.preprocessed_database_path)
    env.training_value = convert_row_limit(env.training_value, env.original_database_instances)

    env.train_database_instances, env.test_database_instances = \
        split2(input_path=env.preprocessed_database_path,
               delimiter=env.delimiter_output,
               row_limit=env.training_value,
               method=env.initial_split_method,
               output_name_train=env.train_database_path,
               output_name_test=env.test_database_path,
               encoding=env.encoding_output,
               class_name=env.class_name,
               number_of_rows=env.original_database_instances,
               quoting=env.quoting_output,
               quote_char=env.quote_character_output,
               line_delimiter=env.line_delimiter_output)
