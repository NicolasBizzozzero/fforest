from math import floor
from typing import Tuple, List


def halfing(input_reader, row_limit: int, out_writers, number_of_trees: int) -> List[int]:
    """ Splits a CSV file into multiple pieces with the `halfing` method.
    The halfing method slice the database in `number_of_trees` parts, then redistribute them.
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
    """ Splits a CSV file into two pieces with the `halfing` method.
    The halfing method slice the database in two parts, then redistribute one part to the train database, and the other
    to the test database.
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
