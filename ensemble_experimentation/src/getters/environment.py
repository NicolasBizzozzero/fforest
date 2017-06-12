""" This module defines environment variables which'll be used by all the modules and packages of the program.
"""
# Contains every parsed arguments without any modification
arguments = dict()

# Contains argument cleaned for better an faster uses by the program
cleaned_arguments = dict()

# Contains useful statistics for the user
statistics = dict()


def number_of_rows() -> str:
    return "number_of_rows"
