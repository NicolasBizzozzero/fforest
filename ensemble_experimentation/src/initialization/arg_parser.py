""" This module contains all functions related to parsing command-line arguments for all entry points of the package.
It uses the `docopt` package (listed as a dependencie) to easily combine the tedious task of writing documentation
and parsing arguments.
"""
import sys

import docopt
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_statistic_name as gsn
import ensemble_experimentation.src.getters.get_parameter_documentation as gpd
import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.exceptions import InvalidValue, MissingClassificationAttribute
from ensemble_experimentation.src.vrac import is_a_percentage, get_filename
from ensemble_experimentation.src.csv_tools import get_number_of_rows
from ensemble_experimentation.src.splitting_methods import _str_to_smenum, SplittingMethod
import os
import copy


_FORMAT_DICTIONARY = dict(
    # Documentation
    doc_usage=gpd.usage(),

    # Parameters
    param_database=gpn.database(),
    param_training_value=gpn.training_value(),
    param_reference_value=gpn.reference_value(),
    param_trees_in_forest=gpn.trees_in_forest(),
    param_initial_split_method=gpn.initial_split_method(),
    param_reference_split_method=gpn.reference_split_method(),
    param_train_name=gpn.train_name(),
    param_test_name=gpn.test_name(),
    param_preprocessed_db_name=gpn.preprocessed_database_name(),
    #TODO: JEN SUIS ICI
    param_identificator=gpn.identifier(),
    param_encoding=gpn.encoding(),
    param_format_db=gpn.format_db(),
    param_delimiter=gpn.delimiter(),
    param_have_header=gpn.have_header(),
    param_class_name=gpn.class_name(),
    param_main_directory=gpn.main_directory(),

    # Default values
    default_identificator=gdv.identifier(),
    default_encoding=gdv.encoding(),
    default_training_value=gdv.training_value(),
    default_format_db=gdv.format_db(),
    default_reference_value=gdv.reference_value(),
    default_delimiter=gdv.delimiter(),
    default_have_header=gdv.have_header(),
    default_initial_split_train_name=gdv.train_name(),
    default_initial_split_test_name=gdv.test_name(),
    default_initial_split_method=gdv.initial_split_method(),
    default_reference_split_method=gdv.reference_split_method(),

    # Miscellaneous
    global_name=ggv.name()
)


def _check_add_id(args: dict) -> bool:
    """Check if the user asked to use as an identificator the same string as the default identificator string.
    If this function is not called, the program will overwrite all the identificator values in this specific case.
    """
    id_name = gpn.identifier()
    if args[id_name] == gdv.identifier():
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


def _clean_args(args: dict) -> dict:
    """ Clean the arguments to make the `args` dictionary usable more easily. """
    cleaned_args = copy.copy(args)

    # Class name
    try:
        cleaned_args[gpn.class_name()]
    except KeyError:
        cleaned_args[gpn.class_name()] = None

    # Have header
    if cleaned_args[gpn.have_header()] == "0":
        cleaned_args[gpn.have_header()] = False
    else:
        cleaned_args[gpn.have_header()] = True

    # ID
    if _check_add_id(cleaned_args):
        # We must add a column as identificator
        cleaned_args[gpn.identifier()] = None

    # Initial split Method
    cleaned_args[gpn.initial_split_method()] = _str_to_smenum(cleaned_args[gpn.initial_split_method()])
    if cleaned_args[gpn.initial_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute("You need to pass a classification attribute for this splitting method")

    # Reference split Method
    cleaned_args[gpn.reference_split_method()] = _str_to_smenum(cleaned_args[gpn.reference_split_method()])
    if cleaned_args[gpn.reference_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute("You need to pass a classification attribute for this splitting method")

    # Rename parameter database
    cleaned_args["{param_database}".format(**_FORMAT_DICTIONARY)] = cleaned_args["<{param_database}>".format(**_FORMAT_DICTIONARY)]
    del cleaned_args["<{param_database}>".format(**_FORMAT_DICTIONARY)]

    # Main directory
    if cleaned_args[gpn.main_directory()] is None:
        cleaned_args[gpn.main_directory()] = get_filename(cleaned_args[gpn.database()])

    # Initial split test database name
    cleaned_args[gpn.test_name()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.test_name()] + "." + cleaned_args[gpn.format_db()]

    # Initial split train database name
    #TODO: I don't know why, but docopt can't parse the default value
    if cleaned_args[gpn.train_name()] is None:
        cleaned_args[gpn.train_name()] = cleaned_args[gpn.main_directory()] + "/" + gdv.train_name() + "." + cleaned_args[gpn.format_db()]
    else:
        cleaned_args[gpn.train_name()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.train_name()] + "." + cleaned_args[gpn.format_db()]

    # Default modified database name
    try:
        cleaned_args[gpn.preprocessed_database_name()]
    except KeyError:
        cleaned_args[gpn.preprocessed_database_name()] = cleaned_args[gpn.main_directory()] + "/" + _get_modified_db_name(cleaned_args)

    # Training value
    cleaned_args[ggv.number_of_rows()] = get_number_of_rows(cleaned_args[gpn.database()])
    cleaned_args[gpn.training_value()] = _convert_row_limit(cleaned_args[gpn.training_value()],
                                                            cleaned_args[ggv.number_of_rows()])

    # Add statistics
    ggv.statistics[gsn.database_path()] = cleaned_args[gpn.database()]
    ggv.statistics[gsn.database_name()] = get_filename(cleaned_args[gpn.database()])
    ggv.statistics[gsn.preprocessed_database_path()] = cleaned_args[gpn.preprocessed_database_name()]
    ggv.statistics[gsn.train_path()] = cleaned_args[gpn.train_name()]
    ggv.statistics[gsn.test_path()] = cleaned_args[gpn.test_name()]
    ggv.statistics[gsn.instances_in_database()] = cleaned_args[ggv.number_of_rows()]

    return cleaned_args


def parse_args_main_entry_point() -> None:
    global _FORMAT_DICTIONARY

    documentation = """{global_name}

Usage:
  {doc_usage}

Options:
  # Splitting values
  {param_training_value}=<value>            {doc_training_value}
  {param_reference_value}=<value>           {doc_reference_value}
  {param_trees_in_forest}=<value>           {doc_trees_in_forest}

  # Splitting methods
  {param_initial_split_method}=<method>     {doc_initial_split_method}
  {param_reference_split_method}=<method>   {doc_reference_split_method}

  # File names
  {param_train_name}=<name>                 {doc_train_name}
  {param_test_name}=<name>                  {doc_test_name}
  {param_preprocessed_db_name}=<name>       {doc_preprocessed_db}
  {param_subtrain_name}=<name>              {doc_subtrain_name}
  {param_reference_name}=<name>             {doc_reference_name}
  {param_subsubtrain_name_pattern}=<name>   {doc_subsubtrain_name_pattern}
  {param_statistics_name}=<name>            {doc_statistics_name}
  {param_tree_file_extension}=<name>        {doc_tree_file_extension}
  {param_vector_file_extension}=<name>      {doc_vector_file_extension}

  # Directories names
  {param_main_directory}=<name>             {doc_main_directory}
  {param_subtrain_directory}=<name>         {doc_subtrain_directory}
  {param_subsubtrain_directory_pattern}=<name> {doc_subsubtrain_directory_pattern}

  # Miscellaneous
  {param_help}                              {doc_help}
  {param_identifier}=<ID>                   {doc_identifier}
  {param_encoding}=<encoding>               {doc_encoding}
  {param_format_db}=<format>                {doc_format_db}
  {param_delimiter}=<char>                  {doc_delimiter}
  {param_have_header}                       {doc_have_header}
  {param_class_name}=<name>                 {doc_class_name}
""".format(**_FORMAT_DICTIONARY)

    arguments = docopt.docopt(documentation, version=ggv.version(), help=True)
    cleaned_arguments = _clean_args(arguments)

    env.arguments = arguments
    env.cleaned_arguments = cleaned_arguments


def parse_args_forest_entry_point() -> dict:
    pass


def parse_args_forest_reduction_entry_point() -> dict:
    pass


if __name__ == "__main__":
    pass
