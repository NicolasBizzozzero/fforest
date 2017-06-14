import json
import ntpath
import os
import sys
import time
from typing import Callable


def timeit(func: Callable) -> Callable:
    """ Decorator who calculate and print execution time of a function into the standard output. """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Execution time for \"" + str(func.func_name) + "\" : " + str(end - start) + " seconds")
        return result
    return wrapper


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
    return is_a_float(s) and 0.0 <= float(s) <= 1.0


def get_filename(path: str, with_extension: bool = False) -> str:
    """ Extract the filename from a path.

    Examples:
        >>> get_filename("file.txt")
        'file'
        >>> get_filename("file.txt", with_extension=True)
        'file.txt'
        >>> get_filename("dir/file.txt")
        'file'
        >>> get_filename("dir/subdir/file.txt")
        'file'
        >>> get_filename("dir/subdir/file")
        'file'
        >>> get_filename("dir/subdir/file.txt.txt")
        'file'
        >>> get_filename("dir/subdir/file.txt.txt", with_extension=True)
        'file.txt.txt'
        >>> get_filename("dir/subdir/file.txt.txt/")
        'file'
        >>> get_filename("dir/subdir/file.txt.txt/", with_extension=True)
        'file.txt.txt'
        >>> get_filename("/dir/subdir/file.txt.txt/")
        'file'
        >>> get_filename("/dir/subdir/file.txt.txt/", with_extension=True)
        'file.txt.txt'
        >>> get_filename("/dir/subdir/file.txt.txt.txt.txt.txt.txt.txt.txt/")
        'file'
    """
    head, tail = ntpath.split(path)
    if with_extension:
        return tail or ntpath.basename(head)
    else:
        result = tail or ntpath.basename(head)
        while "." in result:
            result = os.path.splitext(result)[0]
        return result


def create_dir(directory: str) -> None:
    """ Create a directory if it doesn't exists. Otherwise, do nothing"""
    os.makedirs(directory, exist_ok=True)


def dump_dict(d: dict, path: str, encoding: str = None, indent: int = 4,
              sort_keys: bool = True) -> None:
    """ Dump the content of `d` into the path `path`.
    You can pass an optional encoding, used to open the file, the indent used by the JSON writer and a boolean, which
    makes you able to sort the keys into the file or not.
    """
    with open(path, 'w', encoding=encoding) as file:
        return json.dump(d, file, indent=indent, sort_keys=sort_keys)


def eprint(*args, **kwargs):
    """ Print wrapper for `stderr`. """
    print(*args, file=sys.stderr, **kwargs)
