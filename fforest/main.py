""" This module contains all the entry points created during the software installation. They're all protected by the
`failure_safe` decorator, which safely dump the environment created and the data computed before exiting the process.
The main entry point is the `main_entry_point` method. It executes all the existing phases sequentially by default, and
can also start at a previously computed phase (thus the obligatory `compute_first_phase` statement). Every other method
is an entry point for a specific phase, and exit the process right after its termination.
"""
from fforest.src.core.phase.ending.ending import failure_safe
from fforest.src.core.phase.phase import call_all_phases
from fforest.src.core.phase.preprocessing.args_parser import parse_args_main_entry_point
from fforest.src.core.phase.preprocessing.preparsing import compute_first_phase



def main_entry_point() -> None:
    # Parse only a part of arguments needed to know if the user asked to start the software from the beginning or from a
    # specific phase.
    first_phase = compute_first_phase()

    # Call successively all phases, starting with the `first_phase` (computed by the previous statement).
    call_all_phases(starting_phase=first_phase,
                    parsing_function=parse_args_main_entry_point)


@failure_safe
def preprocessing_entry_point() -> None:
    pass


@failure_safe
def initial_split_entry_point() -> None:
    pass


@failure_safe
def reference_split_entry_point() -> None:
    pass


@failure_safe
def subsubtrain_split_entry_point() -> None:
    pass


@failure_safe
def learning_entry_point() -> None:
    pass


@failure_safe
def reduction_entry_point() -> None:
    pass


@failure_safe
def quality_entry_point() -> None:
    pass


@failure_safe
def classes_matrices_entry_point() -> None:
    pass


if __name__ == "__main__":
    pass
