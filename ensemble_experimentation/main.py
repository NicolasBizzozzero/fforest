import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.splitting_methods import split2
from ensemble_experimentation.src.splitting_methods import SplittingMethod
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point


def main_entry_point():
    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments
    args = parse_args_main_entry_point()
    print(args)

    # Prepare the database to be splitted
    has_ben_backuped = preprocessing(args)

    print(args)
    if has_ben_backuped:
        input_path = args[gpn.modified_database_name()]
    else:
        input_path = args[gpn.database()]
    split2(filepath=input_path, delimiter=args[gpn.delimiter()], row_limit=args[gpn.training_value()],
           have_header=args[gpn.have_header()], method=args[gpn.initial_split_method()],
           output_name_train=args[gpn.initial_split_train_name()],
           output_name_test=args[gpn.initial_split_test_name()],
           encoding=args[gpn.encoding()])


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
