import csv


def iter_rows(filepath: str) -> iter:
    """ Iterate trough the rows of the file located at `filepath`. """
    with open(filepath) as csv_file:
        content = csv.reader(csv_file)
        for line in content:
            yield line


def get_number_of_rows(filepath: str) -> int:
    """ Return the number of rows of the file located at `filepath`. """
    with open(filepath) as csv_file:
        return len(list(csv.reader(csv_file))) - 1


def get_row(filepath: str, row_number: int) -> list:
    """ Return the `row_number`-th row as a list from the file located at `filepath`.
    The rows are indexed from 1 to len(`filepath`).
    If a `row_number` is out-of-bound, this function return the `None` value.
    """
    if row_number <= 0 or row_number > get_number_of_rows(filepath):
        return None

    current_row = 0
    for row in iter_rows(filepath):
        current_row += 1
        if current_row == row_number:
            return row


def select_all_rows_where(filepath: str, predicate: callable) -> list:
    """ Return all rows from the CSV file at `filepath` with which the `predicate` return True.
    The rows are casted as a dictionary.

        Example:
            >>> # SELECT all rows WHERE age > 25
            >>> select_all_rows_where(filepath, lambda r: r["age"] > 25)

            >>> # SELECT all rows WHERE money < 1000 AND city == 'Paris'
            >>> select_all_rows_where(filepath, lambda r: r["money"] < 1000 and r["city"] == "Paris")
    """
    with open(filepath) as csv_file:
        return [row for row in csv.DictReader(csv_file) if predicate(row)]


def get_identified_row(filepath: str, identifier_name: str, row_id: int):
    """ A wrapper for `select_all_rows_where`.
    Select the row identified at the column `identifier_name` with the value `row_id`.
    """
    return select_all_rows_where(filepath, lambda r: r[identifier_name] == row_id)[0]


def write_header(input_reader, *out_writers):
    header = next(input_reader)

    for writer in out_writers:
        writer.writerow(header)
