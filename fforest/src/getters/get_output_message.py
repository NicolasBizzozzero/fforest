""" This module defines functions to easily access values stored in the file `output_messages.json`, located in the
`res` folder at the root of the program's package. This file contains messages which will be outputed in the standard
output stream.
To print an output message, for example the one outputed if we need to put the class column at the end of the database
during the preprocessing phase, simply call:
vprint(Message.APPEND_CLASS)

The module will check if the current verbosity level match the verbosity of the message, and automatically print it if
it's printable.

"""
import json
import os
from enum import IntEnum, Enum
from typing import Union

import fforest.src.getters.environment as env
import fforest.src.getters.get_default_value as gdv

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
    INITIAL_PREPROCESSING = "initial_preprocessing"
    ADD_ID = "add_id"
    PREPEND_ID = "prepend_id"
    APPEND_CLASS = "append_class"
    EXTRACT_HEADER = "extract_header"
    ENVIRONMENT_FILE_NOT_FOUND = "environment_file_not_found"


def vprint(message: Message, **kwargs) -> None:
    message_key = message.value
    message = _get_message_with_verbosity(message_key, env.verbosity,
                                          default_verbosity=string_to_verbosity(gdv.verbosity()))
    if message is not None:
        print(message.format(**kwargs), end="\n", sep="")


def _get_message_with_verbosity(message_key: str, verbosity: Union[Verbosity, None],
                                default_verbosity: Verbosity = Verbosity.NORMAL) -> Union[str, None]:
    if verbosity == Verbosity.QUIET:
        return None
    elif verbosity == Verbosity.NORMAL:
        if _is_a_normal_message(message_key):
            return _get_message_from_file(message_key)
        else:
            return None
    elif verbosity == Verbosity.VERBOSE:
        return _get_message_from_file(message_key)
    elif verbosity is None:
        # Verbosity level has not been initialized, we assume it's the default verbosity
        return _get_message_with_verbosity(message_key, default_verbosity)
    else:
        raise UnknownVerbosity(env.verbosity)


def _get_message_from_file(value):
    global _PATH_OUTPUT_MESSAGES

    path = os.path.join(os.path.dirname(__file__),
                        _PATH_OUTPUT_MESSAGES)
    with open(path) as file:
        return json.load(file)[value]


def _is_a_normal_message(message_key: str) -> bool:
    global VERBOSE_KEY_PREFIX

    return message_key[:len(VERBOSE_KEY_PREFIX)] != VERBOSE_KEY_PREFIX


if __name__ == '__main__':
    pass
