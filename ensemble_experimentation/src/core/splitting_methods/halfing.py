import csv
import os
from typing import Tuple


def halfing(*, filepath: str, delimiter: str = ',', row_limit: int, output_name_template: str = 'output_%s.csv',
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
            >> halfing(filepath='input.csv', row_limit=100, output_name_template="out_%s.csv"));
    """
    # Set the outputs' writer
    current_out_path = os.path.join(output_path, output_name_template % 1)
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)

    with open(filepath) as input_file:
        content = csv.reader(input_file, delimiter=delimiter)
        current_piece = 1
        current_limit = row_limit

        # Store the header and write it once
        if keep_headers:
            headers = next(content)
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


def halfing2(content, row_limit, out_writer_train, out_writer_test) -> Tuple[int, int]:
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
            >> halfing2(filepath='input.csv', row_limit=100, output_name1="train.csv", output_name1="test.csv"));
    """
    row_count_train, row_count_test = 0, 0
    for row_index, row in enumerate(content):
        if row_index + 1 <= row_limit:
            out_writer_train.writerow(row)
            row_count_train += 1
        else:
            out_writer_test.writerow(row)
            row_count_test += 1

    return row_count_train, row_count_test