from enum import IntEnum


KEY_DEFAULT_METHOD = "method_"


def methodnum_to_str(method_number: int) -> str:
    if method_number == ClassificationMethod.CLASSIC.value:
        return "classic"
    elif method_number == ClassificationMethod.ZADEH.value:
        return "zadeh"
    elif method_number == ClassificationMethod.LUKA.value:
        return "luka"
    else:
        return KEY_DEFAULT_METHOD + str(method_number)


class ClassificationMethod(IntEnum):
    CLASSIC = 0
    ZADEH = 1
    LUKA = 2
