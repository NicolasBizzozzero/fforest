from enum import IntEnum


class EntropyMeasure(IntEnum):
    UNKNOWN = 0
    SHANNON = 1


def str_to_entropymeasure(string: str) -> EntropyMeasure:
    string = string.lower()
    if string == "shannon":
        return EntropyMeasure.SHANNON
    else:
        return EntropyMeasure.UNKNOWN


def entropymeasure_to_str(measure: EntropyMeasure) -> str:
    if measure == EntropyMeasure.SHANNON:
        return "shannon"
    else:
        return "unknown"
