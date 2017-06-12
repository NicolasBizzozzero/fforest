import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv
from ensemble_experimentation.src.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.splitting_methods import split2
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point


# Contains every parsed arguments without any modification
arguments = dict()

# Contains argument cleaned for better an faster uses by the program
cleaned_arguments = dict()

# Contains useful statistics for the user
statistics = dict()


def main_entry_point():
    global arguments
    global cleaned_arguments
    global statistics

    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments
    arguments, cleaned_arguments = parse_args_main_entry_point()

    # Prepare the database to be splitted
    has_ben_backuped = preprocessing(cleaned_arguments)
    if has_ben_backuped:
        input_path = cleaned_arguments[gpn.modified_database_name()]
    else:
        input_path = cleaned_arguments[gpn.database()]

    print(arguments)
    print(cleaned_arguments)
    print(input_path)

    split2(filepath=input_path,
           delimiter=cleaned_arguments[gpn.delimiter()],
           row_limit=cleaned_arguments[gpn.training_value()],
           have_header=cleaned_arguments[gpn.have_header()],
           method=cleaned_arguments[gpn.initial_split_method()],
           output_name_train=cleaned_arguments[gpn.initial_split_train_name()],
           output_name_test=cleaned_arguments[gpn.initial_split_test_name()],
           encoding=cleaned_arguments[gpn.encoding()],
           class_name=cleaned_arguments[gpn.class_name()],
           number_of_rows=cleaned_arguments[ggv.number_of_rows()])


def forest_entry_point():
    global arguments
    global cleaned_arguments
    global statistics

    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    global arguments
    global cleaned_arguments
    global statistics

    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
