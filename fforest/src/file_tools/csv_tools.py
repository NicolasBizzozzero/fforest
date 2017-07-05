import csv
from typing import Union, List, Iterable, Dict

from fforest.src.vrac.maths import is_an_int
from fforest.src.file_tools.dialect import Dialect


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


def iter_rows(path: str, skip_header: bool, dialect: Dialect) -> iter:
    """ Iterate trough the rows of the file located at `path`. """
    with open(path, encoding=dialect.encoding, newline=dialect.line_delimiter) as csv_file:
        reader = csv.reader(csv_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                            quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)

        if skip_header:
            next(reader)

        for row in reader:
            if row:
                yield row


def iter_rows_dict(path: str, dialect: Dialect) -> Dict:
    """ Iterate trough the rows of the file located at `path` with a csv.DictReader. """
    with open(path, encoding=dialect.encoding, newline=dialect.line_delimiter) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        for row in reader:
            if row:
                yield row


def get_csv_content(path: str, skip_header: bool, dialect: Dialect) -> Iterable[List]:
    """ Get rows from a CSV file. """
    return [row for row in iter_rows(path=path, skip_header=skip_header, dialect=dialect)]


def dump_csv_content(path: str, content: Iterable[List], dialect: Dialect) -> None:
    """ Dump rows into a CSV file. """
    with open(path, "w", encoding=dialect.encoding, newline=dialect.line_delimiter) as output_file:
        output_writer = csv.writer(output_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                   quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        for row in content:
            output_writer.writerow(row)


def get_header(path: str, dialect: Dialect) -> List[str]:
    """ Return the header located in `path`.

        Example :
        >>> get_header("../../test/data/bank.csv", Dialect(delimiter=";"))[:11]
        ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month']
     """
    return next(iter_rows(path=path, skip_header=False, dialect=dialect))


def get_number_of_rows(path: str, dialect: Dialect) -> int:
    """ Return the number of rows, header included, newline at the end excluded, of the file located at `path`.

        Example :
        >>> get_number_of_rows("../../test/data/bank.csv", Dialect(delimiter=";"))
        4522
    """
    number_of_rows = 0
    for row in iter_rows(path=path, skip_header=False, dialect=dialect):
        if row:
            number_of_rows += 1
    return number_of_rows


def get_number_of_columns(path: str, dialect: Dialect) -> int:
    """ Return the number of columns of the file located at `path`.

        Example :
        >>> get_number_of_columns("../../test/data/bank.csv", Dialect(delimiter=";"))
        17
    """
    return len(get_header(path=path, dialect=dialect))


def get_row(path: str, row_number: int, skip_header: bool, dialect: Dialect) -> Union[List, None]:
    """ Return the `row_number`-th row as a list from the file located at `path`.
    The rows are indexed from 1 to len(`path`).
    If a `row_number` is out-of-bound, this function return the `None` value.

        Example :
        >>> get_row("../../test/data/bank.csv", -1, dialect_output=Dialect(delimiter=";")) is None
        True
        >>> get_row("../../test/data/bank.csv", get_number_of_rows("../../test/data/bank.csv",
        ...                                                        Dialect(delimiter=";")) + 1,
        ...                                     dialect_output=Dialect(delimiter=";")) is None
        True
        >>> get_row("../../test/data/bank.csv", 77, dialect_output=Dialect(delimiter=";"))[:14]
        [54.0, 'management', 'divorced', 'tertiary', 'no', 3222.0, 'no', 'no', 'cellular', 14.0, 'aug', 67.0, 2.0, -1.0]
    """
    if row_number <= 0:
        return None

    current_row = 0
    for row in iter_rows(path=path, skip_header=skip_header, dialect=dialect):
        current_row += 1
        if current_row == row_number:
            return row


def get_column(path: str, column: Union[str, int], have_header: bool, dialect: Dialect) -> List:
    """ Get a column from the CSV database with its index or its name. Remove the header if it's present. """
    if not ((type(column) == int) or ((type(column) == str) and have_header)):
        raise NamedAttributeButNoHeader()
    return [row[column] for row in iter_rows(path=path, skip_header=have_header, dialect=dialect) if row]


def get_columns(path: str, columns: List[Union[str, int]], have_header: bool, dialect: Dialect) -> List:
    """ Get columns from the CSV database with their index or their name. Remove the header if it's present. """
    cleaned_columns = list()
    for class_name in columns:
        if type(class_name) == str:
            if not have_header:
                raise NamedAttributeButNoHeader()
            else:
                cleaned_columns.append(find_index_with_class(path=path, class_name=class_name, dialect=dialect))
        else:
            cleaned_columns.append(class_name)

    return [[row[column] for column in columns] for row in iter_rows(path=path, skip_header=have_header,
                                                                     dialect=dialect) if row]


def select_all_rows_where(path: str, predicate: callable, dialect: Dialect) -> list:
    """ Return all rows from the CSV file at `path` with which the `predicate` return True.
    The rows are casted as a dictionary.

        Example:
            >>> # SELECT all rows WHERE age > 25
            >>> select_all_rows_where(path, lambda r: r["age"] > 25)

            >>> # SELECT all rows WHERE money < 1000 AND city == 'Paris'
            >>> select_all_rows_where(path, lambda r: r["money"] < 1000 and r["city"] == "Paris")
    """
    with open(path, encoding=dialect.encoding, newline=dialect.line_delimiter) as file:
        return [row for row in csv.DictReader(file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                              quotechar=dialect.quote_char,
                                              skipinitialspace=dialect.skip_initial_space) if predicate(row)]


def get_identified_row(path: str, identifier_name: str, row_id: str, dialect: Dialect) -> Union[Dict, None]:
    """ A wrapper for `select_all_rows_where`.
    Select the row identified at the column `identifier_name` with the value `row_id`.

        Example:
        >>> # SELECT row WHERE ID == 77
        >>> get_identified_row(path, "ID", "77")
    """
    try:
        return select_all_rows_where(path=path, predicate=lambda r: r[identifier_name] == row_id, dialect=dialect)[0]
    except IndexError:  # Row was not found
        return None


def preprend_column(input_path: str, output_path: str, column: Union[str, int], dialect: Dialect) -> None:
    """ Prepend a column into input_path, then dump the result file into output_path. """
    if not is_an_int(column):
        index_column = find_index_with_class(path=input_path, class_name=column, dialect=dialect)
        preprend_column(input_path, output_path, index_column, dialect)
    else:
        content = get_csv_content(path=input_path, skip_header=False, dialect=dialect)
        # Move the column at the beginning
        for line in content:
            line.insert(0, (line.pop(column)))
        dump_csv_content(path=output_path, content=content, dialect=dialect)


def append_column(input_path: str, output_path: str, column: Union[str, int], dialect: Dialect) -> None:
    """ Append a column into input_path, then dump the result file into output_path. """
    if not is_an_int(column):
        index_column = find_index_with_class(path=input_path, class_name=column, dialect=dialect)
        append_column(input_path, output_path, index_column, dialect)
    else:
        content = get_csv_content(path=input_path, skip_header=False, dialect=dialect)
        # Move the column at the beginning
        for line in content:
            line.append(line.pop(column))
        dump_csv_content(path=output_path, content=content, dialect=dialect)


def find_index_with_class(path: str, class_name: str, dialect: Dialect) -> int:
    """ Return the column index given a class name for a CSV file containing a header. """
    return get_header(path=path, dialect=dialect).index(class_name)


def index_in_bounds(input_path: str, index: int, dialect: Dialect) -> bool:
    """ Check if an index is inbound of the CSV file columns. Columns can be accessed with a negative index. """
    length = get_number_of_columns(path=input_path, dialect=dialect)
    return (-length <= index < 0) or (0 <= index < length)


if __name__ == "__main__":
    pass
