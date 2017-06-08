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
    param_keep_header=gpn.keep_header(),

    # Default values
    default_identificator=gdv.identificator(),
    default_encoding=gdv.encoding(),
    default_training_value=gdv.training_value(),
    default_format_db=gdv.format_db(),
    default_reference_value=gdv.reference_value(),
    default_delimiter=gdv.delimiter(),
    default_keep_header=gdv.keep_header(),

    # Global variables
    global_name=ggv.name()
)


def parse_args_main_entry_point():
    global _FORMAT_DICTIONARY

    documentation = """{global_name}

Usage:
  ensemble_experimentation.py <{param_database}> [{param_training_value} <training_value>] [{param_trees_in_forest} <trees_in_forest>] [{param_reference_value} <reference_value>] [{param_identificator} <ID>] [{param_encoding} <encoding>] [{param_format_db} <format>] [{param_delimiter} <delimiter>] [{param_keep_header} <keep_header>]

Options:
  -h --help            Print this help message.
  {param_identificator}=<ID>            The class name of the examples' identifier [default: {default_identificator}].
  {param_encoding}=<encoding>           The encoding used to read the database and write the outputs. [default: {default_encoding}]
  {param_training_value}=<training_value>  % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_training_value}].
  {param_trees_in_forest}=<trees_in_forest>   Number of trees in to create in the base forest.
  {param_format_db}=<format>               The format used to read the database and write the outputs. [default: {default_format_db}]
  {param_reference_value}=<reference_value>   % of the values you want to extract from the training set and put in the reference set. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_reference_value}].
  {param_delimiter}=<delimiter>           The symbol used to delimiting data in CSV database. [default: {default_delimiter}]
  {param_keep_header}=<keep_header>      A boolean set to 1 if you want to keep and past the header in all outputs, or 0 otherwise. Set it to 0 if your original database don't have any header. [default: {default_keep_header}]
""".format(**_FORMAT_DICTIONARY)

    # Rename parameter database
    parameters_dict = docopt(documentation, version=ggv.version(), help=True)
    parameters_dict["{param_database}".format(**_FORMAT_DICTIONARY)] = parameters_dict["<{param_database}>".format(**_FORMAT_DICTIONARY)]
    del parameters_dict["<{param_database}>".format(**_FORMAT_DICTIONARY)]

    # Convert string values to desired values
    # Keep header
    if parameters_dict["{param_keep_header}".format(**_FORMAT_DICTIONARY)] == "0":
        parameters_dict["{param_keep_header}".format(**_FORMAT_DICTIONARY)] = False
    else:
        parameters_dict["{param_keep_header}".format(**_FORMAT_DICTIONARY)] = True

    return parameters_dict


def parse_args_forest_entry_point():
    pass


def parse_args_forest_reduction_entry_point():
    pass


if __name__ == "__main__":
    pass
