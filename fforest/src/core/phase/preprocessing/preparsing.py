""" This module is used to retrieve the first phase asked by the user. It should be called with the
`compute_first_phase` method first. It shouldn't be used anywhere in the software but before any form of parsing
has been made. It also shouldn't be needed by any entry point but the `main_entry_point`.
"""
import os
import sys

import fforest.src.getters.environment as env
import fforest.src.getters.get_parameter_name as gpn
from fforest.src.core.phase.ending.environment_file import ENVIRONMENT_FILE_NAME, load_environment_file
from fforest.src.core.phase.phase import Phase, str_to_phase, phase_processable, phase_to_str
from fforest.src.getters.get_output_message import vprint, Message
from fforest.src.vrac.file_system import file_exists


class UnprocessablePhase(Exception):
    def __init__(self, first_phase: str, last_phase: str):
        Exception.__init__(self, "The phase \"{first_phase}\" can't be processed before "
                                 "\"{last_phase}\".".format(first_phase=first_phase, last_phase=last_phase))


def compute_first_phase() -> Phase:
    """ Parse only a part of arguments needed to know if the user asked to start the software from the beginning or from
    a specific phase. Thus return the asked phase.
    """
    main_dir_name = _get_main_dir_name()
    environment_file_path = os.path.join(os.getcwd(), main_dir_name, ENVIRONMENT_FILE_NAME)

    if _env_file_exists(environment_file_path) and _resume_phase_asked():
        # User wants to resume where he stopped last time
        load_environment_file(path=environment_file_path)
        current_phase = str_to_phase(sys.argv[sys.argv.index(gpn.resume_phase()) + 1])

        # Check if the data needed to process the phase asked have been previously computed
        if not phase_processable(phase_to_compute=current_phase, last_phase_computed=env.last_phase):
            raise UnprocessablePhase(phase_to_str(current_phase), phase_to_str(env.last_phase))
        else:
            env.current_phase = current_phase
            return current_phase
    else:
        # User want to compute all phases, regarding of previous computations (or asked it but environment file has not
        # been found).
        if (not _env_file_exists(environment_file_path)) and _resume_phase_asked():
            vprint(Message.ENVIRONMENT_FILE_NOT_FOUND)
        env.current_phase = Phase.PARSING
        return Phase.PARSING


def _get_main_dir_name() -> str:
    """ Return the name of the main directory. Try to get it from the command line if it has been given by the user, or
    then return the default value (basename of the database), located in the current directory.
    """
    try:
        return sys.argv[sys.argv.index(gpn.main_directory()) + 1]
    except ValueError:
        return os.path.splitext(os.path.basename(sys.argv[1]))[0]


def _env_file_exists(environment_file_path: str) -> bool:
    """ Check the existence of the environment file. """
    return file_exists(environment_file_path)


def _resume_phase_asked() -> bool:
    """ Check if the user asked to resume at a specific phase. Try to retrieve this information directly from the
    command-line.
    """
    try:
        sys.argv.index(gpn.resume_phase())
        return True
    except ValueError:
        return False
