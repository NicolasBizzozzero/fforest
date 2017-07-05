import enum
import fforest.src.getters.environment as env
from fforest.src.core.phase.ending.ending import ending


@enum.unique
class Phase(enum.IntEnum):
    NONE = 0
    PREPROCESSING = 1
    INITIAL_SPLIT = 2
    REFERENCE_SPLIT = 3
    SUBSUBTRAIN_SPLIT = 4
    LEARNING = 5
    REDUCTION = 6
    QUALITY = 7
    CLASSES_MATRICES = 8
    ENDING = 9


class UnknownPhase(Exception):
    def __init__(self, phase_name: str):
        Exception.__init__(self, "The phase \"{phase_name}\" doesn't"
                                 " exists".format(phase_name=phase_name))


def str_to_phase(string: str) -> Phase:
    string = string.lower()
    if string == "none":
        return Phase.NONE
    elif string == "preprocessing":
        return Phase.PREPROCESSING
    elif string == "initial_split":
        return Phase.INITIAL_SPLIT
    elif string == "reference_split":
        return Phase.REFERENCE_SPLIT
    elif string == "subsubtrain_split":
        return Phase.SUBSUBTRAIN_SPLIT
    elif string == "learning":
        return Phase.LEARNING
    elif string == "reduction":
        return Phase.REDUCTION
    elif string == "quality":
        return Phase.QUALITY
    elif string == "classes_matrices":
        return Phase.CLASSES_MATRICES
    elif string == "ending":
        return Phase.ENDING
    else:
        raise UnknownPhase(string)


def phase_to_str(phase: Phase) -> str:
    if phase == Phase.NONE:
        return "none"
    elif phase == Phase.PREPROCESSING:
        return "preprocessing"
    elif phase == Phase.INITIAL_SPLIT:
        return "initial_split"
    elif phase == Phase.REFERENCE_SPLIT:
        return "reference_split"
    elif phase == Phase.SUBSUBTRAIN_SPLIT:
        return "subsubtrain_split"
    elif phase == Phase.LEARNING:
        return "learning"
    elif phase == Phase.REDUCTION:
        return "reduction"
    elif phase == Phase.QUALITY:
        return "quality"
    elif phase == Phase.CLASSES_MATRICES:
        return "classes_matrices"
    elif phase == Phase.ENDING:
        return "ending"
    else:
        return "unknown"


def get_next_phase(phase: Phase) -> Phase:
    if phase == Phase.ENDING:
        return Phase.NONE

    for next_phase in Phase:
        if phase.value + 1 == next_phase.value:
            return next_phase


def exit_if_last_phase() -> None:
    if env.current_phase == env.last_phase:
        ending()


def increment_phase() -> None:
    exit_if_last_phase()
    env.current_phase = get_next_phase(env.current_phase)
