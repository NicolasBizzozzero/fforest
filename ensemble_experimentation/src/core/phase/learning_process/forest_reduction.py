import csv
from typing import Dict

import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.phase.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.vrac.iterators import subsubtrain_dir_path


def forest_reduction() -> None:
    _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                number_of_tnorms=env.t_norms,
                                subtrain_dir_path="{}/{}".format(env.original_database_name, env.subtrain_directory),
                                subsubtrain_directory_pattern=env.subsubtrain_directory_pattern,
                                vector_prefix=env.difficulty_vector_prefix,
                                vector_extension=env.vector_file_extension,
                                main_directory=env.main_directory,
                                subtrain_directory=env.subtrain_directory,
                                delimiter=env.delimiter_output,
                                quoting=env.quoting_output,
                                quote_char=env.quote_character_output,
                                encoding=env.encoding_output,
                                quality_vector_prefix=env.quality_vector_prefix)


def _compute_difficulty_vectors(number_of_trees: int, number_of_tnorms: int, subtrain_dir_path: str,
                                subsubtrain_directory_pattern: str, vector_prefix: str, vector_extension: str,
                                main_directory: str, subtrain_directory: str, delimiter: str, quoting: int,
                                quote_char: str, encoding: str, quality_vector_prefix: str) -> None:
    """ Compute a difficulty vector for each t-norm used. A difficulty vector correspond to the sum of all quality
    vectors for a t-norm. It assign a classification difficulty to an example from the reference database.
    """
    for tnorm_num in range(number_of_tnorms + 1):
        tnorm_name = methodnum_to_str(tnorm_num)
        vector_path = "{}/{}{}.{}".format(subtrain_dir_path, vector_prefix, tnorm_name, vector_extension)

        _compute_difficulty_vector(vector_name=quality_vector_prefix + tnorm_name + "." + vector_extension,
                                   vector_path=vector_path,
                                   number_of_trees=number_of_trees,
                                   subsubtrain_directory_pattern=subsubtrain_directory_pattern,
                                   main_directory=main_directory,
                                   subtrain_directory=subtrain_directory,
                                   delimiter=delimiter,
                                   quoting=quoting,
                                   quote_char=quote_char,
                                   encoding=encoding)


def _compute_difficulty_vector(vector_name: str, vector_path: str, number_of_trees: int,
                               subsubtrain_directory_pattern: str, main_directory: str, subtrain_directory: str,
                               delimiter: str, quoting: int, quote_char: str, encoding: str) -> None:
    """ Compute a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all quality vectors for
    a t-norm. It assign a classification difficulty to an example from the reference database.
    """
    difficulty_vector = dict()
    for subsubtrain_dir in subsubtrain_dir_path(number_of_trees, main_directory, subtrain_directory,
                                                subsubtrain_directory_pattern):
        efficiency_vector = _get_efficiency_vector(vector_path=subsubtrain_dir + "/" + vector_name,
                                                   delimiter=delimiter,
                                                   quoting=quoting,
                                                   quote_char=quote_char,
                                                   encoding=encoding,
                                                   skip_initial_space=True)

        try:
            difficulty_vector = {instance: difficulty_vector[instance] + efficiency_vector[instance] for
                                 instance in efficiency_vector.keys()}
        except KeyError:
            difficulty_vector = {instance: efficiency_vector[instance] for instance in efficiency_vector.keys()}

    _dump_difficulty_vector(vector_path=vector_path,
                            difficulty_vector=difficulty_vector,
                            delimiter=delimiter,
                            quoting=quoting,
                            quote_char=quote_char,
                            encoding=encoding,
                            skip_initial_space=True)


def _get_efficiency_vector(vector_path: str, delimiter: str, quoting: int, quote_char: str, encoding: str = "utf8",
                           skip_initial_space: bool = True) -> Dict[str, int]:
    """ Compute an efficiency vector for one t-norm. An efficiency vector correspond to dictionary mapping one instance
    to a boolean. True if this instance as been correctly classified by the t-norm, False otherwise.
    """
    efficiency_vector = dict()
    with open(vector_path, encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)
        for row in reader:
            identifier, correctly_classified = row
            efficiency_vector[identifier] = 1 if correctly_classified else 0

    return efficiency_vector


def _dump_difficulty_vector(vector_path: str, difficulty_vector: Dict[str, int], delimiter: str, quoting: int,
                            quote_char: str, encoding: str = "utf8", skip_initial_space: bool = True) -> None:
    """ Dump the content of a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all quality
    vectors for a t-norm. It assign a classification difficulty to an example from the reference database.
    """
    with open(vector_path, "w", encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)
        for identifier in difficulty_vector.keys():
            row = [identifier, difficulty_vector[identifier]]
            writer.writerow(row)


if __name__ == "__main__":
    pass
