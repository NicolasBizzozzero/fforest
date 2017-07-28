from typing import Dict, List, Union, Callable, Set

from fforest.src.file_tools.csv_tools import get_header, iter_rows_dict
from fforest.src.file_tools.dialect import Dialect
import fforest.src.getters.environment as env
import numpy as np
from fforest.src.core.phase.performance_evaluation.classes_matrices import KEY_IDENTIFIER
from collections import OrderedDict
from fforest.src.vrac.maths.distance_measure import euclidean


def jason_forest() -> Dict[str, Dict[str, List[Dict[str, Union[str, int]]]]]:
    clustering_trees = dict()
    for class_name in env.possible_classes:
        for tnorm_name in env.t_norms_names:
            # TODO: This segment of code can be parallellised
            database = _data_normalization(input_path=env.classes_matrices_files_paths[class_name][tnorm_name],
                                           dialect=env.dialect_output)
            distances_matrix = _compute_distances_matrix(database=database,
                                                         #TODO: Implement this parameter
                                                         #distance_measure=env.distance_measure)
                                                         distance_measure=euclidean)
            print(distances_matrix)
    return clustering_trees


def _data_normalization(input_path: str, dialect: Dialect, useless_value: float = 0.0) -> Dict[str, Dict[str, float]]:
    """ Retrieve a database from a file and normalize its data between the interval [-1, 1]. """
    database = _load_database(file_path=input_path, dialect=dialect)
    for attribute in _get_attributes(file_path=input_path, dialect=dialect):
        mean = _compute_mean(database=database, attribute=attribute)
        standard_deviation = _compute_standard_deviation(database=database, attribute=attribute)
        if standard_deviation == 0.0:
            # This attribute is useless because all the instances have the same values for it
            for tree_name in database.keys():
                database[tree_name][attribute] = useless_value
        else:
            for tree_name in database.keys():
                database[tree_name][attribute] = (database[tree_name][attribute] - mean) / standard_deviation
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


def _compute_distances_matrix(database: Dict[str, Dict[str, float]], distance_measure: Callable)\
        -> Dict[str, Dict[frozenset, float]]:
    distances_matrix = {tree_name: dict() for tree_name in database.keys()}
    for tree_name in database.keys():
        # Compute the semi distance matrix for each tree
        for i_attribute1, attribute1 in enumerate(database[tree_name].keys()):
            for i_attribute2 in range(i_attribute1, len(database[tree_name].keys())):
                attribute2 = list(database[tree_name].keys())[i_attribute2]
                distances_matrix[tree_name][frozenset([attribute1, attribute2])] = \
                    distance_measure(database[tree_name][attribute1], database[tree_name][attribute2])
    return distances_matrix


#TODO: Delete this when the algorithm is working
def jason_forest():
    pass


if __name__ == "__main__":
    pass
