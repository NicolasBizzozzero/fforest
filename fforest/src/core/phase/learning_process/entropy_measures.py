""" This module contains useful tools to manipulate the `EntropyMeasure` class.
The entropy measure is use to measure diversity inside a set of value. It is used by the 'Salammbô' software.
"""
import enum


@enum.unique
class EntropyMeasure(enum.IntEnum):
    SHANNON = 0


class UnknownEntropyMeasure(Exception):
    def __init__(self, entropy_measure_name: str):
        Exception.__init__(self, "The entropy measure \"{entropy_measure_name}\" doesn't"
                                 " exists".format(entropy_measure_name=entropy_measure_name))


def str_to_entropymeasure(string: str) -> EntropyMeasure:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for entropymeasure_name, entropymeasure_value in zip(EntropyMeasure.__members__.keys(),
                                                         EntropyMeasure.__members__.values()):
        if string == entropymeasure_name.lower():
            return entropymeasure_value
    raise UnknownEntropyMeasure(string)


def entropymeasure_to_str(measure: EntropyMeasure) -> str:
    """ Return the name of an entropy measure as a lowercase str. """
    return measure.name.lower()
