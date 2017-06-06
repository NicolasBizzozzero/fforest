from docopt import docopt


def parse_args():
    DEFAULT_ID = "_ID"
    DEFAULT_DATATRAIN = 0.75

    documentation = r"""ensemble_experimentation

Usage:
  ensemble_experimentation.py <database> [--train <datatrain>] [--trainforet <datatrainforet>] [--reference <datareference>] [--id <ID>]

Options:
  -h --help            Print this help message.
  --train=<datatrain>  % of training values to extract from the database. You can also pass the number of values you want to use (by passing an integer greater than 1) [default: {default_datatrain}].
  --id=<ID>            The class name of the examples' identifier [default: {default_id}].
""".format(default_id=DEFAULT_ID, default_datatrain=DEFAULT_DATATRAIN)
    return docopt(documentation, version="0.0.1", help=True)
