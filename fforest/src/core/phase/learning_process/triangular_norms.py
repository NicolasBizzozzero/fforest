from enum import IntEnum


KEY_DEFAULT_METHOD = "tnorm_"


def tnorm_to_str(tnorm_number: int) -> str:
    if tnorm_number == TriangularNorm.CLASSIC.value:
        return "classic"
    elif tnorm_number == TriangularNorm.ZADEH.value:
        return "zadeh"
    elif tnorm_number == TriangularNorm.LUKA.value:
        return "luka"
    else:
        return KEY_DEFAULT_METHOD + str(tnorm_number)


class TriangularNorm(IntEnum):
    CLASSIC = 0
    ZADEH = 1
    LUKA = 2
