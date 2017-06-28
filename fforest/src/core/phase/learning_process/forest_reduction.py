import csv
from typing import Dict, List

import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.classification_methods import methodnum_to_str
from fforest.src.vrac.iterators import subsubtrain_dir_path


def forest_reduction() -> None:
    difficulty_vectors = \
        _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                    number_of_tnorms=env.t_norms,
                                    subsubtrain_directory_pattern=env.subsubtrain_directory_pattern,
                                    vector_extension=env.vector_file_extension,
                                    main_directory=env.main_directory,
                                    subtrain_directory=env.subtrain_directory,
                                    delimiter=env.delimiter_output,
                                    quoting=env.quoting_output,
                                    quote_char=env.quote_character_output,
                                    encoding=env.encoding_output,
                                    quality_vector_prefix=env.quality_vector_prefix)

    _dump_difficulty_vectors(difficulty_vectors=difficulty_vectors,
                             subtrain_dir_path="{}/{}".format(env.original_database_name, env.subtrain_directory),
                             vector_prefix=env.difficulty_vector_prefix,
                             vector_extension=env.vector_file_extension,
                             delimiter=env.delimiter_output,
                             quoting=env.quoting_output,
                             quote_char=env.quote_character_output,
                             encoding=env.encoding_output,
                             skip_initial_space=True)


def _compute_difficulty_vectors(number_of_trees: int, number_of_tnorms: int, subsubtrain_directory_pattern: str,
                                vector_extension: str, main_directory: str, subtrain_directory: str, delimiter: str,
                                quoting: int, quote_char: str, encoding: str,
                                quality_vector_prefix: str) -> Dict[str, Dict[str, float]]:
    """ Compute a difficulty vector for each t-norm used. A difficulty vector correspond to the sum of all true class's
    % of membership for all quality vectors. It assign a classification difficulty to an example from the reference
    database.
    """
    difficulty_vectors = dict()
    for tnorm_num in range(number_of_tnorms + 1):
        tnorm_name = methodnum_to_str(tnorm_num)

        difficulty_vectors[tnorm_name] =\
            _compute_difficulty_vector(vector_name=quality_vector_prefix + tnorm_name + "." + vector_extension,
                                       number_of_trees=number_of_trees,
                                       subsubtrain_directory_pattern=subsubtrain_directory_pattern,
                                       main_directory=main_directory,
                                       subtrain_directory=subtrain_directory,
                                       delimiter=delimiter,
                                       quoting=quoting,
                                       quote_char=quote_char,
                                       encoding=encoding)
    return difficulty_vectors


def _compute_difficulty_vector(vector_name: str, number_of_trees: int, subsubtrain_directory_pattern: str,
                               main_directory: str, subtrain_directory: str, delimiter: str, quoting: int,
                               quote_char: str, encoding: str) -> Dict[str, float]:
    """ Compute a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true class's % of
    membership for all quality vectors. It assign a classification difficulty to an example from the reference database.
    """
    difficulty_vector = dict()
    for subsubtrain_dir in subsubtrain_dir_path(number_of_trees, main_directory, subtrain_directory,
                                                subsubtrain_directory_pattern):
        quality_vector = _get_quality_vector(vector_path=subsubtrain_dir + "/" + vector_name,
                                             delimiter=delimiter,
                                             quoting=quoting,
                                             quote_char=quote_char,
                                             encoding=encoding,
                                             skip_initial_space=True)

        try:
            difficulty_vector = {instance: difficulty_vector[instance] + quality_vector[instance] for
                                 instance in quality_vector.keys()}
        except KeyError:
            difficulty_vector = {instance: quality_vector[instance] for instance in quality_vector.keys()}
    return difficulty_vector


def _get_quality_vector(vector_path: str, delimiter: str, quoting: int, quote_char: str, encoding: str = "utf8",
                        skip_initial_space: bool = True) -> Dict[str, int]:
    """ Construct an quality vector for one t-norm. An quality vector correspond to a dictionary mapping one instance
    to its true class and all classes found by a tree, along with their % of membership.
    """
    quality_vector = dict()
    with open(vector_path, encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)

        # Extract classes from the header
        classes = next(reader)[2:]
        print(classes)

        for row in reader:
            identifier, true_class, *rest = row
            membership = rest[classes.find(true_class)]
            quality_vector[identifier] = membership

    return quality_vector


def _dump_difficulty_vectors(difficulty_vectors: Dict[str, Dict[str, float]], subtrain_dir_path: str,
                             vector_prefix: str, vector_extension: str, delimiter: str, quoting: int, quote_char: str,
                             encoding: str, skip_initial_space: bool = True) -> True:
    """ Dump all the difficulty vectors into their proper directory. """
    for tnorm_name in difficulty_vectors.keys():
        vector_path = "{}/{}{}.{}".format(subtrain_dir_path, vector_prefix, tnorm_name, vector_extension)
        _dump_difficulty_vector(vector_path=vector_path,
                                difficulty_vector=difficulty_vectors[tnorm_name],
                                delimiter=delimiter,
                                quoting=quoting,
                                quote_char=quote_char,
                                encoding=encoding,
                                skip_initial_space=skip_initial_space)


def _dump_difficulty_vector(vector_path: str, difficulty_vector: Dict[str, float], delimiter: str, quoting: int,
                            quote_char: str, encoding: str = "utf8", skip_initial_space: bool = True) -> None:
    """ Dump the content of a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true
    class's % of membership for all quality vectors. It assign a classification difficulty to an example from the
    reference database.
    """
    with open(vector_path, "w", encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)
        for identifier in difficulty_vector.keys():
            row = [identifier, difficulty_vector[identifier]]
            writer.writerow(row)


if __name__ == "__main__":
    pass
