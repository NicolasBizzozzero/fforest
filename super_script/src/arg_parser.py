from docopt import docopt


def parse_args():
    help_message = r"""super_script

Usage:
    super_script.py <database> [<ptrain>] [<ptest>]

Options:
    -h --help           Print the help message.
    --ptrain=<75>       % of training values to extract from the database.
    --ptest=<25>        % of testing values to extract from the database.
"""
    return docopt(help_message)
