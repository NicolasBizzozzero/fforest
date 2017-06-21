from enum import IntEnum


class EntropyMeasure(IntEnum):
    UNKNOWN = 0
    SHANNON = 1


def str_to_entropy_measure(string: str) -> EntropyMeasure:
    string = string.lower()
    if string == "shannon":
        return EntropyMeasure.SHANNON
    else:
        return EntropyMeasure.UNKNOWN
