import json
import os
import errno
import sys

from fforest.src.file_tools.dialect import Dialect


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
    head, tail = os.path.split(path)
    if with_extension:
        return tail or os.path.basename(head)
    else:
        result = tail or os.path.basename(head)
        while "." in result:
            result = os.path.splitext(result)[0]
        return result


def get_path(path: str) -> str:
    """ Extract the path from a path with a filename.

    Examples:
        >>> get_path("")
        ''
        >>> get_path("file.txt")
        ''
        >>> get_path("directory")
        'directory'
        >>> get_path("dir/file.txt")
        'dir'
        >>> get_path("dir/subdir/file.txt")
        'dir/subdir'
        >>> get_path("dir/subdir/file")
        'dir/subdir'
        >>> get_path("dir/subdir/file.txt.txt")
        'dir/subdir'
        >>> get_path("dir/subdir/file.txt.txt/")
        'dir/subdir/file.txt.txt'
        >>> get_path("/dir/subdir/file.txt.txt/")
        '/dir/subdir/file.txt.txt'
        >>> get_path("/dir/subdir/file.txt.txt.txt.txt.txt.txt.txt.txt")
        '/dir/subdir'
        >>> get_path("/dir/subdir/file.txt.txt.txt.txt.txt.txt.txt.txt/")
        '/dir/subdir/file.txt.txt.txt.txt.txt.txt.txt.txt'
    """
    return os.path.dirname(path)


def get_absolute_path(path: str) -> str:
    """ Give the absolute path of a file or directory. """
    return os.path.abspath(path)


def get_file_content(path: str, dialect: Dialect) -> str:
    """ Return all the file content as a string. """
    with open(path, encoding=dialect.encoding, newline=dialect.line_delimiter) as file:
        return "".join(file.readlines())


def create_dir(directory: str) -> None:
    """ Create a directory if it doesn't exists. Otherwise, do nothing"""
    os.makedirs(directory, exist_ok=True)


def dump_dict(d: dict, path: str, dialect: Dialect, indent: int = 4, sort_keys: bool = True) -> None:
    """ Dump the content of `d` into the path `path`.
    You can pass an optional encoding, used to open the file, the indent used by the JSON writer and a boolean, which
    makes you able to sort the keys into the file or not.
    """
    with open(path, 'w', encoding=dialect.encoding, newline=dialect.line_delimiter) as file:
        return json.dump(d, file, indent=indent, sort_keys=sort_keys)


def dump_string(path: str, string: str, dialect: Dialect, mode: str = "w") -> None:
    """ Dump the string into the file located at `path` with the mode `mode`. """
    with open(path, mode, encoding=dialect.encoding, newline=dialect.line_delimiter) as file:
        file.write(string)


def extract_first_line(path: str, dialect: Dialect) -> str:
    """ Remove the first line from a file, then return it. """
    # Extract first line
    content = get_file_content(path, dialect=dialect)
    first_line, *rest = content.split("\n")

    # Clean and rewrite the rest
    rest = filter(lambda s: s != "", rest)
    dump_string(path, "\n".join(rest), dialect=dialect)

    return first_line
