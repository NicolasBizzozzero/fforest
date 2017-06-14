from math import floor
from typing import Tuple, List


def halfing(input_reader, row_limit: int, out_writers, number_of_trees: int) -> List:
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
    rows_count = [0 for _ in range(number_of_trees)]

    try:
        for row_index, row in enumerate(input_reader):
            writer_index = int(floor((row_index + 1) / row_limit))
            out_writers[writer_index].writerow(row)
            rows_count[writer_index] += 1
    except IndexError:
        pass

    return rows_count


def halfing2(input_reader, row_limit, out_writer_train, out_writer_test) -> Tuple[int, int]:
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
    for row_index, row in enumerate(input_reader):
        if row_index + 1 <= row_limit:
            out_writer_train.writerow(row)
            row_count_train += 1
        else:
            out_writer_test.writerow(row)
            row_count_test += 1

    return row_count_train, row_count_test
