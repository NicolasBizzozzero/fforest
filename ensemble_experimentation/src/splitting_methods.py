"""A set of tools to split databases into multiple databases.
All the methods postfixed by "2" are methods used to split the database into two other databases (usually a train and a
test database).
"""
import csv
import os
import enum
from ensemble_experimentation.src.exceptions import UnknownSplittingMethod


class SplittingMethod(enum.IntEnum):
    HALFING = 0
    KEEP_DISTRIBUTION = 1


def split2(*, filepath: str, delimiter: str, row_limit: int, output_path: str = '.', have_header: bool,
           method: SplittingMethod, output_name_train: str, output_name_test: str, encoding: str):
    """ Open the initial database as input, open the two output databases as output, then give the reader and writers
    to the asked splitting method.
    """
    with open(filepath, encoding=encoding) as input_file,\
         open(os.path.join(output_path, output_name_train), 'w', encoding=encoding) as output_train,\
         open(os.path.join(output_path, output_name_test), 'w', encoding=encoding) as output_test:
        input_reader = csv.reader(input_file, delimiter=delimiter)
        out_writer_train = csv.writer(output_train, delimiter=delimiter)
        out_writer_test = csv.writer(output_test, delimiter=delimiter)

        # Write the headers if asked to
        if have_header:
            header = next(input_reader)
            out_writer_train.writerow(header)
            out_writer_test.writerow(header)

        # Then split the file
        splitting_method = _smenum_to_function(method=method, is2=True)
        splitting_method(input_reader, row_limit, out_writer_train, out_writer_test)


def split():
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


def halfing2(content, row_limit, out_writer_train, out_writer_test):
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
    for row_index, row in enumerate(content):
        if row_index + 1 <= row_limit:
            out_writer_train.writerow(row)
        else:
            out_writer_test.writerow(row)


def keep_distribution():
    pass


# TODO: Ouvrir en lecture avec un DictReader pour savoir quel argument se trouve ou
# TODO: Passer ensuite le nom de la colonne de classe OU son numero
def keep_distribution2(content, row_limit, out_writer_train, out_writer_test):
    # We store rows into the distribution dictionary
    distribution_dictionary = dict()
    for row in content:
        if row[TRUC] in distribution_dictionary:
            distribution_dictionary[row[TRUC]].append(row)
        else:
            distribution_dictionary[row[TRUC]] = [row]

    # Then we distribute the rows proportionally


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
