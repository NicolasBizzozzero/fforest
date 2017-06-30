""" This QCM sum all instances' score, then divide this sum by the number of instances to normalize the result.
An instance's score is the product of its difficulty by the % of membership found by the tree.
"""

from typing import Dict, List

from fforest.src.core.phase.learning_process.forest_construction import KEY_ID, KEY_TRUECLASS, KEY_DIFFICULTY
from fforest.src.file_tools.csv_tools import get_identified_row, iter_rows, get_column
from fforest.src.file_tools.dialect import Dialect
import fforest.src.getters.environment as env


def kappa_rifqi_marsala() -> Dict[str, Dict[str, float]]:
    forest_quality_all_tnorms = dict()
    for tnorm in env.t_norms_names:
        forest_quality_all_tnorms[tnorm] = \
            _get_forest_quality(reference_database_path=env.reference_database_path,
                                subsubtrain_directories_path=env.subsubtrain_directories_path,
                                difficulty_vector_path=env.difficulty_vectors_paths[tnorm],
                                salammbo_vector_paths=env.salammbo_vectors_paths[tnorm],
                                dialect=env.dialect_output)
    return forest_quality_all_tnorms


def _get_forest_quality(reference_database_path: str, subsubtrain_directories_path: str, difficulty_vector_path: str,
                        salammbo_vector_paths: str, dialect: Dialect) -> Dict[str, float]:
    instances_identifiers = get_column(path=reference_database_path, column=0, have_header=False, dialect=dialect)
    forest_quality = dict()
    for tree_index, tree in enumerate(subsubtrain_directories_path):
        forest_quality[tree] = _get_tree_quality(instances_identifiers=instances_identifiers,
                                                 difficulty_vector_path=difficulty_vector_path,
                                                 salammbo_vector_path=salammbo_vector_paths[tree_index],
                                                 dialect=dialect)
    return forest_quality


def _get_tree_quality(difficulty_vector_path: str, salammbo_vector_path: str, instances_identifiers: List[str],
                      dialect: Dialect) -> float:
    return sum(_get_instance_score(instance_identifier=instance,
                                   difficulty_vector_path=difficulty_vector_path,
                                   salammbo_vector_path=salammbo_vector_path,
                                   dialect=dialect) for instance in instances_identifiers) / len(instances_identifiers)


def _get_instance_score(instance_identifier: str, difficulty_vector_path: str, salammbo_vector_path: str,
                        dialect: Dialect) -> float:
    """ Return the score of an instance.
    An instance's score is the product of its difficulty by the % of membership found by the tree.
    """
    true_class = _get_instance_trueclass(instance_identifier=instance_identifier,
                                         salammbo_vector_path=salammbo_vector_path,
                                         dialect=dialect)
    difficulty = _get_instance_difficulty(instance_identifier=instance_identifier,
                                          difficulty_vector_path=difficulty_vector_path,
                                          dialect=dialect)
    membership = _get_instance_membership(instance_identifier=instance_identifier,
                                          salammbo_vector_path=salammbo_vector_path,
                                          true_class=true_class,
                                          dialect=dialect)
    return difficulty * membership


def _get_instance_trueclass(instance_identifier: str, salammbo_vector_path: str, dialect: Dialect) -> str:
    row = get_identified_row(path=salammbo_vector_path,
                             identifier_name=KEY_ID,
                             row_id=instance_identifier,
                             dialect=dialect)
    return row[KEY_TRUECLASS]


def _get_instance_difficulty(instance_identifier: str, difficulty_vector_path: str, dialect: Dialect) -> float:
    row = get_identified_row(path=difficulty_vector_path,
                             identifier_name=KEY_ID,
                             row_id=instance_identifier,
                             dialect=dialect)
    return float(row[KEY_DIFFICULTY])


def _get_instance_membership(instance_identifier: str, salammbo_vector_path: str, true_class: str,
                             dialect: Dialect) -> float:
    row = get_identified_row(path=salammbo_vector_path,
                             identifier_name=KEY_ID,
                             row_id=instance_identifier,
                             dialect=dialect)
    return float(row[true_class])
