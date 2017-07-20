from typing import Union
import numpy as np

Number = Union[int, float, complex]


def delta(n1: Number, n2: Number) -> Number:
    """ Return the difference between two numbers.

        Example :
        >>> delta(1, 2)
        1
        >>> delta(2, 1)
        1
    """
    return abs(n2 - n1)


def gamma(n: Number) -> Number:
    """ In mathematics, the gamma function (represented by the capital Greek alphabet letter Γ) is an extension of the
    factorial function, with its argument shifted down by 1, to real and complex numbers.

        Source :
        https://en.wikipedia.org/wiki/Gamma_function
    """
    return np.math.factorial(n - 1)


def round_float(f: float, epsilon: float = 0.0000000000000002) -> Union[float, int]:
    """ Round a float if it's very close to an integer. Else, do nothing and return it.
        Example :
        >>> round_float(0.9999999999999999)
        1
        >>> round_float(0.9999999999999998)
        0.9999999999999998
        >>> round_float(0.8999999999999999)
        0.9
        >>> round_float(0.7999999999999999)
        0.8
        >>> round_float(0.30000000000000004)
        0.3
    """
    if delta(round(f), f) < epsilon:
        return int(round(f))
    return f


def is_a_float(s: str) -> bool:
    """ Check if a parsed string is a float.

        Example :
        >>> is_a_float("0.0")
        True
        >>> is_a_float("0.1")
        True
        >>> is_a_float("1.0")
        True
        >>> is_a_float("1.1")
        True
        >>> is_a_float("75")
        False
        >>> is_a_float("abcd")
        False
    """
    try:
        float(s)
        return "." in s
    except ValueError:
        return False


def is_an_int(s: str) -> bool:
    """ Check if a parsed string is an int.

        Example :
        >>> is_an_int("0.0")
        False
        >>> is_an_int("0.1")
        False
        >>> is_an_int("1.0")
        False
        >>> is_an_int("75")
        True
        >>> is_an_int("abcd")
        False
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_a_percentage(s: str) -> bool:
    """ Check if a parsed string is a percentage.

        Example :
        >>> is_a_percentage("0.0")
        True
        >>> is_a_percentage("0.1")
        True
        >>> is_a_percentage("1.0")
        True
        >>> is_a_percentage("1.1")
        False
        >>> is_a_percentage("75")
        False
        >>> is_a_percentage("abcd")
        False
    """
    return is_a_float(s) and 0.0 <= float(s) <= 1


def convert_row_limit(row_limit: str, number_of_rows: int) -> int:
    """ Convert the parsed `row_limit` to a number of rows if it's a percentage, or raise an exception otherwise

        Example :
        >>> convert_row_limit("0.5", 1000)
        500
        >>> convert_row_limit("500", 1000)
        Traceback (most recent call last):
         ...
        arg_parser.InvalidValue: The value "500" is neither a percentage nor a number of rows.
        >>> convert_row_limit("500.1", 1000)
        Traceback (most recent call last):
         ...
        arg_parser.InvalidValue: The value "500.1" is neither a percentage nor a number of rows.
    """
    if not is_a_percentage(row_limit):
        raise InvalidValue(row_limit)
    percentage = float(row_limit)
    return int(round(percentage * number_of_rows))


class InvalidValue(Exception):
    def __init__(self, row_limit: str):
        Exception.__init__(self, "The value \"{row_limit}\" is neither a percentage nor"
                                 " a number of rows.".format(row_limit=row_limit))


if __name__ == "__main__":
    pass
