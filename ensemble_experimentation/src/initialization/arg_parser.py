from docopt import docopt
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variable as ggv


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


def parse_args_main_entry_point():
    global _FORMAT_DICTIONARY

    documentation = """{global_name}

Usage:
  ensemble_experimentation.py <{param_database}> [{param_training_value} <training_value>] [{param_trees_in_forest} <trees_in_forest>] [{param_reference_value} <reference_value>] [{param_identificator} <ID>] [{param_encoding} <encoding>] [{param_format_db} <format>] [{param_delimiter} <delimiter>] [{param_have_header} <have_header>] [{param_initial_split_train_name} <initial_split_train_name>] [{param_initial_split_test_name} <initial_split_test_name>] [{param_initial_split_method} <initial_split_method>]

Options:
  -h --help            Print this help message.
  {param_identificator}=<ID>            The class name of the examples' identifier [default: {default_identificator}].
  {param_encoding}=<encoding>           The encoding used to read the database and write the outputs. [default: {default_encoding}]
  {param_training_value}=<training_value>  % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_training_value}].
  {param_trees_in_forest}=<trees_in_forest> Number of trees in to create in the base forest.
  {param_format_db}=<format>               The format used to read the database and write the outputs. [default: {default_format_db}]
  {param_reference_value}=<reference_value>   % of the values you want to extract from the training set and put in the reference set. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_reference_value}].
  {param_delimiter}=<delimiter>           The symbol used to delimiting data in CSV database. [default: {default_delimiter}]
  {param_have_header}=<have_header>      Set this boolean to 1 if your database have a header, or 0 otherwise. [default: {default_have_header}]
  {param_initial_split_train_name}=<initial_split_train_name> The name of the training database after the initial split. [default: {default_initial_split_train_name}]
  {param_initial_split_test_name}=<initial_split_test_name>   The name of the testing database after the initial split. [default: {default_initial_split_test_name}]
  {param_initial_split_method}=<initial_split_method>    The method to use with the initial split of the database. Values can be `halfing` or `keepdistribution`
""".format(**_FORMAT_DICTIONARY)

    # Rename parameter database
    parameters_dict = docopt(documentation, version=ggv.version(), help=True)
    parameters_dict["{param_database}".format(**_FORMAT_DICTIONARY)] = parameters_dict["<{param_database}>".format(**_FORMAT_DICTIONARY)]
    del parameters_dict["<{param_database}>".format(**_FORMAT_DICTIONARY)]

    # Convert string values to desired values
    # Have header
    if parameters_dict["{param_have_header}".format(**_FORMAT_DICTIONARY)] == "0":
        parameters_dict["{param_have_header}".format(**_FORMAT_DICTIONARY)] = False
    else:
        parameters_dict["{param_have_header}".format(**_FORMAT_DICTIONARY)] = True

    return parameters_dict


def parse_args_forest_entry_point():
    pass


def parse_args_forest_reduction_entry_point():
    pass


if __name__ == "__main__":
    pass
