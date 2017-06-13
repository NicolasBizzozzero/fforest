import enum


class Format(enum.IntEnum):
    UNKNOWN = 0
    CSV = 1


def str_to_format(string: str) -> Format:
    string = string.lower()
    if string == "csv":
        return Format.CSV
    else:
        return Format.UNKNOWN
