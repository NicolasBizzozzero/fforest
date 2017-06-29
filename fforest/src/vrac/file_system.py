import json
import os
import errno
import sys


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


def is_pathname_valid(pathname: str) -> bool:
    """ `True` if the passed pathname is a valid pathname for the current OS, `False` otherwise.
    Shamelessly pasted from https://stackoverflow.com/a/34102855
    """
    # Windows-specific error code indicating an invalid pathname.
    # See also : https://msdn.microsoft.com/en-us/library/windows/desktop/ms681382%28v=vs.85%29.aspx
    ERROR_INVALID_NAME = 123

    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?
