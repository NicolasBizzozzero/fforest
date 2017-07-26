from typing import Dict, List, Union

from fforest.src.file_tools.csv_tools import get_header
from fforest.src.file_tools.dialect import Dialect
import fforest.src.getters.environment as env
import numpy as np


def jason_forest() -> Dict[str, Dict[str, List[Dict[str, Union[str, int]]]]]:
    clustering_trees = dict()
    for class_name in env.possible_classes:
        for tnorm_name in env.t_norms_names:
            _data_normalization(file_path=, output_path=, dialect=env.dialect_output)
    return clustering_trees


def _data_normalization(file_path: str, output_path: str, dialect: Dialect) -> None:
    matrix = _load_matrix(file_path=file_path, dialect=dialect)
    for attribute in _get_attributes(file_path=file_path, dialect=dialect):
        mean = _compute_mean(matrix=matrix, attribute=attribute)
        standard_deviation = _compute_standard_deviation(matrix=matrix, attribute=attribute, mean=mean)
        for tree_name in matrix.keys():
            matrix[tree_name][attribute] = (matrix[tree_name][attribute] - mean) / standard_deviation
    _dump_matrix(matrix=matrix, output_path=output_path)


def _load_matrix(file_path: str, dialect: Dialect) -> Dict[str, Dict[str, float]]:
    """ Load the matrix located at `file_path` then return a dictionary mapping a tree name with all the attributes, and
    these attributes to the value given by the tree.
    """
    pass


def _get_attributes(file_path: str, dialect: Dialect) -> List[str]:
    """ Retrieve all the attributes from a CSV file. """
    return get_header(path=file_path, dialect=dialect)[1:]


def _compute_mean(matrix: Dict[str, Dict[str, float]], attribute: str) -> float:
    """ Compute the mean of all values given by the trees for one attribute """
    return np.mean(matrix[tree_name][attribute] for tree_name in matrix.keys())


def _compute_standard_deviation(matrix: Dict[str, Dict[str, float]], attribute: str, mean: float) -> float:
    pass


def _dump_matrix(matrix: Dict[str, Dict[str, float]], output_path: str) -> None:
    pass
