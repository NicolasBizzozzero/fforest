""" Initialize the variables contained in the `environment` module. """
from fforest.src.file_tools.csv_tools import get_column
from fforest.src.getters import environment as env, get_parameter_name as gpn
from fforest.src.vrac.file_system import get_filename


def init_environment(args: dict) -> None:
    _init_command_line_parameters(args)
    _init_paths(args)
    _init_names(args)
    _init_miscellaneous(args)


def _init_command_line_parameters(args: dict) -> None:
    """ Initialize all the command-line-parameters-related variables located inside the `env` module. """
    env.class_name = args[gpn.class_name().split()[-1]]
    env.class_found_vector_prefix = args[gpn.class_found_vector_prefix().split()[-1]]
    env.delimiter_input = args[gpn.delimiter_input().split()[-1]]
    env.delimiter_output = args[gpn.delimiter_output().split()[-1]]
    env.difficulty_vector_prefix = args[gpn.difficulty_vector_prefix().split()[-1]]
    env.discretization_threshold = args[gpn.discretization_threshold().split()[-1]]
    env.encoding_input = args[gpn.encoding_input().split()[-1]]
    env.encoding_output = args[gpn.encoding_output().split()[-1]]
    env.entropy_measure = args[gpn.entropy_measure().split()[-1]]
    env.entropy_threshold = args[gpn.entropy_threshold().split()[-1]]
    env.format_input = args[gpn.format_input().split()[-1]]
    env.format_output = args[gpn.format_output().split()[-1]]
    env.have_header = args[gpn.have_header().split()[-1]]
    env.header_extension = args[gpn.header_extension().split()[-1]]
    env.header_name = args[gpn.header_name().split()[-1]]
    env.identifier = args[gpn.identifier().split()[-1]]
    env.initial_database_name = args[gpn.database().split()[-1]]
    env.initial_split_method = args[gpn.initial_split_method().split()[-1]]
    env.main_directory = args[gpn.main_directory().split()[-1]]
    env.minimal_size_leaf = args[gpn.min_size_leaf().split()[-1]]
    env.preprocessed_database_name = args[gpn.preprocessed_database_name().split()[-1]]
    env.quality_threshold = args[gpn.quality_threshold().split()[-1]]
    env.quality_vector_prefix = args[gpn.quality_vector_prefix().split()[-1]]
    env.quote_character_input = args[gpn.quote_char_input().split()[-1]]
    env.quote_character_output = args[gpn.quote_char_output().split()[-1]]
    env.quoting_input = args[gpn.quoting_input().split()[-1]]
    env.quoting_output = args[gpn.quoting_output().split()[-1]]
    env.reference_database_name = args[gpn.reference_name().split()[-1]]
    env.reference_split_method = args[gpn.reference_split_method().split()[-1]]
    env.reference_value = args[gpn.reference_value().split()[-1]]
    env.statistics_file_name = args[gpn.statistics_file_name().split()[-1]]
    env.subsubtrain_directory_pattern = args[gpn.subsubtrain_directory_pattern().split()[-1]]
    env.subsubtrain_name_pattern = args[gpn.subsubtrain_name_pattern().split()[-1]]
    env.subsubtrain_split_method = args[gpn.subsubtrain_split_method().split()[-1]]
    env.subtrain_directory = args[gpn.subtrain_directory().split()[-1]]
    env.subtrain_name = args[gpn.subtrain_name().split()[-1]]
    env.t_norms = args[gpn.number_of_tnorms().split()[-1]]
    env.test_database_name = args[gpn.test_name().split()[-1]]
    env.train_database_name = args[gpn.train_name().split()[-1]]
    env.training_value = args[gpn.training_value().split()[-1]]
    env.tree_file_extension = args[gpn.tree_file_extension().split()[-1]]
    env.trees_in_forest = args[gpn.trees_in_forest().split()[-1]]
    env.vector_file_extension = args[gpn.vector_file_extension().split()[-1]]
    env.verbosity = args[gpn.verbosity().split()[-1]]


def _init_paths(args: dict) -> None:
    """ Initialize all the path-related variables inside the `env` module. """
    env.original_database_path = args[gpn.database()]
    env.preprocessed_database_path = "{}/{}".format(args[gpn.main_directory()],
                                                    args[gpn.preprocessed_database_name()])
    env.train_database_path = "{}/{}".format(args[gpn.main_directory()], args[gpn.train_name()])
    env.test_database_path = "{}/{}".format(args[gpn.main_directory()], args[gpn.test_name()])
    env.subtrain_database_path = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                   args[gpn.subtrain_name()])
    env.reference_database_path = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                    args[gpn.reference_name()])
    env.header_path = "{}/{}.{}".format(env.main_directory, env.header_name, env.header_extension)


def _init_names(args: dict) -> None:
    """ Initialize all the names-related variables inside the `env` module. """
    env.original_database_name = get_filename(args[gpn.database()])


def _init_miscellaneous(args: dict) -> None:
    env.possible_classes = list(set(get_column(path=args[gpn.database()],
                                               column=args[gpn.class_name()],
                                               have_header=args[gpn.have_header()],
                                               delimiter=args[gpn.delimiter_input()],
                                               quoting=args[gpn.quoting_input()],
                                               quote_character=args[gpn.quote_char_input()],
                                               encoding=args[gpn.encoding_input()])))
