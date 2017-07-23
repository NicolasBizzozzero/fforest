""" This module contains useful tools to manipulate the `Dialect` class.
This class regroup multiple parameters related to the CSV format, reducing drastically the number of parameters
contained inside CSV-related functions.
"""
import csv


class Dialect:
    def __init__(self, *, encoding: str = "utf8", delimiter: str = ",", quoting: int = csv.QUOTE_NONNUMERIC,
                 quote_char: str = "\"", line_delimiter: str = None, skip_initial_space: bool = True):
        self.encoding = encoding
        self.delimiter = delimiter
        self.quoting = quoting
        self.quote_char = quote_char
        self.line_delimiter = line_delimiter
        self.skip_initial_space = skip_initial_space
