""" This module contains all functions related to cleaning command-line arguments parsed by the `docopt` package
(listed as a dependency). It mainly convert string values to their numeric and enum counterpart. If a parameter
requiring an index or a column name has been completed with a name, it change it to its corresponding index. It also
checks if some of the parameters are invalids and raises exceptions accordingly.
"""
import sys

import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.core.learning_process.entropy_measures import str_to_entropy_measure
from ensemble_experimentation.src.core.splitting_methods.split import str_to_splittingmethod, SplittingMethod
from ensemble_experimentation.src.file_tools.csv_tools import find_index_for_class, index_in_bounds, \
    get_number_of_columns
from ensemble_experimentation.src.file_tools.csv_tools import str_to_quoting
from ensemble_experimentation.src.file_tools.format import str_to_format
from ensemble_experimentation.src.vrac.file_system import get_filename
from ensemble_experimentation.src.vrac.maths import is_a_percentage, is_an_int


class MissingClassificationAttribute(Exception):
    def __init__(self):
        Exception.__init__(self, "You need to pass a classification attribute.")


class InvalidPercentage(Exception):
    def __init__(self, percentage: str):
        Exception.__init__(self, "The value \"{percentage}\" is not a percentage.".format(percentage=percentage))


class IndexOutOfBounds(Exception):
    def __init__(self, index: int, length: int, column: str):
        Exception.__init__(self, "The {column} index \"{index}\" can't be used in a "
                                 "database with {length} columns.".format(index=index, length=length, column=column))


class InvalidParameter(Exception):
    def __init__(self, invalid_parameter_name: str):
        Exception.__init__(self, "The \"{param}\" parameter doesn't exists.".format(param=invalid_parameter_name))


def clean_args(args: dict) -> None:
    """ Clean the command-line arguments parsed by the `docopt` package.
    It mainly convert string values to their numeric and enum counterpart. If a parameter requiring an index or a column
    name has been completed with a name, it change it to its corresponding index. It also checks if some of the
    parameters are invalids and raises exceptions accordingly.
    """
    # Rename parameter database
    args[gpn.database()] = args["<" + gpn.database() + ">"]
    del args["<" + gpn.database() + ">"]

    extension = "." + args[gpn.format_output()].lower()

    for param_name in args.keys():
        if param_name == gpn.class_name():
            _check_key_exists(args, param_name, custom_exception=MissingClassificationAttribute)
            _clean_column_index_or_name(args=args, param_name=param_name, column_name="class")
        elif param_name in (gpn.discretization_threshold(), gpn.number_of_tnorms(), gpn.trees_in_forest()):
            args[param_name] = int(args[param_name])
        elif param_name in (gpn.format_input(), gpn.format_output):
            args[param_name] = str_to_format(args[param_name])
        elif param_name == gpn.entropy_measure():
            args[param_name] = str_to_entropy_measure(args[param_name])
        elif param_name == gpn.entropy_threshold():
            if not is_a_percentage(args[param_name]):
                raise InvalidPercentage(args[param_name])
        elif param_name == gpn.identifier():
            if _check_default_value_id(param_name, gdv.identifier()):
                # We must add a column as an identifier. It will be done in the preprocessing function
                args[param_name] = None
            else:
                _clean_column_index_or_name(args=args, param_name=param_name, column_name="identifier")
        elif param_name in (gpn.initial_split_method(), gpn.reference_split_method(), gpn.subsubtrain_split_method()):
            args[param_name] = str_to_splittingmethod(args[param_name])
            if args[param_name] == SplittingMethod.KEEP_DISTRIBUTION and args[gpn.class_name()] is None:
                raise MissingClassificationAttribute()
        elif param_name == gpn.main_directory():
            if args[param_name] is None:
                args[param_name] = get_filename(args[gpn.database()])
        elif param_name == gpn.preprocessed_database_name():
            if args[param_name] is None:
                args[param_name] = _get_preprocessed_db_name(database_name=args[gpn.database()], extension=extension)
            else:
                args[param_name] = get_filename(args[param_name], with_extension=True)
        elif param_name in (gpn.quoting_input(), gpn.quoting_output()):
            args[param_name] = str_to_quoting(args[param_name])
        elif param_name in (gpn.reference_name(), gpn.subtrain_name(), gpn.test_name(), gpn.train_name()):
            args[param_name] = get_filename(args[param_name], with_extension=False) + extension

    from pprint import pprint
    pprint(args)


def _check_key_exists(d: dict, key: object, custom_exception=None) -> None:
    """ Check if a key exists inside a dictionary. Otherwise, raise KeyError or a custom exception. """
    try:
        d[key]
    except KeyError:
        if custom_exception:
            raise custom_exception
        else:
            raise KeyError


def _clean_column_index_or_name(args: dict, param_name: str, column_name: str) -> None:
    """ If the specified name value is a column name, convert it to it's respective index. Otherwise, check if it's
    inbounds and convert it to an integer.
    """
    if (not is_an_int(args[param_name])) and (type(args[param_name]) == str):
        # User asked for a named class, we retrieve its index then change it
        args[param_name] = find_index_for_class(input_path=args[gpn.database()],
                                                class_name=args[gpn.class_name()],
                                                encoding=args[gpn.encoding_input()],
                                                delimiter=args[gpn.delimiter_input()])
    else:
        # User asked for an index, we convert it to int then check if it's inbound
        args[param_name] = int(args[param_name])
        if not index_in_bounds(input_path=args[gpn.database()],
                               index=args[param_name],
                               encoding=args[gpn.encoding_input()],
                               delimiter=args[gpn.delimiter_input()]):
            raise IndexOutOfBounds(index=args[param_name],
                                   column=column_name,
                                   length=get_number_of_columns(path=args[gpn.database()],
                                                                encoding=args[gpn.encoding_input()],
                                                                delimiter=args[gpn.delimiter_input()]))


def _check_default_value_id(id_name: str, default_value: str) -> bool:
    """ Check if the user asked to use as an identifier the same string used for the default identifier string.
    Calling this function prevent the software from overwriting all the identifier values in this specific case.
    """
    if id_name == default_value:
        # Check if the parameter for the identifier has been used
        for option in sys.argv:
            if len(option) > len(id_name) and option[:len(id_name)] == id_name:
                return False  # User asked for the default identifier
        return True           # User didn't asked for an identifier at all
    return False              # User asked for a different identifier than the default


def _get_preprocessed_db_name(database_name: str, extension: str = "") -> str:
    """ Return the name of the modified database given the path of the original database.
        Example:
        >>> _get_preprocessed_db_name("database", "csv")
        '~database.csv'
    """
    return "~" + get_filename(database_name, with_extension=False) + extension
