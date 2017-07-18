from fforest.src.core.phase.ending.ending import failure_safe, ending
from fforest.src.core.phase.learning_process.forest_construction import forest_construction
from fforest.src.core.phase.learning_process.forest_reduction import forest_reduction
from fforest.src.core.phase.phase import call_all_phases
from fforest.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point
from fforest.src.core.phase.preprocessing.preparsing import compute_first_phase
from fforest.src.core.phase.preprocessing.preprocessing import preprocessing
import fforest.src.getters.environment as env


@failure_safe
def main_entry_point() -> None:
    first_phase = compute_first_phase()
    call_all_phases(starting_phase=first_phase,
                    parsing_function=parse_args_main_entry_point)


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
