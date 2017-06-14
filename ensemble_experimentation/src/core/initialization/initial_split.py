import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.splitting_methods.split import split2


def initial_split():
    """ Split the initial database into the train and test databases.
    Store the number of instances of the train and test databases into the `statistics` dictionary into the `env`
    module.
    """
    env.statistics[gsn.instances_in_train()], \
        env.statistics[gsn.instances_in_test()] = \
        split2(filepath=env.initial_split_input_path,
               delimiter=env.cleaned_arguments[gpn.delimiter()],
               row_limit=env.cleaned_arguments[gpn.training_value()],
               have_header=env.cleaned_arguments[gpn.have_header()],
               method=env.cleaned_arguments[gpn.initial_split_method()],
               output_name_train=env.statistics[gsn.train_path()],
               output_name_test=env.statistics[gsn.test_path()],
               encoding=env.cleaned_arguments[gpn.encoding()],
               class_name=env.cleaned_arguments[gpn.class_name()],
               number_of_rows=env.statistics[gsn.instances_in_database()])