""" This module contains all functions related to parsing command-line arguments for all entry points of the package.
It uses the `docopt` package (listed as a dependencie) to easily combine the tedious task of writing documentation
and parsing arguments.
#TODO: Instead of writing all documentation line for each parameter, we should store all lines in a separate file to
#TODO: make it consistent between all entry points.
"""
import sys
import docopt
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv
from ensemble_experimentation.src.exceptions import InvalidValue
from ensemble_experimentation.src.vrac import is_a_percentage
from ensemble_experimentation.src.csv_tools import get_number_of_rows
from ensemble_experimentation.src.splitting_methods import _str_to_smenum
import os


_FORMAT_DICTIONARY = dict(
    # Parameters
    param_database=gpn.database(),
    param_training_value=gpn.training_value(),
    param_trees_in_forest=gpn.trees_in_forest(),
    param_reference_value=gpn.reference_value(),
    param_identificator=gpn.identificator(),
    param_encoding=gpn.encoding(),
    param_format_db=gpn.format_db(),
    param_delimiter=gpn.delimiter(),
    param_have_header=gpn.have_header(),
    param_initial_split_train_name=gpn.initial_split_train_name(),
    param_initial_split_test_name=gpn.initial_split_test_name(),
    param_initial_split_method=gpn.initial_split_method(),
    param_modified_database_name=gpn.modified_database_name(),

    # Default values
    default_identificator=gdv.identificator(),
    default_encoding=gdv.encoding(),
    default_training_value=gdv.training_value(),
    default_format_db=gdv.format_db(),
    default_reference_value=gdv.reference_value(),
    default_delimiter=gdv.delimiter(),
    default_have_header=gdv.have_header(),
    default_initial_split_train_name=gdv.initial_split_train_name(),
    default_initial_split_test_name=gdv.initial_split_test_name(),
    default_initial_split_method=gdv.initial_split_method(),

    # Global variables
    global_name=ggv.name()
)


def _check_add_id(args: dict) -> bool:
    """Check if the user asked to use as an identificator the same string as the default identificator string.
    If this function is not called, the program will overwrite all the identificator values in this specific case.
    """
    id_name = gpn.identificator()
    if args[id_name] == gdv.identificator():
        # Check if the parameter for the identificator has been used
        for option in sys.argv:
            if len(option) > len(id_name) and option[:len(id_name)] == id_name:
                return False  # User asked for the default identificator
        return True           # User didn't asked for an identificator at all
    return False              # User asked for a different identificator than the default


def _convert_row_limit(row_limit: str, number_of_rows: int) -> int:
    """ Convert the parsed `row_limit` to a number of rows if it's a percentage, or return it if it's already a number
    of rows.

        Example :
        >>> _convert_row_limit("0.5", 1000)
        500
        >>> _convert_row_limit("500", 1000)
        500
        >>> _convert_row_limit("500.1", 1000)
        InvalidValue: The value "500.1" is neither a percentage nor a number of rows.
    """
    if not is_a_percentage(row_limit):
        raise InvalidValue("The value \"" + row_limit + "\" is neither a percentage nor a number of rows.")
    percentage = float(row_limit)
    return int(round(percentage * number_of_rows))


def _get_modified_db_name(args: dict) -> str:
    """ Return the name of the modified database given the path of the original database. """
    return "~" + os.path.split(args[gpn.database()])[1]


def _clean_args(args: dict) -> None:
    """ Clean the arguments to make the `args` dictionary usable more easily. """
    # Have header
    if args[gpn.have_header()] == "0":
        args[gpn.have_header()] = False
    else:
        args[gpn.have_header()] = True

    # ID
    if _check_add_id(args):
        # We must add a column as identificator
        args[gpn.identificator()] = None

    # Initial split Method
    args[gpn.initial_split_method()] = _str_to_smenum(args[gpn.initial_split_method()])

    # Initial split test database name
    args[gpn.initial_split_test_name()] += "." + args[gpn.format_db()]

    # Initial split train database name
    #TODO: I don't know why, but docopt can't parse the default value
    if args[gpn.initial_split_train_name()] is None:
        args[gpn.initial_split_train_name()] = gdv.initial_split_train_name() + "." + args[gpn.format_db()]

    # Rename parameter database
    args["{param_database}".format(**_FORMAT_DICTIONARY)] = args["<{param_database}>".format(**_FORMAT_DICTIONARY)]
    del args["<{param_database}>".format(**_FORMAT_DICTIONARY)]

    # Default modified database name
    try:
        args[gpn.modified_database_name()]
    except KeyError:
        args[gpn.modified_database_name()] = _get_modified_db_name(args)

    # Training value
    args[gpn.training_value()] = _convert_row_limit(args[gpn.training_value()],
                                                    get_number_of_rows(args[gpn.database()]))


def parse_args_main_entry_point() -> dict:
    global _FORMAT_DICTIONARY

    documentation = """{global_name}

Usage:
  ensemble_experimentation.py <{param_database}> [{param_training_value} <training_value>] [{param_trees_in_forest} <trees_in_forest>] [{param_reference_value} <reference_value>] [{param_identificator} <ID>] [{param_encoding} <encoding>] [{param_format_db} <format>] [{param_delimiter} <delimiter>] [{param_have_header} <have_header>] [{param_initial_split_train_name} <initial_split_train_name>] [{param_initial_split_test_name} <initial_split_test_name>] [{param_initial_split_method} <initial_split_method>]

Options:
  -h --help                           Print this help message.
  {param_identificator}=<STR>                           The class name of the examples' identifier [default: {default_identificator}].
  {param_encoding}=<SRE>               The encoding used to read the database and write the outputs. [default: {default_encoding}]
  {param_training_value}=<NUMBER>   % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_training_value}].
  {param_trees_in_forest}=<INT> Number of trees in to create in the base forest.
  {param_format_db}=<STR>                   The format used to read the database and write the outputs. [default: {default_format_db}]
  {param_reference_value}=<NUMBER>       % of the values you want to extract from the training set and put in the reference set. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_reference_value}].
  {param_delimiter}=<CHAR>             The symbol used to delimiting data in CSV database. [default: {default_delimiter}]
  {param_have_header}=<BOOL>         Set this boolean to 1 if your database have a header, or 0 otherwise. [default: {default_have_header}]
  {param_initial_split_train_name}=<STR> The name of the training database after the initial split. [default: {default_initial_split_train_name}]
  {param_initial_split_test_name}=<STR>   The name of the testing database after the initial split. [default: {default_initial_split_test_name}]
  {param_initial_split_method}=<METHOD>         The method to use with the initial split of the database. Values can be `halfing` or `keepdistribution` [default: {default_initial_split_method}]
  {param_modified_database_name}=<STR>                      The name of the modified original database. Its defaulting to the database name prefixed with '~'.
""".format(**_FORMAT_DICTIONARY)

    args = docopt.docopt(documentation, version=ggv.version(), help=True)
    _clean_args(args)
    return args


def parse_args_forest_entry_point() -> dict:
    pass


def parse_args_forest_reduction_entry_point() -> dict:
    pass


if __name__ == "__main__":
    pass
