""" This module defines functions to easily access values stored in the file `output_messages.json`, located in the
`res` folder at the root of the program's package.
This file contains messages which will be outputed in the standard output stream.

To print an output message, for example the one outputed if we need to put the class column at the end of the database
during the preprocessing, simply call:
>>> print(Message.APPEND_CLASS)

The module will check if the current verbosity level match the verbosity of the message, and automatically print it if
it's printable.
"""
import json
import os
from enum import IntEnum, Enum

import ensemble_experimentation.src.getters.environment as env

_PATH_OUTPUT_MESSAGES = "../../res/default_values.json"


class Verbosity(IntEnum):
    QUIET = 0
    NORMAL = 1
    VERBOSE = 2


class Message(Enum):
    PREPEND_ID = "prepend_id"
    APPEND_CLASS = "append_class"

    def __str__(self):
        return _is_printable(self.value)


def _is_printable(message_key: str):
    if env.verbosity == Verbosity.QUIET:
        return ""
    elif env.verbosity == Verbosity.NORMAL:
        if _is_a_normal_message(message_key):
            return _get_message_from_file(message_key)
    elif env.verbosity == Verbosity.VERBOSE:
        return _get_message_from_file(message_key)
    else:
        return ""


def _is_a_normal_message(message_key: str) -> bool:
    return message_key[:5] != "verb_"


def _get_message_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_OUTPUT_MESSAGES)
    with open(path) as file:
        return json.load(file)[value]


if __name__ == '__main__':
    pass
