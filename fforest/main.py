from fforest.src.core.phase.ending.ending import failure_safe, ending
from fforest.src.core.phase.initialization.initial_split import initial_split
from fforest.src.core.phase.initialization.reference_split import reference_split
from fforest.src.core.phase.learning_process.forest_construction import forest_construction
from fforest.src.core.phase.learning_process.forest_reduction import forest_reduction
from fforest.src.core.phase.learning_process.subsubtrain_split import subsubtrain_split
from fforest.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point
from fforest.src.core.phase.preprocessing.preprocessing import preprocessing
from fforest.src.core.phase.performance_evaluation.forest_quality import forest_quality
from fforest.src.core.phase.performance_evaluation.classes_matrices import classes_matrices
import fforest.src.getters.environment as env


@failure_safe
def main_entry_point() -> None:
    # Parsing and cleaning command-line arguments.
    # After calling this method, all variables defined in the `environment` module will be initialized
    parse_args_main_entry_point()

    preprocessing()
    initial_split()
    reference_split()
    subsubtrain_split()


    exit(0)


    forest_construction()
    forest_reduction()
    forest_quality()
    classes_matrices()
    ending()


def preprocessing_entry_point() -> None:
    preprocessing()
    ending()


def initialization_entry_point() -> None:
    pass


def learning_entry_point() -> None:
    forest_construction()
    ending()


def reduction_entry_point() -> None:
    forest_reduction()
    ending()


if __name__ == "__main__":
    pass
