import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv
from ensemble_experimentation.src.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.splitting_methods import split2
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point


def main_entry_point():
    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments
    ggv.arguments, ggv.cleaned_arguments = parse_args_main_entry_point()

    # Prepare the database to be splitted
    has_ben_backuped = preprocessing(ggv.cleaned_arguments)
    if has_ben_backuped:
        input_path = ggv.cleaned_arguments[gpn.modified_database_name()]
    else:
        input_path = ggv.cleaned_arguments[gpn.database()]

    print(ggv.arguments)
    print(ggv.cleaned_arguments)
    print(ggv.statistics)

    split2(filepath=input_path,
           delimiter=ggv.cleaned_arguments[gpn.delimiter()],
           row_limit=ggv.cleaned_arguments[gpn.training_value()],
           have_header=ggv.cleaned_arguments[gpn.have_header()],
           method=ggv.cleaned_arguments[gpn.initial_split_method()],
           output_name_train=ggv.cleaned_arguments[gpn.initial_split_train_name()],
           output_name_test=ggv.cleaned_arguments[gpn.initial_split_test_name()],
           encoding=ggv.cleaned_arguments[gpn.encoding()],
           class_name=ggv.cleaned_arguments[gpn.class_name()],
           number_of_rows=ggv.cleaned_arguments[ggv.number_of_rows()])


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
