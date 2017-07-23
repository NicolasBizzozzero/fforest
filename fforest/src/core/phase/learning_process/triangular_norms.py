""" This module contains useful tools to manipulate the `TriangularNorm` class.
A T-Norm, or Triangular Norm, is a binary operation used in Fuzzy Logic and which generalize a conjunction.
It it used by the 'Salammbô' software.
"""
import enum


KEY_DEFAULT_METHOD = "tnorm_"


@enum.unique
class TriangularNorm(enum.IntEnum):
    CLASSIC = 0
    ZADEH = 1
    LUKA = 2


def tnorm_to_str(tnorm_number: int) -> str:
    """ Return the name of a Triangular Norm number as a lowercase str. """
    try:
        return TriangularNorm(tnorm_number).name.lower()
    except ValueError:
        return KEY_DEFAULT_METHOD + str(tnorm_number)
