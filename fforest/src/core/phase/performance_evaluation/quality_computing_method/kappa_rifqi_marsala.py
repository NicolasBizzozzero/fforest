""" This QCM sum all instances' score, then divide this sum by the number of instances to normalize the result.
An instance score is the product of its difficulty by the % of membership found by the tree.
"""

from typing import Dict


def kappa_rifqi_marsala() -> Dict[str, Dict[str, float]]:
    pass


def _get_instance_score(instance_identifier: str, difficulty_vector_path: str, quality_vector_path: str):
    pass


def _get_instance_difficulty(instance_identifier: str, difficulty_vector_path: str) -> float:
    row = get_identified_row(difficulty_vector_path, KEY_ID, instance_identifier, delimiter=";", quoting=2, quote_character= "\"", encoding="utf8")
    trueclass = row[KEY_TRUECLASS]
    return float(row[trueclass])