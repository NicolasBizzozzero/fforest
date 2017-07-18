from fforest.src.core.phase.ending.ending import failure_safe
from fforest.src.core.phase.phase import call_all_phases
from fforest.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point, \
    parse_args_preprocessing_entry_point
from fforest.src.core.phase.preprocessing.preparsing import compute_first_phase
from fforest.src.core.phase.preprocessing.preprocessing import preprocessing


@failure_safe
def main_entry_point() -> None:
    first_phase = compute_first_phase()
    call_all_phases(starting_phase=first_phase,
                    parsing_function=parse_args_main_entry_point)


def preprocessing_entry_point() -> None:
    parse_args_preprocessing_entry_point()
    preprocessing()


def initial_split_entry_point() -> None:
    pass


def reference_split_entry_point() -> None:
    pass


def subsubtrain_split_entry_point() -> None:
    pass


def learning_entry_point() -> None:
    pass


def reduction_entry_point() -> None:
    pass


def quality_entry_point() -> None:
    pass


def classes_matrices_entry_point() -> None:
    pass


if __name__ == "__main__":
    pass
