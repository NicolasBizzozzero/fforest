""" A set of tools to split databases into multiple databases.
All the methods postfixed by "2" are methods used to split the database into two other databases (usually a train and a
test database).
This module initialize the file handlers and the readers/writers, then redirect the program to the module corresponding
to the splitting method asked.
"""
import csv
import enum
import os
from typing import Tuple, List

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.core.splitting_methods.halfing import halfing
from ensemble_experimentation.src.core.splitting_methods.halfing import halfing2
from ensemble_experimentation.src.core.splitting_methods.keep_distribution import keep_distribution
from ensemble_experimentation.src.core.splitting_methods.keep_distribution import keep_distribution2
from ensemble_experimentation.src.vrac.file_system import get_filename


class SplittingMethod(enum.IntEnum):
    UNKNOWN = 0
    HALFING = 1
    KEEP_DISTRIBUTION = 2


class UnknownSplittingMethod(Exception):
    def __init__(self, method_name: str):
        Exception.__init__(self, "The splitting method : \"{method_name}\" doesn't"
                                 " exists".format(method_name=method_name))


def str_to_splittingmethod(string: str) -> SplittingMethod:
    """ Convert a String into its respective SplittingMethod enum. """
    string = string.lower()
    if string == "halfing":
        return SplittingMethod.HALFING
    elif string == "keepdistribution":
        return SplittingMethod.KEEP_DISTRIBUTION
    else:
        raise UnknownSplittingMethod(string)


def splittingmethod_to_str(splitting_method: SplittingMethod) -> str:
    """ Convert a SplittingMethod enum into its respective String. """
    if splitting_method == SplittingMethod.HALFING:
        return "halfing"
    elif splitting_method == SplittingMethod.KEEP_DISTRIBUTION:
        return "keepdistribution"
    else:
        return splitting_method.__str__()


def split2(*, input_path: str, delimiter: str, row_limit: int, output_path: str = '.', have_header: bool,
           method: SplittingMethod, output_name_train: str, output_name_test: str, encoding: str, class_name=None,
           number_of_rows: int = None, quoting: int = 1, quotechar: str = "\"",
           skip_initial_space: bool = True) -> Tuple[int, int]:
    """ Open the initial database as input, open the two output databases as output, then give the reader and writers
    to the asked splitting2 method.
    You must pass each argument along with its name.
    """
    with open(input_path, mode="r", encoding=encoding) as input_file,\
            open(os.path.join(output_path, output_name_train), mode='w') as output_train,\
            open(os.path.join(output_path, output_name_test), mode='w') as output_test:

        input_reader = csv.reader(input_file, delimiter=delimiter, quoting=quoting, quotechar=quotechar,
                                  skipinitialspace=skip_initial_space)
        out_writer_train = csv.writer(output_train, delimiter=delimiter, quoting=quoting, quotechar=quotechar,
                                      skipinitialspace=skip_initial_space)
        out_writer_test = csv.writer(output_test, delimiter=delimiter, quoting=quoting, quotechar=quotechar,
                                     skipinitialspace=skip_initial_space)

        if method == SplittingMethod.HALFING:
            size_train, size_test = halfing2(input_reader, row_limit, out_writer_train, out_writer_test)
        elif method == SplittingMethod.KEEP_DISTRIBUTION:
            size_train, size_test = keep_distribution2(input_reader, row_limit, out_writer_train, out_writer_test,
                                                       class_name, number_of_rows)
        else:
            raise UnknownSplittingMethod(splittingmethod_to_str(method))

        return size_train, size_test


def split(*, input_path: str, delimiter: str, row_limit: int, have_header: bool, method: SplittingMethod, encoding: str,
          class_name=None, number_of_rows: int = None, tree_names: list, subtrain_path: str, quoting: int = 1,
          quote_char: str = "\"", skip_initial_space: bool = True) -> List[int]:
    """ Open the initial database as input, open all the other databases as output, then give the reader and writers
    to the asked splitting method.
    You must pass each argument along with its name.
    """
    with open(input_path, mode='r', encoding=encoding) as input_file:
        out_files = [open("{dir_path}/{tree_name}.{extension}".format(dir_path=name,
                                                                      tree_name=get_filename(name),
                                                                      extension=env.arguments[gpn.format_db()]),
                          mode='w') for name in tree_names]

        input_reader = csv.reader(input_file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                                  skipinitialspace=skip_initial_space)
        out_writers = [csv.writer(f, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                                  skipinitialspace=skip_initial_space) for f in out_files]

        if method == SplittingMethod.HALFING:
            databases_size = halfing(input_reader, row_limit, out_writers, env.cleaned_arguments[gpn.trees_in_forest()])
        elif method == SplittingMethod.KEEP_DISTRIBUTION:
            databases_size = keep_distribution(input_reader, row_limit, out_writers,
                                               env.cleaned_arguments[gpn.trees_in_forest()], class_name, number_of_rows)
        else:
            raise UnknownSplittingMethod(splittingmethod_to_str(method))

        # Close all the file handlers
        map(lambda f: f.close(), out_files)

        return databases_size
