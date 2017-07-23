""" This QCM sum all instances' score, then divide this sum by the number of instances to normalize the result.
An instance's score is the product of its difficulty by the % of membership found by the fuzzy tree.
"""

from typing import Dict, Union

import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.forest_construction import KEY_ID, KEY_TRUECLASS, KEY_DIFFICULTY
from fforest.src.file_tools.csv_tools import get_columns, iter_rows_dict
from fforest.src.file_tools.dialect import Dialect

KEY_MEMBERSHIP = "%membership"


def kappa_rifqi_marsala() -> Dict[str, Dict[str, float]]:
    forest_quality_all_tnorms = dict()
    for tnorm in env.t_norms_names:
        instances = _load_instances_difficulty(difficulty_vector_path=env.difficulty_vectors_paths[tnorm],
                                               dialect=env.dialect_output)

        forest_quality_all_tnorms[tnorm] = \
            _get_forest_quality(instances=instances,
                                subsubtrain_directories_path=env.subsubtrain_directories_path,
                                salammbo_vector_paths=env.salammbo_vectors_paths[tnorm],
                                dialect=env.dialect_output)
    return forest_quality_all_tnorms


def _load_instances_difficulty(difficulty_vector_path: str, dialect: Dialect) -> Dict[str, Dict[str, float]]:
    """ Get the instances' difficulty from their difficulty vector. """
    instances = dict()
    for identifier, difficulty in get_columns(path=difficulty_vector_path,
                                              columns=[KEY_ID, KEY_DIFFICULTY],
                                              have_header=True,
                                              dialect=dialect):
        instances[identifier] = dict()
        instances[identifier][KEY_DIFFICULTY] = float(difficulty)
    return instances


def _get_forest_quality(instances: Dict[str, Dict[str, Union[str, float]]], subsubtrain_directories_path: str,
                        salammbo_vector_paths: str, dialect: Dialect) -> Dict[str, float]:
    """ Compute the forest quality.
    Return a dictionary mapping each forest's path to their quality.
    """
    forest_quality = dict()
    for tree_index, tree_path in enumerate(subsubtrain_directories_path):
        _load_instances_membership(salammbo_vector_path=salammbo_vector_paths[tree_index],
                                   instances=instances,
                                   dialect=dialect)
        forest_quality[tree_path] = _get_tree_quality(instances=instances)
    return forest_quality


def _load_instances_membership(salammbo_vector_path: str, instances: Dict[str, Dict[str, float]],
                               dialect: Dialect) -> None:
    """ Get the instances' membership from their salammbo vector. """
    global KEY_MEMBERSHIP

    for row in iter_rows_dict(path=salammbo_vector_path, dialect=dialect):
        identifier, true_class = row[KEY_ID], row[KEY_TRUECLASS]
        membership = row[true_class]
        instances[identifier][KEY_MEMBERSHIP] = float(membership)


def _get_tree_quality(instances: Dict[str, Dict[str, Union[str, float]]]) -> float:
    """ Return the quality of a tree.
    The quality of a tree, as defined by the Kappa-Rifqi-Marsala method, is the sum of the score of all instances
    divided by the number of instances (to normalize the result).
    """
    global KEY_MEMBERSHIP

    return sum(_get_instance_score(difficulty=instances[identifier][KEY_DIFFICULTY],
                                   membership=instances[identifier][KEY_MEMBERSHIP]) for
               identifier in instances.keys()) / len(instances)


def _get_instance_score(difficulty: float, membership: float) -> float:
    """ Return the score of an instance.
    An instance's score is the product of its difficulty by the % of membership found by the tree.
    """
    return difficulty * membership
