""" Compute one difficulty vector for each triangular norm used. A difficulty vector correspond to the sum of all true
class's % of membership for all salammbo vectors. It assign a classification difficulty to an example from the reference
database. Theses difficulty vectors will be dumped into the subtrain directory.
"""

from typing import Dict, List

import fforest.src.getters.environment as env
from fforest.src.file_tools.csv_tools import iter_rows, get_header, dump_csv_content
from fforest.src.vrac.maths import round_float
from fforest.src.file_tools.dialect import Dialect


def forest_reduction() -> None:
    """ Compute one difficulty vector for each triangular norm used. A difficulty vector correspond to the sum of all
    true class's % of membership for all salammbo vectors. It assign a classification difficulty to an example from the
    reference database. Theses difficulty vectors will be dumped into the subtrain directory.
    """
    difficulty_vectors = \
        _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                    salammbo_vectors_dict=env.salammbo_vectors_paths,
                                    dialect=env.dialect_output)

    _dump_difficulty_vectors(difficulty_vectors=difficulty_vectors,
                             difficulty_vectors_paths=env.difficulty_vectors_paths,
                             dialect=env.dialect_output)


def _compute_difficulty_vectors(number_of_trees: int, salammbo_vectors_dict: Dict[str, List],
                                dialect: Dialect) -> Dict[str, Dict[str, float]]:
    """ Compute a difficulty vector for each t-norm used. A difficulty vector correspond to the sum of all true class's
    % of membership for all salammbo vectors. It assign a classification difficulty to an example from the reference
    database.
    """
    difficulty_vectors = dict()
    for tnorm in salammbo_vectors_dict.keys():
        difficulty_vectors[tnorm] =\
            _compute_difficulty_vector(salammbo_vectors_paths=salammbo_vectors_dict[tnorm],
                                       number_of_trees=number_of_trees,
                                       dialect=dialect)
    return difficulty_vectors


def _compute_difficulty_vector(salammbo_vectors_paths: List[str], number_of_trees: int,
                               dialect: Dialect) -> Dict[str, float]:
    """ Compute a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true class's % of
    membership for all salammbo vectors. It assign a classification difficulty to an example from the reference
    database.
    """
    difficulty_vector = dict()
    for vector_path in salammbo_vectors_paths:
        salammbo_vector = _get_salammbo_vector(vector_path=vector_path, number_of_trees=number_of_trees,
                                               dialect=dialect)

        try:
            difficulty_vector = {instance: difficulty_vector[instance] + salammbo_vector[instance] for
                                 instance in salammbo_vector.keys()}
        except KeyError:
            difficulty_vector = {instance: salammbo_vector[instance] for instance in salammbo_vector.keys()}

    # Round wrong floating values
    for instance in difficulty_vector.keys():
        difficulty_vector[instance] = round_float(difficulty_vector[instance])
    return difficulty_vector


def _get_salammbo_vector(vector_path: str, number_of_trees: int, dialect: Dialect) -> Dict[str, int]:
    """ Construct an salammbo vector for one t-norm. A salammbo vector correspond to a dictionary mapping one instance
    to its true class and all classes found by a tree, along with their % of membership.
    """
    salammbo_vector = dict()

    # Extract classes from the header
    classes = get_header(path=vector_path, dialect=dialect)[2:]

    for row in iter_rows(path=vector_path, skip_header=True, dialect=dialect):
        identifier, true_class, *rest = row
        membership = rest[classes.index(true_class)]
        salammbo_vector[identifier] = membership / number_of_trees

    return salammbo_vector


def _dump_difficulty_vectors(difficulty_vectors: Dict[str, Dict[str, float]], difficulty_vectors_paths: Dict[str, str],
                             dialect: Dialect) -> None:
    """ Dump all the difficulty vectors into their proper directory. """
    for tnorm in difficulty_vectors.keys():
        _dump_difficulty_vector(vector_path=difficulty_vectors_paths[tnorm],
                                difficulty_vector=difficulty_vectors[tnorm],
                                dialect=dialect)


def _dump_difficulty_vector(vector_path: str, difficulty_vector: Dict[str, float], dialect: Dialect) -> None:
    """ Dump the content of a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true
    class's % of membership for all salammbo vectors. It assign a classification difficulty to an example from the
    reference database.
    """
    content = [[identifier, difficulty_vector[identifier]] for identifier in difficulty_vector.keys()]
    dump_csv_content(path=vector_path, content=content, dialect=dialect)


if __name__ == "__main__":
    pass
