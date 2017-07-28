from typing import Dict, List, Union, Callable, Set

from fforest.src.file_tools.csv_tools import get_header, iter_rows_dict
from fforest.src.file_tools.dialect import Dialect
import fforest.src.getters.environment as env
import numpy as np
from fforest.src.core.phase.performance_evaluation.classes_matrices import KEY_IDENTIFIER
from collections import OrderedDict


def jason_forest() -> Dict[str, Dict[str, List[Dict[str, Union[str, int]]]]]:
    clustering_trees = dict()
    for class_name in env.possible_classes:
        for tnorm_name in env.t_norms_names:
            # TODO: This segment of code can be parallellised
            database = _data_normalization(input_path=env.classes_matrices_files_paths[class_name][tnorm_name],
                                           dialect=env.dialect_output)
            distances_matrix = _compute_distances_matrix(database=database,
                                                         distance_measure=env.distance_measure)
    return clustering_trees


def _data_normalization(input_path: str, dialect: Dialect) -> Dict[str, Dict[str, float]]:
    """ Retrieve a database from a file and normalize its data between the interval [-1, 1]. """
    database = _load_database(file_path=input_path, dialect=dialect)
    for attribute in _get_attributes(file_path=input_path, dialect=dialect):
        mean = _compute_mean(database=database, attribute=attribute)
        print("mean:", mean)
        standard_deviation = _compute_standard_deviation(database=database, attribute=attribute)
        print("sd:", standard_deviation)
        for tree_name in database.keys():
            print("old_value:", database[tree_name][attribute])
            database[tree_name][attribute] = (database[tree_name][attribute] - mean) / standard_deviation
            print("new_value:", database[tree_name][attribute])
    return database


def _load_database(file_path: str, dialect: Dialect) -> Dict[str, Dict[str, float]]:
    """ Load the database located at `file_path` then return a dictionary mapping a tree name with all the attributes,
    and these attributes to the value given by the tree.
    """
    database = dict()
    for row in iter_rows_dict(path=file_path, dialect=dialect):
        tree_name = row[KEY_IDENTIFIER]
        del row[KEY_IDENTIFIER]
        database[tree_name] = OrderedDict(row)
    return database


def _get_attributes(file_path: str, dialect: Dialect) -> List[str]:
    """ Retrieve all the attributes from a CSV file. """
    return get_header(path=file_path, dialect=dialect)[1:]


def _compute_mean(database: Dict[str, Dict[str, float]], attribute: str) -> float:
    """ Compute the mean of all values given by the trees for one attribute """
    return np.mean([database[tree_name][attribute] for tree_name in database.keys()])


def _compute_standard_deviation(database: Dict[str, Dict[str, float]], attribute: str) -> float:
    """ Compute the standard deviatio of all values given by the trees for one attribute """
    return np.std([database[tree_name][attribute] for tree_name in database.keys()])


def _compute_distances_matrix(database: Dict[str, Dict[str, float]], distance_measure: Callable) -> Dict[Set, float]:
    pass
