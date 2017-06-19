""" This module contains all functions related to parsing command-line arguments for all entry points of the package.
It uses the `docopt` package (listed as a dependencie) to easily combine the tedious task of writing documentation
and parsing arguments.
#TODO: We can gain time by not formatting the helping message twice, but by directly formatting the documentation from
#      the format dictionary
"""
import docopt

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_parameter_documentation as gpd
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.initialization.arg_cleaner import clean_args
from ensemble_experimentation.src.vrac.file_system import get_filename

_FORMAT_DICTIONARY = dict(
    # Documentation
    doc_usage=gpd.usage(),
    doc_training_value=gpd.training_value(),
    doc_reference_value=gpd.reference_value(),
    doc_trees_in_forest=gpd.trees_in_forest(),
    doc_initial_split_method=gpd.initial_split_method(),
    doc_reference_split_method=gpd.reference_split_method(),
    doc_subsubtrain_split_method=gpd.subsubtrain_split_method(),
    doc_train_name=gpd.train_name(),
    doc_test_name=gpd.test_name(),
    doc_preprocessed_db_name=gpd.preprocessed_database_name(),
    doc_subtrain_name=gpd.subtrain_name(),
    doc_reference_name=gpd.reference_name(),
    doc_subsubtrain_name_pattern=gpd.subsubtrain_name_pattern(),
    doc_statistics_name=gpd.statistics_file_name(),
    doc_header_name=gpd.header_name(),
    doc_tree_file_extension=gpd.tree_file_extension(),
    doc_vector_file_extension=gpd.vector_file_extension(),
    doc_header_extension=gpd.header_extension(),
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
    param_subsubtrain_split_method=gpn.subsubtrain_split_method(),
    param_train_name=gpn.train_name(),
    param_test_name=gpn.test_name(),
    param_preprocessed_db_name=gpn.preprocessed_database_name(),
    param_subtrain_name=gpn.subtrain_name(),
    param_reference_name=gpn.reference_name(),
    param_subsubtrain_name_pattern=gpn.subsubtrain_name_pattern(),
    param_statistics_name=gpn.statistics_file_name(),
    param_header_name=gpn.header_name(),
    param_tree_file_extension=gpn.tree_file_extension(),
    param_vector_file_extension=gpn.vector_file_extension(),
    param_header_extension=gpn.header_extension(),
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
    default_header_name=gdv.header_name(),
    default_tree_file_extension=gdv.tree_file_extension(),
    default_vector_file_extension=gdv.vector_file_extension(),
    default_header_extension=gdv.header_extension(),
    default_subtrain_directory=gdv.subtrain_directory(),
    default_subsubtrain_directory_pattern=gdv.subsubtrain_directory_pattern(),
    default_identifier=gdv.identifier(),
    default_encoding=gdv.encoding(),
    default_format_db=gdv.format_db(),
    default_delimiter=gdv.delimiter(),

    # Miscellaneous
    global_name=ggv.name()
)


def _init_statistics(args: dict) -> None:
    """ Initialize the `statistics` dictionary located inside the `env` module. """
    env.statistics[gsn.database_path()] = args[gpn.database()]
    env.statistics[gsn.database_name()] = get_filename(args[gpn.database()])
    env.statistics[gsn.preprocessed_database_path()] = "{}/{}".format(args[gpn.main_directory()],
                                                                      args[gpn.preprocessed_database_name()])
    env.statistics[gsn.train_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.train_name()])
    env.statistics[gsn.test_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.test_name()])
    env.statistics[gsn.subtrain_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                            args[gpn.subtrain_name()])
    env.statistics[gsn.reference_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                             args[gpn.reference_name()])


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
  {param_subsubtrain_split_method}=<method> {doc_subsubtrain_split_method}

  # File names
  {param_train_name}=<name>                 {doc_train_name}
  {param_test_name}=<name>                  {doc_test_name}
  {param_preprocessed_db_name}=<name>       {doc_preprocessed_db_name}
  {param_subtrain_name}=<name>              {doc_subtrain_name}
  {param_reference_name}=<name>             {doc_reference_name}
  {param_subsubtrain_name_pattern}=<name>   {doc_subsubtrain_name_pattern}
  {param_statistics_name}=<name>            {doc_statistics_name}
  {param_header_name}=<name>                {doc_header_name}
  {param_tree_file_extension}=<name>        {doc_tree_file_extension}
  {param_vector_file_extension}=<name>      {doc_vector_file_extension}
  {param_header_extension}=<name>           {doc_header_extension}

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
    cleaned_arguments = clean_args(arguments)

    env.arguments = arguments
    env.cleaned_arguments = cleaned_arguments

    _init_statistics(cleaned_arguments)


def parse_args_forest_entry_point() -> dict:
    pass


def parse_args_forest_reduction_entry_point() -> dict:
    pass


if __name__ == "__main__":
    pass
