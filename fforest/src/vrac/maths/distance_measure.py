from typing import Iterable, Callable

import scipy as sp
import enum

from fforest.src.vrac.maths.maths import Number


@enum.unique
class DistanceMeasure(enum.IntEnum):
    EUCLIDEAN = 0
    MANHATTAN = 1


class UnknownDistanceMeasure(Exception):
    def __init__(self, measure_name: str):
        Exception.__init__(self, "The distance measure \"{measure_name}\" doesn't"
                                 " exists".format(measure_name=measure_name))


def str_to_distancemeasure(string: str) -> DistanceMeasure:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for measure_name, measure_value in zip(DistanceMeasure.__members__.keys(), DistanceMeasure.__members__.values()):
        if string == measure_name.lower():
            return measure_value
    raise UnknownDistanceMeasure(string)


def distancemeasure_to_str(form: DistanceMeasure) -> str:
    """ Return the name of a DistanceMeasure as a lowercase str. """
    return form.name.lower()


def distancemeasure_to_function(form: DistanceMeasure) -> Callable:
    """ Return the name of a DistanceMeasure as a its respective function. """
    pass


def euclidean(vector1: Iterable[Number], vector2: Iterable[Number]) -> float:
    return sp.spatial.distance.euclidean(vector1, vector2)


def manhattan(vector1: Iterable[Number], vector2: Iterable[Number]) -> int:
    pass
