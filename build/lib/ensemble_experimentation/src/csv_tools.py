import os
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


def split(*, filepath: str, delimiter: str = ',', row_limit: int, output_name_template: str = 'output_%s.csv',
          output_path: str = '.', keep_headers: bool = True):
    """Splits a CSV file into multiple pieces.
        You must pass each argument along with its name.

        Inspired by :
        https://gist.github.com/jrivero/1085501

        Arguments:
            `row_limit`: The number of rows you want in each output file.
            `output_name_template`: A %s-style template for the numbered output files.
            `output_path`: Where to stick the output files.
            `keep_headers`: Whether or not to print the headers in each output file.
        Example:
            >> split(filepath='input.csv', row_limit=100, output_name_template="out_%s.csv"));
    """
    # Set the outputs' writer
    current_out_path = os.path.join(output_path, output_name_template % 1)
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)

    with open(filepath) as file:
        content = csv.reader(file, delimiter=delimiter)
        current_piece = 1
        current_limit = row_limit

        # Set the writer to keep headers for each output
        if keep_headers:
            headers = content.next()
            current_out_writer.writerow(headers)

        for row_index, row in enumerate(content):
            if row_index + 1 > current_limit:
                current_piece += 1
                current_limit = row_limit * current_piece
                current_out_path = os.path.join(output_path, output_name_template % current_piece)
                current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
                if keep_headers:
                    current_out_writer.writerow(headers)
            current_out_writer.writerow(row)


def halfing(*, filepath: str, delimiter: str = ',', row_limit: int, output_name1: str = 'train_data.csv',
            output_name2: str = 'test_data.csv', output_path: str = '.', keep_headers: bool = True):
    """Splits a CSV file into two pieces.
        You must pass each argument along with its name.

        Inspired by :
        https://gist.github.com/jrivero/1085501

        Arguments:
            `row_limit`: The number of rows you want to put in the first output file.
            `output_name_template`: A %s-style template for the numbered output files.
            `output_path`: Where to stick the output files.
            `keep_headers`: Whether or not to print the headers in each output file.
        Example:
            >> halfing(filepath='input.csv', row_limit=100, output_name1="train.csv", output_name1="test.csv"));
    """
    # Set the outputs' writer
    out_writer1 = csv.writer(open(os.path.join(output_path, output_name1), 'w'), delimiter=delimiter)
    out_writer2 = csv.writer(open(os.path.join(output_path, output_name2), 'w'), delimiter=delimiter)

    with open(filepath) as file:
        content = csv.reader(file, delimiter=delimiter)

        # Write the headers if asked to
        if keep_headers:
            headers = content.next()
            out_writer1.writerow(headers)
            out_writer2.writerow(headers)

        for row_index, row in enumerate(content):
            if row_index + 1 <= row_limit:
                out_writer1.writerow(row)
            else:
                out_writer2.writerow(row)
