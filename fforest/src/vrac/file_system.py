import json
import os


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
        'dir/subdir'
        >>> get_path("/dir/subdir/file.txt.txt/")
        '/dir/subdir'
        >>> get_path("/dir/subdir/file.txt.txt.txt.txt.txt.txt.txt.txt/")
        '/dir/subdir'
    """
    if not path:
        return ""
    if path[-1] == "/":
        path = path[:-1]
    if ("/" not in path) and ("." not in path):
        return path
    result = path[:-len(get_filename(path, with_extension=True))]
    if result and result[-1] == "/":
        result = result[:-1]
    return result


def get_file_content(path: str, encoding: str = "utf8") -> str:
    """ Return all the file content as a str. """
    with open(path, encoding=encoding) as file:
        return "".join(file.readlines())


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


def dump_string(path: str, string: str, mode: str = "w", encoding: str = "utf8") -> None:
    """ Dump the string into the file located at `path` with the mode `mode`. """
    with open(path, mode, encoding=encoding) as file:
        file.write(string)


def extract_first_line(path: str, encoding: str = "utf8") -> str:
    """ Remove the first line from a file, then return it. """
    content = get_file_content(path, encoding=encoding)
    first_line, *rest = content.split("\n")
    rest = filter(lambda s: s != "", rest)
    dump_string(path, "\n".join(rest))
    return first_line
