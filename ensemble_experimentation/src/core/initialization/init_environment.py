from ensemble_experimentation.src.getters import environment as env, get_statistic_name as gsn, \
    get_parameter_name as gpn
from ensemble_experimentation.src.vrac.file_system import get_filename


def _init_statistics(args: dict) -> None:
    """ Initialize the `statistics` dictionary located inside the `env` module. """
    env.statistics[gsn.database_path()] = args[gpn.database()]
    env.statistics[gsn.database_name()] = get_filename(args[gpn.database()])
    env.statistics[gsn.preprocessed_database_path()] = "{}/{}".format(args[gpn.main_directory()],
                                                                      args[gpn.preprocessed_database_name()])
    env.statistics[gsn.train_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.train_name()])
    env.statistics[gsn.test_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.test_name()])
    env.statistics[gsn.subtrain_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                            args[gpn.subtrain_name()])
    env.statistics[gsn.reference_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                             args[gpn.reference_name()])