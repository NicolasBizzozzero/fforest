""" This module contains all functions related to parsing command-line arguments for all entry points of the package.
It uses the `docopt` package (listed as a dependencie) to easily combine the tedious task of writing documentation
and parsing arguments.
#TODO: We can gain time wy not formatting the helping message twice, but by directly formatting the documentation from
#      the format dictionary
"""
import copy
import sys

import docopt

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_parameter_documentation as gpd
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.splitting_methods.splitting_methods import str_to_splittingmethod,\
    SplittingMethod
from ensemble_experimentation.src.exceptions import InvalidValue, MissingClassificationAttribute
from ensemble_experimentation.src.file_tools.csv_tools import get_number_of_rows
from ensemble_experimentation.src.file_tools.format import str_to_format
from ensemble_experimentation.src.vrac import is_a_percentage, get_filename

_FORMAT_DICTIONARY = dict(
    # Documentation
    doc_usage=gpd.usage(),
    doc_training_value=gpd.training_value(),
    doc_reference_value=gpd.reference_value(),
    doc_trees_in_forest=gpd.trees_in_forest(),
    doc_initial_split_method=gpd.initial_split_method(),
    doc_reference_split_method=gpd.reference_split_method(),
    doc_train_name=gpd.train_name(),
    doc_test_name=gpd.test_name(),
    doc_preprocessed_db_name=gpd.preprocessed_database_name(),
    doc_subtrain_name=gpd.subtrain_name(),
    doc_reference_name=gpd.reference_name(),
    doc_subsubtrain_name_pattern=gpd.subsubtrain_name_pattern(),
    doc_statistics_name=gpd.statistics_file_name(),
    doc_tree_file_extension=gpd.tree_file_extension(),
    doc_vector_file_extension=gpd.vector_file_extension(),
    doc_main_directory=gpd.main_directory(),
    doc_subtrain_directory=gpd.subtrain_directory(),
    doc_subsubtrain_directory_pattern=gpd.subsubtrain_directory_pattern(),
    doc_help=gpd.help_doc(),
    doc_identifier=gpd.identifier(),
    doc_encoding=gpd.encoding(),
    doc_format_db=gpd.format_db(),
    doc_delimiter=gpd.delimiter(),
    doc_have_header=gpd.have_header(),
    doc_class_name=gpd.class_name(),

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
    param_subtrain_name=gpn.subtrain_name(),
    param_reference_name=gpn.reference_name(),
    param_subsubtrain_name_pattern=gpn.subsubtrain_name_pattern(),
    param_statistics_name=gpn.statistics_file_name(),
    param_tree_file_extension=gpn.tree_file_extension(),
    param_vector_file_extension=gpn.vector_file_extension(),
    param_main_directory=gpn.main_directory(),
    param_subtrain_directory=gpn.subtrain_directory(),
    param_subsubtrain_directory_pattern=gpn.subsubtrain_directory_pattern(),
    param_help=gpn.help_param(),
    param_identifier=gpn.identifier(),
    param_encoding=gpn.encoding(),
    param_format_db=gpn.format_db(),
    param_delimiter=gpn.delimiter(),
    param_have_header=gpn.have_header(),
    param_class_name=gpn.class_name(),

    # Default values
    default_training_value=gdv.training_value(),
    default_reference_value=gdv.reference_value(),
    default_trees_in_forest=gdv.trees_in_forest(),
    default_initial_split_method=gdv.initial_split_method(),
    default_reference_split_method=gdv.reference_split_method(),
    default_subsubtrain_split_method=gdv.subsubtrain_split_method(),
    default_train_name=gdv.train_name(),
    default_test_name=gdv.test_name(),
    default_subtrain_name=gdv.subtrain_name(),
    default_reference_name=gdv.reference_name(),
    default_subsubtrain_name_pattern=gdv.subsubtrain_name_pattern(),
    default_statistics_name=gdv.statistics_file_name(),
    default_tree_file_extension=gdv.tree_file_extension(),
    default_vector_file_extension=gdv.vector_file_extension(),
    default_subtrain_directory=gdv.subtrain_directory(),
    default_subsubtrain_directory_pattern=gdv.subsubtrain_directory_pattern(),
    default_identifier=gdv.identifier(),
    default_encoding=gdv.encoding(),
    default_format_db=gdv.format_db(),
    default_delimiter=gdv.delimiter(),

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
        raise InvalidValue(row_limit)
    percentage = float(row_limit)
    return int(round(percentage * number_of_rows))


def _get_preprocessed_db_name(args: dict, extension: str = "") -> str:
    """ Return the name of the modified database given the path of the original database. """
    return "~" + get_filename(args[gpn.database()], with_extension=False) + extension


def _clean_args(args: dict) -> dict:
    """ Clean the arguments to make the `args` dictionary usable more easily.
    This mainly consist of converting strings to int, float or enum.
    """
    cleaned_args = copy.copy(args)

    # Rename parameter database
    cleaned_args[gpn.database()] = cleaned_args["<" + gpn.database() + ">"]
    del cleaned_args["<" + gpn.database() + ">"]

    # Count instances in initial database
    env.statistics[gsn.instances_in_database()] = get_number_of_rows(cleaned_args[gpn.database()])

    # Class name
    try:
        args[gpn.class_name()]
    except KeyError:
        cleaned_args[gpn.class_name()] = None

    # Delimiter

    # Encoding

    # Format
    cleaned_args[gpn.format_db()] = str_to_format(args[gpn.format_db()])
    extension = "." + args[gpn.format_db()].lower()

    # Have header

    # Help

    # ID
    if _check_add_id(args):
        # We must add a column as an identifier
        # It will be done in the preprocessing function
        cleaned_args[gpn.identifier()] = None

    # Initial split Method
    cleaned_args[gpn.initial_split_method()] = str_to_splittingmethod(args[gpn.initial_split_method()])
    if cleaned_args[gpn.initial_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and \
       cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute(cleaned_args[gpn.initial_split_method()])

    # Main directory
    if cleaned_args[gpn.main_directory()] is None:
        cleaned_args[gpn.main_directory()] = get_filename(cleaned_args[gpn.database()])

    # Preprocessed database name
    if args[gpn.preprocessed_database_name()] is None:
        cleaned_args[gpn.preprocessed_database_name()] = _get_preprocessed_db_name(cleaned_args, extension=extension)
    else:
        cleaned_args[gpn.preprocessed_database_name()] = get_filename(cleaned_args[gpn.preprocessed_database_name()],
                                                                      with_extension=True)

    # Reference database name
    cleaned_args[gpn.reference_name()] = get_filename(cleaned_args[gpn.reference_name()],
                                                      with_extension=False) + extension

    # Reference split Method
    cleaned_args[gpn.reference_split_method()] = str_to_splittingmethod(args[gpn.reference_split_method()])
    if cleaned_args[gpn.reference_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and \
       cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute(cleaned_args[gpn.reference_split_method()])

    # Reference split value

    # Statistics file name

    # Subsubtrain directory name pattern
    # TODO: I don't know why, but docopt can't parse the default value
    if cleaned_args[gpn.subsubtrain_directory_pattern()] is None:
        cleaned_args[gpn.subsubtrain_directory_pattern()] = gdv.subsubtrain_directory_pattern()

    # Subsubtrain name pattern

    # Subtrain directory

    # Subtrain name
    cleaned_args[gpn.subtrain_name()] = get_filename(cleaned_args[gpn.subtrain_name()], with_extension=False) + extension

    # Test database name
    cleaned_args[gpn.test_name()] = get_filename(cleaned_args[gpn.test_name()], with_extension=False) + extension

    # Train database name
    cleaned_args[gpn.train_name()] = get_filename(cleaned_args[gpn.train_name()], with_extension=False) + extension

    # Training value
    cleaned_args[gpn.training_value()] = _convert_row_limit(cleaned_args[gpn.training_value()],
                                                            env.statistics[gsn.instances_in_database()])

    # Tree file extension

    # Trees in forest
    cleaned_args[gpn.trees_in_forest()] = int(cleaned_args[gpn.trees_in_forest()])

    # Vector file extension

    # Add statistics
    env.statistics[gsn.database_path()] = cleaned_args[gpn.database()]
    env.statistics[gsn.database_name()] = get_filename(cleaned_args[gpn.database()])
    env.statistics[gsn.preprocessed_database_path()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.preprocessed_database_name()]
    env.statistics[gsn.train_path()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.train_name()]
    env.statistics[gsn.test_path()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.test_name()]
    env.statistics[gsn.subtrain_path()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.subtrain_directory()] + "/" + cleaned_args[gpn.subtrain_name()]
    env.statistics[gsn.reference_path()] = cleaned_args[gpn.main_directory()] + "/" + cleaned_args[gpn.subtrain_directory()] + "/" + cleaned_args[gpn.reference_name()]

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
  {param_preprocessed_db_name}=<name>       {doc_preprocessed_db_name}
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
""".format(**_FORMAT_DICTIONARY).format(**_FORMAT_DICTIONARY)

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
