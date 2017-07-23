""" A set of tools to split databases into multiple databases.
All the methods postfixed by "2" are methods used to split the database into two other databases (usually a train and a
test database).
This module initialize the file handlers and the readers/writers, then redirect the program to the module corresponding
to the splitting method asked.
"""
import csv
import enum
from typing import Tuple, List

from fforest.src.core.splitting_methods.halfing import halfing
from fforest.src.core.splitting_methods.halfing import halfing2
from fforest.src.core.splitting_methods.keep_distribution import keep_distribution
from fforest.src.core.splitting_methods.keep_distribution import keep_distribution2
from fforest.src.file_tools.dialect import Dialect
from fforest.src.vrac.maths.maths import is_a_percentage


class UnknownSplittingMethod(Exception):
    def __init__(self, method_name: str):
        Exception.__init__(self, "The splitting method : \"{method_name}\" doesn't"
                                 " exists".format(method_name=method_name))


class InvalidValue(Exception):
    def __init__(self, row_limit: str):
        Exception.__init__(self, "The value \"{row_limit}\" is neither a percentage nor"
                                 " a number of rows.".format(row_limit=row_limit))


@enum.unique
class SplittingMethod(enum.IntEnum):
    UNKNOWN = 0
    HALFING = 1
    KEEP_DISTRIBUTION = 2


def str_to_splittingmethod(string: str) -> SplittingMethod:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for method_name, method_value in zip(SplittingMethod.__members__.keys(), SplittingMethod.__members__.values()):
        if string == method_name.lower():
            return method_value
    raise UnknownSplittingMethod(string)


def splittingmethod_to_str(splitting_method: SplittingMethod) -> str:
    """ Return the name of a splitting method as a lowercase str. """
    return splitting_method.name.lower()


def split2(*, class_name: int, input_path: str, method: SplittingMethod, number_of_rows: int, output_name_test: str,
           output_name_train: str, row_limit: int, dialect: Dialect) -> Tuple[int, int]:
    """ Open the initial database as input, open the two output databases as output, then give the reader and writers
    to the asked splitting2 method.
    You must pass each argument along with its name.
    """
    with open(input_path, mode="r", encoding=dialect.encoding, newline=dialect.line_delimiter) as input_file,\
            open(output_name_train, mode='w', encoding=dialect.encoding,
                 newline=dialect.line_delimiter) as output_train,\
            open(output_name_test, mode='w', encoding=dialect.encoding,
                 newline=dialect.line_delimiter) as output_test:

        input_reader = csv.reader(input_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                  quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        out_writer_train = csv.writer(output_train, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                      quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        out_writer_test = csv.writer(output_test, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                     quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)

        if method == SplittingMethod.HALFING:
            size_train, size_test = halfing2(input_reader, row_limit, out_writer_train, out_writer_test)
        elif method == SplittingMethod.KEEP_DISTRIBUTION:
            size_train, size_test = keep_distribution2(input_reader, row_limit, out_writer_train, out_writer_test,
                                                       class_name, number_of_rows)
        else:
            raise UnknownSplittingMethod(splittingmethod_to_str(method))

        return size_train, size_test


def split(*, class_name: int,  input_path: str, method: SplittingMethod, number_of_rows: int,  row_limit: int,
          output_paths: List[str], dialect: Dialect) -> List[int]:
    """ Open the initial database as input, open all the other databases as output, then give the reader and writers
    to the asked splitting method.
    You must pass each argument along with its name.
    """
    with open(input_path, mode='r', encoding=dialect.encoding, newline=dialect.line_delimiter) as input_file:
        out_files = [open(name, mode='w', encoding=dialect.encoding,
                          newline=dialect.line_delimiter) for name in output_paths]

        input_reader = csv.reader(input_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                  quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        out_writers = [csv.writer(f, delimiter=dialect.delimiter, quoting=dialect.quoting, quotechar=dialect.quote_char,
                                  skipinitialspace=dialect.skip_initial_space) for f in out_files]

        number_of_trees = len(output_paths)
        if method == SplittingMethod.HALFING:
            databases_size = halfing(input_reader, row_limit, out_writers, number_of_trees)
        elif method == SplittingMethod.KEEP_DISTRIBUTION:
            databases_size = keep_distribution(input_reader, row_limit, out_writers, number_of_trees, class_name,
                                               number_of_rows)
        else:
            raise UnknownSplittingMethod(splittingmethod_to_str(method))

        # Close all the file handlers
        map(lambda f: f.close(), out_files)

        return databases_size


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
