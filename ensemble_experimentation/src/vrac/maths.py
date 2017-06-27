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
