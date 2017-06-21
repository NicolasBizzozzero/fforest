import csv
from typing import Union

from ensemble_experimentation.src.vrac.maths import is_an_int


class UndefinedQuoting(Exception):
    def __init__(self, quoting: str):
        Exception.__init__(self, "The quoting value : \"{quoting}\" doesn't"
                                 " exists".format(quoting=quoting))


def str_to_quoting(string: str) -> int:
    string = string.lower()
    if string == "all":
        return csv.QUOTE_ALL
    elif string == "minimal":
        return csv.QUOTE_MINIMAL
    elif string == "nonnumeric":
        return csv.QUOTE_NONNUMERIC
    elif string == "none":
        return csv.QUOTE_NONE
    else:
        raise UndefinedQuoting(string)


def iter_rows(path: str, encoding: str = "utf8", delimiter: str = ",", quoting: int = 1,
              quote_char: str = "\"", skipinitialspace: bool = True) -> iter:
    """ Iterate trough the rows of the file located at `path`. """
    with open(path, encoding=encoding) as csv_file:
        content = csv.reader(csv_file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                             skipinitialspace=skipinitialspace)
        for line in content:
            yield line


def get_number_of_rows(path: str, encoding: str = "utf8", delimiter: str = ",") -> int:
    """ Return the number of rows of the file located at `path`. """
    with open(path, encoding=encoding) as csv_file:
        return len(list(csv.reader(csv_file, delimiter=delimiter))) - 1


def get_number_of_columns(path: str, encoding: str = "utf8", delimiter: str = ",") -> int:
    """ Return the number of columns of the file located at `path`. """
    return len(next(iter_rows(path, encoding=encoding, delimiter=delimiter)))


def get_row(path: str, row_number: int, encoding: str = "utf8") -> Union[list, None]:
    """ Return the `row_number`-th row as a list from the file located at `path`.
    The rows are indexed from 1 to len(`path`).
    If a `row_number` is out-of-bound, this function return the `None` value.
    """
    if row_number <= 0 or row_number > get_number_of_rows(path, encoding=encoding):
        return None

    current_row = 0
    for row in iter_rows(path):
        current_row += 1
        if current_row == row_number:
            return row


# TODO: add parameter delimiter
def select_all_rows_where(path: str, predicate: callable, encoding: str = "utf8") -> list:
    """ Return all rows from the CSV file at `path` with which the `predicate` return True.
    The rows are casted as a dictionary.

        Example:
            >>> # SELECT all rows WHERE age > 25
            >>> select_all_rows_where(path, lambda r: r["age"] > 25)

            >>> # SELECT all rows WHERE money < 1000 AND city == 'Paris'
            >>> select_all_rows_where(path, lambda r: r["money"] < 1000 and r["city"] == "Paris")
    """
    with open(path, encoding=encoding) as csv_file:
        return [row for row in csv.DictReader(csv_file) if predicate(row)]


# TODO: IndexError will probably happen, embed this function into a 'try except' and return None.
# TODO: add parameter delimiter
def get_identified_row(path: str, identifier_name: str, row_id: int, encoding: str = "utf8"):
    """ A wrapper for `select_all_rows_where`.
    Select the row identified at the column `identifier_name` with the value `row_id`.

        Example:
        >>> # SELECT row WHERE ID == 77
        >>> get_identified_row(path, "ID", 77)
    """
    return select_all_rows_where(path, lambda r: r[identifier_name] == row_id, encoding=encoding)[0]


def write_header(input_reader, *out_writers, replace_fieldnames: bool = False):
    header = next(input_reader)

    for writer in out_writers:
        writer.writerow(header)


def preprend_column(input_path: str, output_path: str, column: str, encoding: str = "utf8", delimiter: str = ","):
    if not is_an_int(column):
        header = next(iter_rows(input_path, encoding=encoding, delimiter=delimiter))
        index_column = header.index(column)
        preprend_column(input_path, output_path, index_column, encoding=encoding, delimiter=delimiter)
    else:
        content = [line for line in iter_rows(input_path, encoding=encoding, delimiter=delimiter)]
        with open(output_path, "w", encoding=encoding) as output_file:
            output_writer = csv.writer(output_file, delimiter=delimiter)
            for line in content:
                line.insert(0, (line.pop(column)))
                output_writer.writerow(line)


def append_column(input_path: str, output_path: str, column: str, encoding: str = "utf8", delimiter: str = ","):
    if not is_an_int(column):
        header = next(iter_rows(input_path, encoding=encoding, delimiter=delimiter))
        index_column = header.index(column)
        append_column(input_path, output_path, index_column, encoding=encoding, delimiter=delimiter)
    else:
        content = [line for line in iter_rows(input_path, encoding=encoding, delimiter=delimiter)]
        with open(output_path, "w", encoding=encoding) as output_file:
            output_writer = csv.writer(output_file, delimiter=delimiter)
            for line in content:
                line.append(line.pop(column))
                output_writer.writerow(line)


def find_index_for_class(input_path: str, class_name: str, encoding: str = "utf8", delimiter: str = ",") -> int:
    """ Return the column index given a class name for a CSV file containing a header. """
    with open(input_path, encoding=encoding) as file:
        header = file.readline()

    list_header = [s.strip().strip("'\"") for s in header.split(delimiter)]
    return list_header.index(class_name)


def index_in_bounds(input_path: str, index: int, encoding: str = "utf8", delimiter: str = ",") -> bool:
    """ Check if an index is inbound of the CSV file columns. Columns can be accessed with a negative index. """
    length = get_number_of_columns(path=input_path, encoding=encoding, delimiter=delimiter)
    return (-length <= index < 0) or (0 <= index < length)
