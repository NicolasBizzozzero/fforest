""" This module contains useful tools to manipulate the `Format` class.
This class help to identify the format used in a file, and the common extensions associated with it.
"""
import enum


@enum.unique
class Format(enum.IntEnum):
    UNKNOWN = -1
    CSV = 0
    JSON = 1
    XML = 2
    YAML = 3


class UnknownFormat(Exception):
    def __init__(self, format_name: str):
        Exception.__init__(self, "The format \"{format_name}\" doesn't"
                                 " exists".format(format_name=format_name))


def str_to_format(string: str) -> Format:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for phase_name, phase_value in zip(Format.__members__.keys(), Format.__members__.values()):
        if string == phase_name.lower():
            return phase_value
    raise UnknownFormat(string)


def format_to_string(form: Format) -> str:
    if form == Format.CSV:
        return "csv"
    else:
        return ""
