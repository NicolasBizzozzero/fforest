""" This module contains useful tools to manipulate the `QualityComputingMethod` class.
This class enumerate methods used to compute the quality of a fuzzy forest.
"""
import enum


@enum.unique
class QualityComputingMethod(enum.IntEnum):
    KAPPARIFQIMARSALA = 0


class UnknownQualityComputingMethod(Exception):
    def __init__(self, method_name: str = "unknown"):
        Exception.__init__(self, "The quality computing method : \"{method_name}\" doesn't"
                                 " exists".format(method_name=method_name))


def str_to_qualitycomputingmethod(string: str):
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for computing_method_name, computing_method_value in zip(QualityComputingMethod.__members__.keys(),
                                                             QualityComputingMethod.__members__.values()):
        if string == computing_method_name.lower():
            return computing_method_value
    raise UnknownQualityComputingMethod(string)
