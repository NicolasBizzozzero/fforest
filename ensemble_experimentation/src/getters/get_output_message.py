""" This module defines functions to easily access values stored in the file `output_messages.json`, located in the
`res` folder at the root of the program's package.
This file contains messages which will be outputed in the standard output stream.

To print an output message, for example the one outputed if we need to put the class column at the end of the database
during the preprocessing, simply call:
>>> vprint(Message.APPEND_CLASS)

The module will check if the current verbosity level match the verbosity of the message, and automatically print it if
it's printable.
"""
import json
import os
from enum import IntEnum, Enum

import ensemble_experimentation.src.getters.environment as env

_PATH_OUTPUT_MESSAGES = "../../res/output_messages.json"
VERBOSE_KEY_PREFIX = "verbose_"


class Verbosity(IntEnum):
    QUIET = 0
    NORMAL = 1
    VERBOSE = 2


def string_to_verbosity(string: str) -> Verbosity:
    string = string.lower()
    if string == "quiet":
        return Verbosity.QUIET
    elif string == "normal":
        return Verbosity.NORMAL
    elif string == "verbose":
        return Verbosity.VERBOSE
    else:
        raise UnknownVerbosity(string)


class UnknownVerbosity(Exception):
    def __init__(self, verbosity):
        Exception.__init__(self, "The verbosity level \"{verbosity}\" is unknown "
                                 "to the software.".format(verbosity=verbosity))


class Message(Enum):
    PREPEND_ID = "prepend_id"
    APPEND_CLASS = "append_class"
    EXTRACT_HEADER = "extract_header"


def _is_a_normal_message(message_key: str) -> bool:
    global VERBOSE_KEY_PREFIX

    return message_key[:len(VERBOSE_KEY_PREFIX)] != VERBOSE_KEY_PREFIX


def _get_message_from_file(value):
    global _PATH_OUTPUT_MESSAGES

    path = os.path.join(os.path.dirname(__file__),
                        _PATH_OUTPUT_MESSAGES)
    with open(path) as file:
        return json.load(file)[value]


def vprint(message: Message, **kwargs) -> None:
    message_key = message.value

    if env.verbosity == Verbosity.QUIET:
        return None
    elif env.verbosity == Verbosity.NORMAL:
        if _is_a_normal_message(message_key):
            message = _get_message_from_file(message_key)
        else:
            message = ""
    elif env.verbosity == Verbosity.VERBOSE:
        message = _get_message_from_file(message_key)
    else:
        raise UnknownVerbosity(env.verbosity)

    print(message.format(**kwargs), end="", sep="")


if __name__ == '__main__':
    pass
