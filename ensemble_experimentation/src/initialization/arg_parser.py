from docopt import docopt
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_global_variables as ggv


def parse_args_main_entry_point():
    documentation = r"""{name}

Usage:
  ensemble_experimentation.py <{param_database}> [{param_training_values} <training_value>] [{param_trees_in_forest} <trees_in_forest>] [{param_reference_values} <reference_value>] [{param_identificator} <ID>]

Options:
  -h --help            Print this help message.
  {param_identificator}=<ID>            The class name of the examples' identifier [default: {default_id}].
  {param_encoding}=<encoding>           The encoding used to read the database and write the outputs. [default: {default_encoding}]
  {param_training_values}=<training_value>  % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_training_value}].
  {param_trees_in_forest}=<trees_in_forest>   Number of trees in to create in the base forest.
  {param_format}=<format>               The format used to read the database and write the outputs. [default: {default_format}]
  {param_reference_values}=<reference_value>   % of the values you want to extract from the training set and put in the reference set. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_reference_values}].
  {param_delimiter}=<delimiter>           The symbol used to delimiting data in CSV database. [default: {default_delimiter}]
  {param_keep_header}=<keep_header>      A booling set to 1 if you want to keep and past the header in all outputs, or 0 otherwise. Set it to 0 if your original database don't have any header. [default: {default_keep_header}]
""".format(param_training_values=gpn.training_value(), param_trees_in_forest=gpn.trees_in_forest(), param_reference_values)
    return docopt(documentation, version=ensemble_experimentation.__version__, help=True)


def parse_args_forest_entry_point():
    pass


def parse_args_forest_reduction_entry_point():
    pass


if __name__ == "__main__":
    pass
