from typing import Dict, List, Union
import enum

import fforest.src.getters.environment as env
from fforest.src.core.phase.performance_evaluation.clustering_trees_method.clustering_trees_method import \
    ClusteringTreesMethod, UnknownClusteringTreesMethod
from fforest.src.core.phase.performance_evaluation.clustering_trees_method.hypersphere import hypersphere
from fforest.src.core.phase.performance_evaluation.clustering_trees_method.jason_forest import jason_forest
from fforest.src.vrac.file_system import create_dir


_KEY_ID_TREE = "ID_tree"
_KEY_ID_CLUSTER = "ID_cluster"
_KEY_QUALITY = "quality"


@enum.unique
class TreeQuality(enum.IntEnum):
    LOW_QUALITY_TREE = 0
    HIGH_QUALITY_TREE = 1


def clustering_trees() -> None:
    _create_directories(clustering_trees_directories=env.clustering_trees_directories_path,
                        possibles_classes=env.possible_classes)

    clustering_trees = _compute_clustering_trees(clustering_method=env.clustering_trees_method)


def _create_directories(clustering_trees_directories: Dict[str, str], possibles_classes: List[str]) -> None:
    """ Create the directories for the "clustering tree" files, and one directory for each class. """
    for class_name in possibles_classes:
        create_dir(clustering_trees_directories[class_name])


def _compute_clustering_trees(clustering_method: ClusteringTreesMethod)\
        -> Dict[str, Dict[str, List[Dict[str, Union[str, int]]]]]:
    if clustering_method == ClusteringTreesMethod.HYPERSPHERE:
        return hypersphere()
    elif clustering_method == ClusteringTreesMethod.JASON_FOREST:
        return jason_forest()
    else:
        UnknownClusteringTreesMethod(clustering_method.value)



result_example = {
    "yes": {
        "classic": [
            {
                "ID_tree": "bank/subtrain/01_subsubtrain",
                "ID_cluster": 0,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/02_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/03_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            }
        ],
        "luka": [
            {
                "ID_tree": "bank/subtrain/01_subsubtrain",
                "ID_cluster": 0,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/02_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/03_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            }
        ],
        "zadeh": [
            {
                "ID_tree": "bank/subtrain/01_subsubtrain",
                "ID_cluster": 0,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/02_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            },
            {
                "ID_tree": "bank/subtrain/03_subsubtrain",
                "ID_cluster": 1,
                "quality": 0
            }
        ],
    },
    "no": {
        "classic": {

        },
        "luka": {

        },
        "zadeh": {

        }
    }
}