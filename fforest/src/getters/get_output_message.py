""" This module defines functions to easily access values stored in the file `output_messages.json`, located in the
`res` folder at the root of the program's package. This file contains messages which will be outputed in the standard
output stream.

If a message needs to be added, one must append it to the file 'output_messages.json'. Carefully chose the name of the
key, it needs to be unique and prefixed by the value `VERBOSE_KEY_PREFIX` if the message is a VERBOSE message.
Thereafter, the key must be added to the `Message` class with the same name as the key, but uppercase (to follows the
PEP8 guidelines about constant names).

To print an output message (for example the one outputed if we need to put the class column at the end of the database
during the preprocessing phase), simply call:
vprint(Message.APPEND_CLASS)
The module will check if the current verbosity level match the verbosity of the message, and automatically print it if
it's printable.

Moreover, if a message needs a dynamic argument, store it in the file like this example :
"print_name": "Hello, my name is {name}."
Add it in the `Message` class, then call the `vprint` function like this :
vprint(Message.PRINT_NAME, name="Christophe")
"""
import enum
import json
import os
from typing import Union

import fforest.src.getters.environment as env
import fforest.src.getters.get_default_value as gdv

_PATH_OUTPUT_MESSAGES = "../../res/output_messages.json"
VERBOSE_KEY_PREFIX = "verbose_"


@enum.unique
class Message(enum.Enum):
    INITIAL_PREPROCESSING = "initial_preprocessing"
    ADD_ID = "add_id"
    PREPEND_ID = "prepend_id"
    APPEND_CLASS = "append_class"
    EXTRACT_HEADER = "extract_header"
    ENVIRONMENT_FILE_NOT_FOUND = "environment_file_not_found"
    GUESS_HEADER = "guess_header"
    GUESS_DELIMITER = "guess_delimiter"
    GUESS_QUOTING = "guess_quoting"
    GUESS_QUOTE_CHARACTER = "guess_quote_character"
    GUESS_ENCODING = "guess_encoding"


@enum.unique
class Verbosity(enum.IntEnum):
    QUIET = 0
    NORMAL = 1
    VERBOSE = 2


def str_to_verbosity(string: str) -> Verbosity:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for verbosity_name, verbosity_value in zip(Verbosity.__members__.keys(), Verbosity.__members__.values()):
        if string == verbosity_name.lower():
            return verbosity_value
    raise UnknownVerbosity(string)


class UnknownVerbosity(Exception):
    def __init__(self, verbosity):
        Exception.__init__(self, "This verbosity level \"{verbosity}\" is unknown "
                                 "to the software.".format(verbosity=verbosity))


def vprint(message: Message, **kwargs) -> None:
    """ Print a message in the standard output based on the `verbosity` variable located at the `env` module. """
    message_key = message.value
    message = _get_message_with_verbosity(message_key, env.verbosity,
                                          default_verbosity=str_to_verbosity(gdv.verbosity()))
    if message is not None:
        print(message.format(**kwargs), end="\n", sep="")


def _get_message_with_verbosity(message_key: str, verbosity: Union[Verbosity, None],
                                default_verbosity: Verbosity = Verbosity.NORMAL) -> Union[str, None]:
    """ Based on `verbosity`, retrieve the message if it should be outputed.
    A QUIET verbosity output nothing.
    A NORMAL verbosity output only normal (useful) messages.
    A VERBOSE verbosity output every messages.
    If no verbosity is passed as argument (the `environment` module has not been initialized), the method will use the
    `default_verbosity`.
    """
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
        raise UnknownVerbosity(verbosity)


def _get_message_from_file(message_key: str):
    """ Retrieve the asked message from the file 'output_messages.json'. """
    global _PATH_OUTPUT_MESSAGES

    path = os.path.join(os.path.dirname(__file__),
                        _PATH_OUTPUT_MESSAGES)
    with open(path) as file:
        return json.load(file)[message_key]


def _is_a_normal_message(message_key: str) -> bool:
    """ Check if a message is not a VERBOSE message. """
    global VERBOSE_KEY_PREFIX

    return message_key[:len(VERBOSE_KEY_PREFIX)] != VERBOSE_KEY_PREFIX


if __name__ == '__main__':
    pass
