from fforest.src.core.phase.ending.ending import failure_safe
from fforest.src.core.phase.initialization.initial_split import initial_split
from fforest.src.core.phase.initialization.reference_split import reference_split
from fforest.src.core.phase.learning_process.forest_construction import forest_construction
from fforest.src.core.phase.learning_process.forest_reduction import forest_reduction
from fforest.src.core.phase.learning_process.subsubtrain_split import subsubtrain_split
from fforest.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point
from fforest.src.core.phase.preprocessing.preprocessing import preprocessing
from fforest.src.core.phase.ending.ending import dump_statistics_dictionary
from fforest.src.core.phase.performance_evaluation.forest_quality import forest_quality
from fforest.src.core.phase.performance_evaluation.classes_matrices import classes_matrices


@failure_safe
def main_entry_point() -> None:
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

    # Compute forest quality and construct classes matrices
    forest_quality()
    classes_matrices()

    dump_statistics_dictionary()


def preprocessing_entry_point() -> None:
    pass


def initialization_entry_point() -> None:
    pass


def learning_entry_point() -> None:
    pass


def reduction_entry_point() -> None:
    pass


if __name__ == "__main__":
    pass
