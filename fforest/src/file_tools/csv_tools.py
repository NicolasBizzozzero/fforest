import csv
from typing import Union, List

from fforest.src.vrac.maths import is_an_int


class NamedAttributeButNoHeader(Exception):
    def __init__(self):
        Exception.__init__(self, "Impossible to access a named attribute with no header.")


class EmptyHeader(Exception):
    def __init__(self, database_path):
        Exception.__init__(self, "The header of the database located at \"{path}\" is "
                                 "empty.".format(path=database_path))


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


def iter_rows(path: str, skip_header: bool = False, encoding: str = "utf8", delimiter: str = ",",
              quoting: int = csv.QUOTE_NONNUMERIC, quote_char: str = "\"", line_delimiter: str = None,
              skip_initial_space: bool = True) -> iter:
    """ Iterate trough the rows of the file located at `path`. """
    with open(path, encoding=encoding, newline=line_delimiter) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)

        if skip_header:
            next(reader)

        for row in reader:
            if row:
                yield row


def get_header(path: str, encoding: str = "utf8", delimiter: str = ",", quoting: int = csv.QUOTE_NONNUMERIC,
               quote_char: str = "\"", line_delimiter: str = None, skip_initial_space: bool = True) -> List[str]:
    """ Return the header located in `path`.

        Example :
        >>> get_header("../../test/data/bank.csv", delimiter=";")[:11]
        ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month']
     """
    with open(path, encoding=encoding, newline=line_delimiter) as csv_file:
        return next(csv.reader(csv_file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                               skipinitialspace=skip_initial_space))


def get_number_of_rows(path: str, encoding: str = "utf8", delimiter: str = ",", quoting: int = csv.QUOTE_NONNUMERIC,
                       quote_char: str = "\"", line_delimiter: str = None, skip_initial_space: bool = True) -> int:
    """ Return the number of rows, header included, newline at the end excluded, of the file located at `path`.

        Example :
        >>> get_number_of_rows("../../test/data/bank.csv", delimiter=";")
        4522
    """
    number_of_rows = 0
    with open(path, encoding=encoding, newline=line_delimiter) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)

        for row in reader:
            if row:
                number_of_rows += 1
    return number_of_rows


def get_number_of_columns(path: str, encoding: str = "utf8", delimiter: str = ",", quoting: int = csv.QUOTE_NONNUMERIC,
                          quote_char: str = "\"", line_delimiter: str = None, skip_initial_space: bool = True) -> int:
    """ Return the number of columns of the file located at `path`.

        Example :
        >>> get_number_of_columns("../../test/data/bank.csv", delimiter=";")
        17
    """
    return len(next(iter_rows(path, encoding=encoding, delimiter=delimiter, quoting=quoting, quote_char=quote_char,
                              skip_initial_space=skip_initial_space, line_delimiter=line_delimiter)))


def get_row(path: str, row_number: int, skip_header: bool = False, encoding: str = "utf8", delimiter: str = ",",
            quoting: int = csv.QUOTE_NONNUMERIC, quote_char: str = "\"", line_delimiter: str = None,
            skip_initial_space: bool = True) -> Union[list, None]:
    """ Return the `row_number`-th row as a list from the file located at `path`.
    The rows are indexed from 1 to len(`path`).
    If a `row_number` is out-of-bound, this function return the `None` value.

        Example :
        >>> get_row("../../test/data/bank.csv", -1, delimiter=";") is None
        True
        >>> get_row("../../test/data/bank.csv", get_number_of_rows("../../test/data/bank.csv", delimiter=";") + 1,
        ...                                     delimiter=";") is None
        True
        >>> get_row("../../test/data/bank.csv", 77, delimiter=";")[:14]
        [54.0, 'management', 'divorced', 'tertiary', 'no', 3222.0, 'no', 'no', 'cellular', 14.0, 'aug', 67.0, 2.0, -1.0]
    """
    if row_number <= 0:
        return None

    current_row = 0
    for row in iter_rows(path=path, skip_header=skip_header, encoding=encoding, delimiter=delimiter, quoting=quoting,
                         quote_char=quote_char, line_delimiter=line_delimiter, skip_initial_space=skip_initial_space):
        current_row += 1
        if current_row == row_number:
            return row


def get_column(path: str, column: Union[str, int], have_header: bool = True, delimiter: str = ";",
               quoting: int = csv.QUOTE_NONNUMERIC, quote_character: str = "\"", encoding: str = "utf8",
               skip_initial_space: bool = True) -> List:
    """ Get a column from the CSV database with its index or its name. """
    content = list()
    with open(path, "r", encoding=encoding) as file:
        if type(column) == int:
            reader = csv.reader(file, delimiter=delimiter, quoting=quoting, quotechar=quote_character,
                                skipinitialspace=skip_initial_space)
        elif (type(column) == str) and have_header:
            reader = csv.DictReader(file, delimiter=delimiter, quoting=quoting, quotechar=quote_character,
                                    skipinitialspace=skip_initial_space)
        else:
            raise NamedAttributeButNoHeader()

        for row in reader:
            if row:
                content.append(row[column])
    if have_header and (type(column) == int):
        content.pop(0)
    return content


def select_all_rows_where(path: str, predicate: callable, delimiter: str = ";", quoting: int = csv.QUOTE_NONNUMERIC,
                          quote_character: str = "\"", encoding: str = "utf8", skip_initial_space: bool = True) -> list:
    """ Return all rows from the CSV file at `path` with which the `predicate` return True.
    The rows are casted as a dictionary.

        Example:
            >>> # SELECT all rows WHERE age > 25
            >>> select_all_rows_where(path, lambda r: r["age"] > 25)

            >>> # SELECT all rows WHERE money < 1000 AND city == 'Paris'
            >>> select_all_rows_where(path, lambda r: r["money"] < 1000 and r["city"] == "Paris")
    """
    with open(path, encoding=encoding) as csv_file:
        return [row for row in csv.DictReader(csv_file, delimiter=delimiter, quoting=quoting, quotechar=quote_character,
                                              skipinitialspace=skip_initial_space) if predicate(row)]


def get_identified_row(path: str, identifier_name: str, row_id: str, delimiter: str = ";",
                       quoting: int = csv.QUOTE_NONNUMERIC, quote_character: str = "\"", encoding: str = "utf8",
                       skip_initial_space: bool = True) -> Union[List, None]:
    """ A wrapper for `select_all_rows_where`.
    Select the row identified at the column `identifier_name` with the value `row_id`.

        Example:
        >>> # SELECT row WHERE ID == 77
        >>> get_identified_row(path, "ID", "77")
    """
    try:
        return select_all_rows_where(path=path, predicate=lambda r: r[identifier_name] == row_id, encoding=encoding,
                                     delimiter=delimiter, quoting=quoting, quote_character=quote_character,
                                     skip_initial_space=skip_initial_space)[0]
    except IndexError:  # Row was not found
        return None


def write_header(input_reader, *out_writers):
    header = next(input_reader)

    for writer in out_writers:
        writer.writerow(header)


def preprend_column(input_path: str, output_path: str, column: str, encoding: str = "utf8", delimiter: str = ",",
                    line_delimiter: str = None):
    if not is_an_int(column):
        header = next(iter_rows(input_path, encoding=encoding, delimiter=delimiter))
        index_column = header.index(column)
        preprend_column(input_path, output_path, index_column, encoding=encoding, delimiter=delimiter,
                        line_delimiter=line_delimiter)
    else:
        content = [line for line in iter_rows(input_path, encoding=encoding, delimiter=delimiter)]
        with open(output_path, "w", encoding=encoding, newline=line_delimiter) as output_file:
            output_writer = csv.writer(output_file, delimiter=delimiter)
            for line in content:
                line.insert(0, (line.pop(column)))
                output_writer.writerow(line)


def append_column(input_path: str, output_path: str, column: str, encoding: str = "utf8", delimiter: str = ",",
                  line_delimiter: str = None):
    if not is_an_int(column):
        header = next(iter_rows(input_path, encoding=encoding, delimiter=delimiter))
        index_column = header.index(column)
        append_column(input_path, output_path, index_column, encoding=encoding, delimiter=delimiter,
                      line_delimiter=line_delimiter)
    else:
        content = [line for line in iter_rows(input_path, encoding=encoding, delimiter=delimiter)]
        with open(output_path, "w", encoding=encoding, newline=line_delimiter) as output_file:
            output_writer = csv.writer(output_file, delimiter=delimiter)
            for line in content:
                line.append(line.pop(column))
                output_writer.writerow(line)


def find_index_for_class(input_path: str, class_name: str, delimiter: str, quoting: str, quote_char: str,
                         encoding: str = "utf8", skip_initial_space: bool = True) -> int:
    """ Return the column index given a class name for a CSV file containing a header. """
    with open(input_path, encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)
        header = next(reader)

    return header.index(class_name)


def index_in_bounds(input_path: str, index: int, encoding: str = "utf8", delimiter: str = ",") -> bool:
    """ Check if an index is inbound of the CSV file columns. Columns can be accessed with a negative index. """
    length = get_number_of_columns(path=input_path, encoding=encoding, delimiter=delimiter)
    return (-length <= index < 0) or (0 <= index < length)


if __name__ == "__main__":
    pass
