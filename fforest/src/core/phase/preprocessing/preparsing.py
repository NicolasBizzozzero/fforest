from fforest.src.getters.get_output_message import vprint, Message
from fforest.src.vrac.file_system import file_exists
from fforest.src.core.phase.ending.environment_file import ENVIRONMENT_FILE_NAME, load_environment_file
from fforest.src.core.phase.phase import Phase, str_to_phase, phase_processable, phase_to_str
import fforest.src.getters.environment as env
import fforest.src.getters.get_parameter_name as gpn
import os
import sys


class UnprocessablePhase(Exception):
    def __init__(self, first_phase: str, last_phase: str):
        Exception.__init__(self, "The phase \"{first_phase}\" can't be processed before "
                                 "\"{last_phase}\".".format(first_phase=first_phase, last_phase=last_phase))


def compute_first_phase() -> Phase:
    main_dir_name = _get_main_dir_name()
    environment_file_path = os.path.join(os.getcwd(), main_dir_name, ENVIRONMENT_FILE_NAME)

    print("env file exists :", _env_file_exists(environment_file_path))
    print(environment_file_path)
    print(os.path.isfile(environment_file_path))
    #print("resumephaseasked :", _resume_phase_asked())
    # User wants to resume where he stopped last time
    if _env_file_exists(environment_file_path) and _resume_phase_asked():
        print("\n\nRESUME PHASE ASKED\n\n")
        load_environment_file(path=environment_file_path)
        current_phase = str_to_phase(sys.argv[sys.argv.index(gpn.resume_phase()) + 1])
        if not phase_processable(phase_to_compute=current_phase, last_phase_computed=env.last_phase):
            raise UnprocessablePhase(phase_to_str(current_phase), phase_to_str(env.last_phase))
        else:
            env.current_phase = current_phase
            return current_phase
    # User want to compute all phases, regarding of previous computations
    else:
        if (not _env_file_exists(environment_file_path)) and _resume_phase_asked():
            vprint(Message.ENVIRONMENT_FILE_NOT_FOUND)
        print("\n\nRESUME PHASE NOT ASKED\n\n")
        env.current_phase = Phase.PARSING
        return Phase.PARSING


def _env_file_exists(environment_file_path: str) -> bool:
    return file_exists(environment_file_path)


def _get_main_dir_name() -> str:
    try:
        return sys.argv[sys.argv.index(gpn.main_directory()) + 1]
    except ValueError:
        return os.path.splitext(os.path.basename(sys.argv[1]))[0]


def _resume_phase_asked() -> bool:
    try:
        sys.argv.index(gpn.resume_phase())
        return True
    except ValueError:
        return False
