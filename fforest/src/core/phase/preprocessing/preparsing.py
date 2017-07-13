from fforest.src.vrac.file_system import file_exists
from fforest.src.core.phase.ending.environment_file import ENVIRONMENT_FILE_NAME, load_environment_file
from fforest.src.core.phase.phase import resume_phase
import fforest.src.getters.environment as env
import os


def preparsing() -> None:
    main_dir_name = _get_main_dir_name()
    environment_file_path = os.path.join(main_dir_name, ENVIRONMENT_FILE_NAME)

    if _env_file_exists(environment_file_path) and _resume_phase_asked():
        load_environment_file()
        resume_phase(env.current_phase)


def _get_main_dir_name():
    pass


def _env_file_exists(environment_file_path: str) -> bool:
    return file_exists(environment_file_path)


def _resume_phase_asked() -> bool:
    pass
