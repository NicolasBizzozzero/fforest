""" In linear algebra and functional analysis, a norm is a function that assigns a strictly positive value to each
vector in a vector space (save for the zero vector, which is assigned a length of zero).
https://en.wikipedia.org/wiki/Norm_(mathematics)
"""

from typing import Iterable

from fforest.src.vrac.maths.maths import Number
import numpy as np


def euclidean(vector: Iterable[Number]) -> float:
    """ Compute the Euclidean norm of a vector of arbitrary dimension.
    https://en.wikipedia.org/wiki/Norm_%28mathematics%29#Euclidean_norm

    Examples :
        >>> euclidean([0, 0, 0, 0])
        0.0
        >>> euclidean([1, 1, 1, 1])
        2.0
        >>> euclidean([4, 8, 15, 16, 23, 42])
        53.422841556772326
    """
    return np.linalg.norm(vector)


def frobenius(vector: Iterable[Number]) -> float:
    """ Compute the Frobenius norm of a vector of arbitrary dimension.
    https://en.wikipedia.org/wiki/Norm_%28mathematics%29#Euclidean_norm

    Examples :
        >>> frobenius([0, 0, 0, 0])
        0.0
        >>> frobenius([1, 1, 1, 1])
        2.0
        >>> frobenius([4, 8, 15, 16, 23, 42])
        53.422841556772326
    """
    return euclidean(vector)


def manhattan(vector: Iterable[Number]) -> int:
    """ Compute the Manhattan norm of a vector of arbitrary dimension.
    https://en.wikipedia.org/wiki/Norm_%28mathematics%29#Taxicab_norm_or_Manhattan_norm

    Examples :
        >>> manhattan([0, 0, 0, 0])
        0
        >>> manhattan([1, 1, 1, 1])
        4
        >>> manhattan([4, 8, 15, 16, 23, 42])
        108
    """
    return np.sum(np.absolute(vector))
