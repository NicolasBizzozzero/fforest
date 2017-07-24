""" Initialize the variables contained in the `environment` module. """
from fforest.src.core.phase.learning_process.triangular_norms import tnorm_to_str
from fforest.src.core.phase.phase import Phase
from fforest.src.file_tools.csv_tools import get_column
from fforest.src.file_tools.dialect import Dialect
from fforest.src.file_tools.format import format_to_str
from fforest.src.getters import environment as env, get_parameter_name as gpn
from fforest.src.vrac.file_system import get_filename


def init_environment(args: dict) -> None:
    _init_command_line_parameters(args)
    _init_miscellaneous(args)
    _init_dir_paths(args)
    _init_paths(args)
    _init_names(args)


def _init_command_line_parameters(args: dict) -> None:
    """ Initialize all the command-line-parameters-related variables located inside the `env` module. """
    env.cclassified_vector_prefix = args.get(gpn.cclassified_vector_prefix().split()[-1])
    env.class_name = args.get(gpn.class_name().split()[-1])
    env.class_matrix_prefix = args.get(gpn.class_matrix_prefix().split()[-1])
    env.classes_matrices_directory = args.get(gpn.classes_matrices_directory().split()[-1])
    env.clustering_trees_directory = args.get(gpn.clustering_trees_directory().split()[-1])
    env.clustering_trees_method = args.get(gpn.clustering_trees_method().split()[-1])
    env.delimiter_input = args.get(gpn.delimiter_input().split()[-1])
    env.delimiter_output = args.get(gpn.delimiter_output().split()[-1])
    env.difficulty_vector_prefix = args.get(gpn.difficulty_vector_prefix().split()[-1])
    env.discretization_threshold = args.get(gpn.discretization_threshold().split()[-1])
    env.encoding_input = args.get(gpn.encoding_input().split()[-1])
    env.encoding_output = args.get(gpn.encoding_output().split()[-1])
    env.entropy_measure = args.get(gpn.entropy_measure().split()[-1])
    env.entropy_threshold = args.get(gpn.entropy_threshold().split()[-1])
    env.format_input = args.get(gpn.format_input().split()[-1])
    env.format_output = args.get(gpn.format_output().split()[-1])
    env.have_header = args.get(gpn.have_header().split()[-1])
    env.header_extension = args.get(gpn.header_extension().split()[-1])
    env.header_name = args.get(gpn.header_name().split()[-1])
    env.identifier = args.get(gpn.identifier().split()[-1])
    env.last_phase = args.get(gpn.last_phase().split()[-1])
    env.initial_database_name = args.get(gpn.database().split()[-1])
    env.initial_split_method = args.get(gpn.initial_split_method().split()[-1])
    env.line_delimiter_input = args.get(gpn.line_delimiter_input().split()[-1])
    env.line_delimiter_output = args.get(gpn.line_delimiter_output().split()[-1])
    env.main_directory = args.get(gpn.main_directory().split()[-1])
    env.minimal_size_leaf = args.get(gpn.min_size_leaf().split()[-1])
    env.parent_dir = args.get(gpn.parent_dir())
    env.preprocessed_database_name = args.get(gpn.preprocessed_database_name().split()[-1])
    env.quality_threshold = args.get(gpn.quality_threshold().split()[-1])
    env.salammbo_vector_prefix = args.get(gpn.salammbo_vector_prefix().split()[-1])
    env.quality_computing_method = args.get(gpn.quality_computing_method().split()[-1])
    env.quality_file_prefix = args.get(gpn.quality_file_prefix().split()[-1])
    env.quote_character_input = args.get(gpn.quote_char_input().split()[-1])
    env.quote_character_output = args.get(gpn.quote_char_output().split()[-1])
    env.quoting_input = args.get(gpn.quoting_input().split()[-1])
    env.quoting_output = args.get(gpn.quoting_output().split()[-1])
    env.reference_database_name = args.get(gpn.reference_name().split()[-1])
    env.reference_split_method = args.get(gpn.reference_split_method().split()[-1])
    env.reference_value = args.get(gpn.reference_value().split()[-1])
    env.resume_phase = args.get(gpn.resume_phase().split()[-1])
    env.statistics_file_name = args.get(gpn.statistics_file_name().split()[-1])
    env.subsubtrain_directory = args.get(gpn.subsubtrain_directory().split()[-1])
    env.subsubtrain_directory_pattern = args.get(gpn.subsubtrain_directory_pattern().split()[-1])
    env.subsubtrain_name_pattern = args.get(gpn.subsubtrain_name_pattern().split()[-1])
    env.subsubtrain_split_method = args.get(gpn.subsubtrain_split_method().split()[-1])
    env.subtrain_directory = args.get(gpn.subtrain_directory().split()[-1])
    env.subtrain_name = args.get(gpn.subtrain_name().split()[-1])
    env.t_norms = args.get(gpn.number_of_tnorms().split()[-1])
    env.test_database_name = args.get(gpn.test_name().split()[-1])
    env.train_database_name = args.get(gpn.train_name().split()[-1])
    env.training_value = args.get(gpn.training_value().split()[-1])
    env.tree_file_extension = args.get(gpn.tree_file_extension().split()[-1])
    env.trees_in_forest = args.get(gpn.trees_in_forest().split()[-1])
    env.true_class_directory = args.get(gpn.true_class_directory().split()[-1])
    env.vector_file_extension = args.get(gpn.vector_file_extension().split()[-1])
    env.verbosity = args.get(gpn.verbosity().split()[-1])


def _init_miscellaneous(args: dict) -> None:
    """ Initialize all the others variables inside the `env` module. """
    env.current_phase = Phase.PREPROCESSING
    env.dialect_input = Dialect(encoding=env.encoding_input,
                                delimiter=env.delimiter_input,
                                quoting=env.quoting_input,
                                quote_char=env.quote_character_input,
                                line_delimiter=env.line_delimiter_input,
                                skip_initial_space=True)
    env.dialect_output = Dialect(encoding=env.encoding_output,
                                 delimiter=env.delimiter_output,
                                 quoting=env.quoting_output,
                                 quote_char=env.quote_character_output,
                                 line_delimiter=env.line_delimiter_output,
                                 skip_initial_space=True)
    env.possible_classes = list(set(get_column(path=args.get(gpn.database()),
                                               column=args.get(gpn.class_name()),
                                               have_header=args.get(gpn.have_header()),
                                               dialect=env.dialect_input)))
    if args.get(gpn.number_of_tnorms()):
        env.t_norms_names = [tnorm_to_str(name) for name in range(args.get(gpn.number_of_tnorms()) + 1)]


def _init_dir_paths(args: dict) -> None:
    """ Initialize all the path-related directories variables inside the `env` module. """
    env.main_directory_path = "{}/{}".format(env.parent_dir, env.main_directory)
    env.subtrain_directory_path = "{}/{}".format(env.main_directory_path, env.subtrain_directory)
    env.subsubtrain_directory_path = "{}/{}".format(env.subtrain_directory_path, env.subsubtrain_directory)

    if env.trees_in_forest:
        env.subsubtrain_directories_path = ["{}/{}".format(env.subsubtrain_directory_path,
                                                           env.subsubtrain_directory_pattern %
                                                           str(tree_index).zfill(len(str(env.trees_in_forest))))
                                            for tree_index in range(1, env.trees_in_forest + 1)]
    if env.classes_matrices_directory:
        env.classes_matrices_directory_path = "{}/{}".format(env.subtrain_directory_path,
                                                             env.classes_matrices_directory)
        env.classes_matrices_directories_path = {class_name: "{}/{}".format(env.classes_matrices_directory_path,
                                                                            class_name) for
                                                 class_name in env.possible_classes}
    if env.clustering_trees_directory:
        env.clustering_trees_directory_path = "{}/{}".format(env.subtrain_directory_path,
                                                             env.clustering_trees_directory)
        env.clustering_trees_directories_path = {class_name: "{}/{}".format(env.clustering_trees_directory_path,
                                                                            class_name) for
                                                 class_name in env.possible_classes}


def _init_paths(args: dict) -> None:
    """ Initialize all the path-related variables inside the `env` module. """
    env.statistics_file_path = "{}/{}".format(env.main_directory_path, env.statistics_file_name)
    env.original_database_path = args.get(gpn.database())
    env.preprocessed_database_path = "{}/{}".format(env.main_directory_path, args.get(gpn.preprocessed_database_name()))
    env.header_path = "{}/{}".format(env.main_directory_path, env.header_name)
    env.test_database_path = "{}/{}".format(env.main_directory_path, args.get(gpn.test_name()))
    env.train_database_path = "{}/{}".format(env.main_directory_path, args.get(gpn.train_name()))
    env.reference_database_path = "{}/{}".format(env.subtrain_directory_path, args.get(gpn.reference_name()))
    env.subtrain_database_path = "{}/{}".format(env.subtrain_directory_path, args.get(gpn.subtrain_name()))
    if env.trees_in_forest:
        env.subsubtrain_databases_paths = ["{}/{}.{}".format(env.subsubtrain_directories_path[tree_index],
                                                             env.subsubtrain_directory_pattern %
                                                             str(tree_index + 1).zfill(len(str(env.trees_in_forest))),
                                                             format_to_str(args.get(gpn.format_output())).lower()) for
                                           tree_index in range(env.trees_in_forest)]
        env.cclassified_vectors_paths = {tnorm: ["{}/{}{}.{}".format(env.subsubtrain_directories_path[tree_index - 1],
                                                                     env.cclassified_vector_prefix,
                                                                     tnorm,
                                                                     env.vector_file_extension) for
                                                 tree_index in range(1, env.trees_in_forest + 1)] for
                                         tnorm in [tnorm_to_str(tnorm_index) for tnorm_index in range(env.t_norms + 1)]}

        env.salammbo_vectors_paths = {tnorm: ["{}/{}{}.{}".format(env.subsubtrain_directories_path[tree_index - 1],
                                                                  env.salammbo_vector_prefix,
                                                                  tnorm,
                                                                  env.vector_file_extension) for
                                              tree_index in range(1, env.trees_in_forest + 1)] for
                                      tnorm in [tnorm_to_str(tnorm_index) for tnorm_index in range(env.t_norms + 1)]}
    if env.t_norms:
        env.difficulty_vectors_paths = {tnorm: "{}/{}{}.{}".format(env.subtrain_directory_path,
                                                                   env.difficulty_vector_prefix,
                                                                   tnorm,
                                                                   env.vector_file_extension) for
                                        tnorm in [tnorm_to_str(tnorm_index) for tnorm_index in range(env.t_norms + 1)]}
        env.quality_files_paths = {tnorm: "{}/{}{}.{}".format(env.subtrain_directory_path,
                                                              env.quality_file_prefix,
                                                              tnorm,
                                                              format_to_str(args.get(gpn.format_output()))) for
                                   tnorm in [tnorm_to_str(tnorm_index) for tnorm_index in range(env.t_norms + 1)]}
        env.classes_matrices_files_paths = {class_name: {tnorm: "{}/{}{}_{}.{}".format(
            env.classes_matrices_directories_path[class_name],
            env.class_matrix_prefix,
            class_name,
            tnorm,
            format_to_str(args.get(gpn.format_output()))) for
            tnorm in [tnorm_to_str(tnorm_index) for tnorm_index in range(env.t_norms + 1)]}
            for class_name in env.possible_classes}


def _init_names(args: dict) -> None:
    """ Initialize all the names-related variables inside the `env` module. """
    env.original_database_name = get_filename(args.get(gpn.database()))
