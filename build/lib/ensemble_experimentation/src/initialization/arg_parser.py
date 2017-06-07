from docopt import docopt
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation


def parse_args_main_entry_point():
    documentation = r"""ensemble_experimentation

Usage:
  ensemble_experimentation.py <database> [--train <datatrain>] [--trainforet <datatrainforet>] [--reference <datareference>] [--id <ID>]

Options:
  -h --help            Print this help message.
  --train=<datatrain>  % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {value_datatrain}].
  --id=<ID>            The class name of the examples' identifier [default: {value_id}].
""".format(value_id=gdv.id(), value_datatrain=gdv.pourcentage_train())
    return docopt(documentation, version=ensemble_experimentation.__version__, help=True)


def parse_args_forest_entry_point():
    pass


def parse_args_forest_reduction_entry_point():
    pass

if __name__ == "__main__":
    pass
