import enum


class Format(enum.IntEnum):
    UNKNOWN = 0
    CSV = 1


def string_to_format(string: str) -> Format:
    string = string.lower()
    if string == "csv":
        return Format.CSV
    else:
        return Format.UNKNOWN


def format_to_string(form: Format) -> str:
    if form == Format.CSV:
        return "csv"
    else:
        return ""
