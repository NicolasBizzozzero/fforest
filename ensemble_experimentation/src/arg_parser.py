"""ensemble_experimentation

Usage:
  ensemble_experimentation.py <database> [--ptrain <%train>] [--ptest <%test>]

Options:
  -h --help           Print the help message.
  --ptrain=<75>       % of training values to extract from the database.
  --ptest=<25>        % of testing values to extract from the database.
"""

from docopt import docopt


def parse_args():
    return docopt(__doc__, version="0.0.1", help=True)
