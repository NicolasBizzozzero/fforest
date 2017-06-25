import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.splitting_methods.split import split2
from ensemble_experimentation.src.file_tools.csv_tools import get_number_of_rows
from ensemble_experimentation.src.vrac.maths import convert_row_limit


def initial_split() -> None:
    """ Split the initial database into the train and test databases.
    Store the number of instances of the train and test databases into the `statistics` dictionary in the `env`
    module.
    """
    # Count instances in initial database
    env.instances_original_database = get_number_of_rows(env.preprocessed_database_path)
    env.training_value = convert_row_limit(env.training_value, env.instances_original_database)

    env.instances_train_database, env.instances_test_database = \
        split2(input_path=env.preprocessed_database_path,
               delimiter=env.delimiter_output,
               row_limit=env.training_value,
               have_header=env.have_header,
               method=env.initial_split_method,
               output_name_train=env.train_database_path,
               output_name_test=env.test_database_path,
               encoding=env.encoding_output,
               class_name=env.class_name,
               number_of_rows=env.instances_original_database)
