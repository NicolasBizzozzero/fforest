from fforest.src.vrac.file_system import file_exists
from fforest.src.core.phase.ending.environment_file import ENVIRONMENT_FILE_NAME, load_environment_file
from fforest.src.core.phase.phase import Phase
import fforest.src.getters.environment as env
import fforest.src.getters.get_parameter_name as gpn
import os
import sys


def compute_first_phase() -> Phase:
    main_dir_name = _get_main_dir_name()
    environment_file_path = os.path.join(main_dir_name, ENVIRONMENT_FILE_NAME)

    if _env_file_exists(environment_file_path):
        # User wants to resume where he stopped last time
        if _starting_phase_asked():
            load_environment_file(path=environment_file_path)
            if
            return env.current_phase
        elif _resume_phase_asked():
            load_environment_file(path=environment_file_path)
            return env.current_phase
    # User want to compute all phases, regarding of previous computations
    else:
        return Phase.PARSING


def _env_file_exists(environment_file_path: str) -> bool:
    return file_exists(environment_file_path)


def _get_main_dir_name() -> str:
    try:
        return sys.argv[sys.argv.index(gpn.main_directory()) + 1]
    except ValueError:
        return os.path.dirname(sys.argv[0])


def _resume_phase_asked() -> bool:
    return bool(sys.argv[sys.argv.index(gpn.resume_phase()) + 1])
