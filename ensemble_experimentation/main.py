from ensemble_experimentation.src.core.phase.ending.ending import failure_safe
from ensemble_experimentation.src.core.phase.initialization.initial_split import initial_split
from ensemble_experimentation.src.core.phase.initialization.reference_split import reference_split
from ensemble_experimentation.src.core.phase.learning_process.forest_construction import forest_construction
from ensemble_experimentation.src.core.phase.learning_process.forest_reduction import forest_reduction
from ensemble_experimentation.src.core.phase.learning_process.subsubtrain_split import subsubtrain_split
from ensemble_experimentation.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point
from ensemble_experimentation.src.core.phase.preprocessing.preprocessing import preprocessing


@failure_safe
def main_entry_point():
    # Parsing and cleaning command-line arguments.
    # After calling this method, all variables defined in the `environment` module will be initialized
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
    forest_reduction()


def forest_entry_point():
    pass


def forest_reduction_entry_point():
    pass


if __name__ == "__main__":
    pass
