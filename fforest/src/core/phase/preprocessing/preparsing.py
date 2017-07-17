from fforest.src.vrac.file_system import file_exists
from fforest.src.core.phase.ending.environment_file import ENVIRONMENT_FILE_NAME, load_environment_file
from fforest.src.core.phase.phase import resume_phase, Phase
import fforest.src.getters.environment as env
import fforest.src.getters.get_parameter_name as gpn
import os
import sys


def compute_first_phase() -> Phase:
    main_dir_name = _get_main_dir_name()
    environment_file_path = os.path.join(main_dir_name, ENVIRONMENT_FILE_NAME)

    # User wants to resume where he stopped last time
    if _env_file_exists(environment_file_path) and _resume_phase_asked():
        load_environment_file(path=environment_file_path)
        return env.current_phase
    # User want to compute all phases, regarding of previous computations
    else:
        return Phase.NONE


def _env_file_exists(environment_file_path: str) -> bool:
    return file_exists(environment_file_path)


def _get_main_dir_name() -> str:
    return sys.argv[sys.argv.index(gpn.main_directory()) + 1]


def _resume_phase_asked() -> bool:
    return bool(sys.argv[sys.argv.index(gpn.resume_phase()) + 1])
