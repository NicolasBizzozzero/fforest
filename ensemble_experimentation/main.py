import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
import ensemble_experimentation.src.vrac
from ensemble_experimentation.src.core.initialization.arg_parser import parse_args_main_entry_point, _convert_row_limit
from ensemble_experimentation.src.core.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.core.splitting_methods import split2


def main_entry_point():
    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments.
    # After calling this method, the parsed arguments and the cleaned arguments will be stored as dictionaries into the
    # `environment` module.
    parse_args_main_entry_point()

    # Preprocessing of the database
    preprocessing(env.cleaned_arguments)

    # Split the initial database into the train and test database
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

    # Split the train database into the reference database and the subtrain database
    # Create the subtrain directory
    ensemble_experimentation.src.vrac.create_dir(env.cleaned_arguments[gpn.main_directory()] + "/" +
                                                 env.cleaned_arguments[gpn.subtrain_directory()])

    # Calculate the row_limit
    env.cleaned_arguments[gpn.reference_value()] = _convert_row_limit(env.cleaned_arguments[gpn.reference_value()],
                                                                      env.statistics[gsn.instances_in_train()])

    print(env.cleaned_arguments)
    env.statistics[gsn.instances_in_reference()], \
        env.statistics[gsn.instances_in_subtrain()] = \
        split2(filepath=env.statistics[gsn.train_path()],
               delimiter=env.cleaned_arguments[gpn.delimiter()],
               row_limit=env.cleaned_arguments[gpn.reference_value()],
               have_header=env.cleaned_arguments[gpn.have_header()],
               method=env.cleaned_arguments[gpn.reference_split_method()],
               output_name_train=env.statistics[gsn.reference_path()],
               output_name_test=env.statistics[gsn.subtrain_path()],
               encoding=env.cleaned_arguments[gpn.encoding()],
               class_name=env.cleaned_arguments[gpn.class_name()],
               number_of_rows=env.statistics[gsn.instances_in_train()])

    # Split the subtrain database into multiple subsubtrain databases
    # Create the subsubtrain directories
    for tree_index in range(1, env.cleaned_arguments[gpn.trees_in_forest()] + 1):
        ensemble_experimentation.src.vrac.create_dir(env.cleaned_arguments[gpn.main_directory()] + "/" +
                                                     env.cleaned_arguments[gpn.subtrain_directory()] + "/" +
                                                     (env.cleaned_arguments[gpn.subsubtrain_directory_pattern()] % str(tree_index).zfill(4)))

    # Dump the statistics dictionary
    ensemble_experimentation.src.vrac.dump_dict(env.statistics, env.cleaned_arguments[gpn.main_directory()] + "/" + \
                                                env.cleaned_arguments[gpn.statistics_file_name()])


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
