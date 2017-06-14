import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.initialization.arg_cleaner import convert_row_limit
from ensemble_experimentation.src.core.splitting_methods.split import split2
from ensemble_experimentation.src.vrac import create_dir


def _create_subtrain_directory():
    create_dir("{}/{}".format(env.cleaned_arguments[gpn.main_directory()],
                              env.cleaned_arguments[gpn.subtrain_directory()]))


def _calculate_row_limit():
    env.cleaned_arguments[gpn.reference_value()] = convert_row_limit(env.cleaned_arguments[gpn.reference_value()],
                                                                     env.statistics[gsn.instances_in_train()])


def reference_split():
    """ Split the train database into the subtrain and reference databases.
    Store the number of instances of the `subtrain` and `reference` databases into the `statistics` dictionary, inside
    the `env` module.
    """
    _create_subtrain_directory()

    _calculate_row_limit()

    # Split the database
    env.statistics[gsn.instances_in_reference()], \
        env.statistics[gsn.instances_in_subtrain()] = \
        split2(input_path=env.statistics[gsn.train_path()],
               delimiter=env.cleaned_arguments[gpn.delimiter()],
               row_limit=env.cleaned_arguments[gpn.reference_value()],
               have_header=env.cleaned_arguments[gpn.have_header()],
               method=env.cleaned_arguments[gpn.reference_split_method()],
               output_name_train=env.statistics[gsn.reference_path()],
               output_name_test=env.statistics[gsn.subtrain_path()],
               encoding=env.cleaned_arguments[gpn.encoding()],
               class_name=env.cleaned_arguments[gpn.class_name()],
               number_of_rows=env.statistics[gsn.instances_in_train()])