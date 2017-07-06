""" This QCM sum all instances' score, then divide this sum by the number of instances to normalize the result.
An instance's score is the product of its difficulty by the % of membership found by the fuzzy tree.
"""

from typing import Dict, List, Union

from fforest.src.core.phase.learning_process.forest_construction import KEY_ID, KEY_TRUECLASS, KEY_DIFFICULTY
from fforest.src.file_tools.csv_tools import get_identified_row, get_column, get_columns, iter_rows, iter_rows_dict
from fforest.src.file_tools.dialect import Dialect
import fforest.src.getters.environment as env
from fforest.src.vrac.decorators import timeit


KEY_MEMBERSHIP = "%membership"


# TODO: Check if salammbo and difficulty vectors have headers
# TODO: _load_instances_id_and_trueclass can probably be removed


def kappa_rifqi_marsala() -> Dict[str, Dict[str, float]]:

    # Load instances information to limit the number of access to the files
    instances = _load_instances_id_and_trueclass(
        salammbo_vector_path=env.salammbo_vectors_paths.values()[0][0], # Get one salammbo vector path, the instances ID
                                                                        # and true_class are the same everywhere.
        dialect=env.dialect_output)

    forest_quality_all_tnorms = dict()
    for tnorm in env.t_norms_names:
        _load_instances_difficulty(difficulty_vector_path=env.difficulty_vectors_paths[tnorm],
                                   instances=instances,
                                   dialect=env.dialect_output)

        forest_quality_all_tnorms[tnorm] = \
            _get_forest_quality(reference_database_path=env.reference_database_path,
                                subsubtrain_directories_path=env.subsubtrain_directories_path,
                                salammbo_vector_paths=env.salammbo_vectors_paths[tnorm],
                                dialect=env.dialect_output)
    return forest_quality_all_tnorms


def _load_instances_id_and_trueclass(salammbo_vector_path: str, dialect: Dialect) -> Dict[str, Dict[str, str]]:
    """ Get the instances' identifiers and true class from a salammbo vector.
    The vector in itself doesn't mater, as they all contains the same identifiers with the same true classes.
    """
    instances = dict()
    for identifier, true_class in get_columns(path=salammbo_vector_path,
                                              columns=[KEY_ID, KEY_TRUECLASS],
                                              have_header=True,
                                              dialect=dialect):
        instances[identifier] = {KEY_TRUECLASS: true_class,
                                 KEY_DIFFICULTY: None,
                                 KEY_MEMBERSHIP: None}
    return instances


def _load_instances_difficulty(difficulty_vector_path: str, instances: Dict[str, Dict[str, str]],
                               dialect: Dialect) -> None:
    """ Get the instances' difficulty from their difficulty vector. """
    for identifier, difficulty in get_columns(path=difficulty_vector_path,
                                              columns=[KEY_ID, KEY_DIFFICULTY],
                                              have_header=True,
                                              dialect=dialect):
        instances[identifier][KEY_DIFFICULTY] = float(difficulty)


def _load_instances_membership(salammbo_vector_path: str, instances: Dict[str, Dict[str, str]], true_class: str,
                               dialect: Dialect) -> None:
    """ Get the instances' membership from their salammbo vector. """
    for row in iter_rows_dict(path=salammbo_vector_path, dialect=dialect):
        identifier, true_class = row[KEY_ID], row[KEY_TRUECLASS]
        membership = row[true_class]
        instances[identifier][KEY_MEMBERSHIP] = membership

    for identifier, membership in get_columns(path=salammbo_vector_path,
                                              columns=[KEY_ID, true_class],
                                              have_header=True,
                                              dialect=dialect):
        instances[identifier][KEY_MEMBERSHIP] = float(membership)


def _get_forest_quality(instances: Dict[str, Dict[str, Union[str, float]]], subsubtrain_directories_path: str,
                        salammbo_vector_paths: str, dialect: Dialect) -> Dict[str, float]:
    """ Compute the forest quality.
    Return a dictionary mapping each forest's path to their quality.
    """
    forest_quality = dict()
    for tree_path in subsubtrain_directories_path:
        _load_instances_membership(salammbo_vector_path=,
                                   instances=instances,
                                   true_class=,
                                   dialect=dialect)
        forest_quality[tree_path] = _get_tree_quality(instances=instances)
    return forest_quality


def _get_tree_quality(instances: Dict[str, Dict[str, Union[str, float]]]) -> float:
    """ Return the quality of a tree.
    The quality of a tree, as defined by the Kappa-Rifqi-Marsala method, is the sum of the score of all instances
    divided by the number of instances (to normalize the result).
    """
    return sum(_get_instance_score(difficulty=instances[identifier][KEY_DIFFICULTY],
                                   membership=instances[identifier][KEY_MEMBERSHIP]) for
               identifier in instances.keys()) / len(instances)


def _get_instance_score(difficulty: float, membership: float) -> float:
    """ Return the score of an instance.
    An instance's score is the product of its difficulty by the % of membership found by the tree.
    """
    return difficulty * membership


def _get_instance_membership(instance_identifier: str, salammbo_vector_path: str, true_class: str,
                             dialect: Dialect) -> float:
    row = get_identified_row(path=salammbo_vector_path,
                             identifier_name=KEY_ID,
                             row_id=instance_identifier,
                             dialect=dialect)
    return float(row[true_class])
