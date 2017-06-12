"""A set of tools to split databases into multiple databases.
All the methods postfixed by "2" are methods used to split the database into two other databases (usually a train and a
test database).
"""
import csv
import os
import enum
import itertools
from typing import Tuple

from ensemble_experimentation.src.exceptions import UnknownSplittingMethod
from ensemble_experimentation.src.csv_tools import write_header
from ensemble_experimentation.src.vrac import is_an_int
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_statistic_name as gsn


class SplittingMethod(enum.IntEnum):
    HALFING = 0
    KEEP_DISTRIBUTION = 1


def split2(*, filepath: str, delimiter: str, row_limit: int, output_path: str = '.', have_header: bool,
           method: SplittingMethod, output_name_train: str, output_name_test: str, encoding: str, class_name=None,
           number_of_rows: int = None) -> Tuple[int, int]:
    """ Open the initial database as input, open the two output databases as output, then give the reader and writers
    to the asked splitting2 method.
    """
    with open(filepath, encoding=encoding) as input_file,\
         open(os.path.join(output_path, output_name_train), 'w', encoding=encoding) as output_train,\
         open(os.path.join(output_path, output_name_test), 'w', encoding=encoding) as output_test:
        out_writer_train = csv.writer(output_train, delimiter=delimiter)
        out_writer_test = csv.writer(output_test, delimiter=delimiter)

        if method == SplittingMethod.HALFING:
            input_reader = csv.reader(input_file, delimiter=delimiter)

            # Write the headers if asked to
            if have_header:
                write_header(input_reader, out_writer_train, out_writer_test)

            size_train, size_test = halfing2(input_reader, row_limit, out_writer_train, out_writer_test)
        elif method == SplittingMethod.KEEP_DISTRIBUTION:
            if is_an_int(class_name):
                input_reader = csv.reader(input_file, delimiter=delimiter)
            else:
                input_reader = csv.DictReader(input_file, delimiter=delimiter)

            # Write the headers if asked to
            if have_header:
                write_header(input_reader, out_writer_train, out_writer_test)

            size_train, size_test = keep_distribution2(input_reader, row_limit, out_writer_train, out_writer_test, class_name, number_of_rows)

    return size_train, size_test

def split():
    """ Open the initial database as input, open all the other databases as output, then give the reader and writers
    to the asked splitting method.
    """
    pass


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


def keep_distribution():
    pass


def keep_distribution2(content, row_limit, out_writer_train, out_writer_test, class_name, number_of_rows: int) ->\
        Tuple[int, int]:
    row_count_train, row_count_test = 0, 0
    # We store rows into the distribution dictionary
    distribution_dictionary = dict()

    if is_an_int(class_name):
        class_name = int(class_name)
    for row in content:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_train = row_limit / number_of_rows
    # If the class name is an index
    if isinstance(class_name, int):
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0))

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row)
                row_count_test += 1
    # If it's a name
    else:
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0).values())

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row.values())
                row_count_test += 1

    return row_count_train, row_count_test


def _smenum_to_function(method: SplittingMethod, is2: bool) -> callable:
    """ Convert a SplittingMethod enum into its respective function. """
    if method == SplittingMethod.HALFING:
        if is2:
            return halfing2
        return halfing
    elif method == SplittingMethod.KEEP_DISTRIBUTION:
        if is2:
            return keep_distribution2
        return keep_distribution


def _str_to_smenum(string: str) -> SplittingMethod:
    """ Convert a String into its respective SplittingMethod enum. """
    if string == "halfing":
        return SplittingMethod.HALFING
    elif string == "keepdistribution":
        return SplittingMethod.KEEP_DISTRIBUTION
    else:
        raise UnknownSplittingMethod("The splitting method : \"" + string + "\" doesn't exists")
