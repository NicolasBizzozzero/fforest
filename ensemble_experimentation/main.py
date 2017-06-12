import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_statistic_name as gsn
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.vrac
from ensemble_experimentation.src.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.splitting_methods import split2
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point


def main_entry_point():
    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments + preprocessing
    ggv.arguments, ggv.cleaned_arguments = parse_args_main_entry_point()
    has_ben_backuped = preprocessing(ggv.cleaned_arguments)

    # Split the initial database into the train and test database
    if has_ben_backuped:
        input_path = ggv.cleaned_arguments[gpn.preprocessed_database_name()]
    else:
        input_path = ggv.cleaned_arguments[gpn.database()]
    ggv.statistics[gsn.instances_in_train()], \
    ggv.statistics[gsn.instances_in_test()] = \
        split2(filepath=input_path,
               delimiter=ggv.cleaned_arguments[gpn.delimiter()],
               row_limit=ggv.cleaned_arguments[gpn.training_value()],
               have_header=ggv.cleaned_arguments[gpn.have_header()],
               method=ggv.cleaned_arguments[gpn.initial_split_method()],
               output_name_train=ggv.cleaned_arguments[gpn.train_name()],
               output_name_test=ggv.cleaned_arguments[gpn.test_name()],
               encoding=ggv.cleaned_arguments[gpn.encoding()],
               class_name=ggv.cleaned_arguments[gpn.class_name()],
               number_of_rows=ggv.cleaned_arguments[ggv.number_of_rows()])

    # Split the train database into the reference database and the subtrain database
    ggv.statistics[gsn.instances_in_subtrain()], \
    ggv.statistics[gsn.instances_in_reference()] = \
        split2(filepath=gsn.train_path(),
               delimiter=ggv.cleaned_arguments[gpn.delimiter()],
               row_limit=1 - ggv.cleaned_arguments[gpn.reference_value()],
               have_header=ggv.cleaned_arguments[gpn.have_header()],
               method=ggv.cleaned_arguments[gpn.reference_split_method()],
               output_name_train=ggv.cleaned_arguments[gpn.reference_name()],
               output_name_test=ggv.cleaned_arguments[gpn.subtrain_name()],
               encoding=ggv.cleaned_arguments[gpn.encoding()],
               class_name=ggv.cleaned_arguments[gpn.class_name()],
               number_of_rows=ggv.statistics[gsn.instances_in_train()])

    # Dump the statistics dictionary
    ensemble_experimentation.src.vrac.dump_dict(ggv.statistics, ggv.cleaned_arguments[gpn.main_directory()] + "/" + gdv.statistics_file_name())


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
