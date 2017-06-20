from ensemble_experimentation.src.core.ending.ending import dump_statistics_dictionary, failure_safe
from ensemble_experimentation.src.core.initialization.arg_parser import parse_args_main_entry_point
from ensemble_experimentation.src.core.initialization.initial_split import initial_split
from ensemble_experimentation.src.core.initialization.preprocessing import preprocessing
from ensemble_experimentation.src.core.initialization.reference_split import reference_split
from ensemble_experimentation.src.core.learning_process.forest_construction import forest_construction
from ensemble_experimentation.src.core.learning_process.subsubtrain_split import subsubtrain_split


@failure_safe
def main_entry_point():
    print("Hello main_entry_point")

    # Parsing and cleaning command-line arguments.
    # After calling this method, the parsed arguments and the cleaned arguments will be stored as dictionaries into the
    # `environment` module.
    parse_args_main_entry_point()

    # Preprocessing of the database
    preprocessing()

    # Split the initial database into the train and test database
    initial_split()

    # Split the train database into the reference database and the subtrain database
    reference_split()

    # Split the subtrain database into multiple subsubtrain databases
    subsubtrain_split()

    # Construct forest and compute efficiency vectors
    forest_construction()

    dump_statistics_dictionary()


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
#    print(execute_and_get_stdout("bin/Salammbo", "-L", "-R", "-c 2", "-N", "-M", "-f 2",
#                                 "../bank/subtrain/001_sstrain/001_sstrain.csv",
#                                 "../bank/subtrain/reference.csv"))