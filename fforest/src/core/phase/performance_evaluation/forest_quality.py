""" Compute a quality's forest vector for each triangular norm chosen. A quality's forest vector map each tree of the
forest to its quality. It exists many ways to compute the quality of a tree. Theses quality's forest vectors will be
dumped into the subtrain directory.
"""
from typing import Dict, List

import fforest.src.getters.environment as env
from fforest.src.core.phase.performance_evaluation.quality_computing_method.kappa_rifqi_marsala import kappa_rifqi_marsala
from fforest.src.core.phase.performance_evaluation.quality_computing_method.quality_computing_method import \
    QualityComputingMethod, UnknownQualityComputingMethod
from fforest.src.file_tools.csv_tools import dump_csv_content
from fforest.src.file_tools.dialect import Dialect


def forest_quality() -> None:
    forest_quality_dict = _get_forest_quality(method=env.quality_computing_method)

    import pprint
    pprint.pprint(forest_quality_dict)

    _dump_forest_quality_dict(forest_quality_dict=forest_quality_dict,
                              forest_quality_vectors_path=env.quality_files_paths,
                              dialect=env.dialect_output)


def _get_forest_quality(method: QualityComputingMethod) -> Dict[str, Dict[str, float]]:
    """ Get a forest's quality with a defined method. A forest's quality content map each tree from the forest to its
    quality.
    """
    if method == QualityComputingMethod.KAPPARIFQIMARSALA:
        return kappa_rifqi_marsala()
    else:
        raise UnknownQualityComputingMethod()


def _dump_forest_quality_dict(forest_quality_dict: Dict[str, Dict[str, float]],
                              forest_quality_vectors_path: Dict[str, str], dialect: Dialect) -> None:
    """ Dump the forest's quality vector for all t-norms. A forest's quality content map each tree from the forest to
    its quality.
    """
    for tnorm in forest_quality_dict.keys():
        content = forest_quality_dict[tnorm]
        _dump_forest_quality(content=content,
                             forest_quality_vector_path=forest_quality_vectors_path[tnorm],
                             dialect=dialect)


def _dump_forest_quality(content: Dict[str, float], forest_quality_vector_path: str, dialect: Dialect) -> None:
    """ Dump the forest's quality vector for one t-norm. A forest's quality content map each tree from the forest to
    its quality.
    """
    content = [[tree, quality] for tree, quality in zip(content.keys(), content.values())]
    dump_csv_content(path=forest_quality_vector_path, content=content, dialect=dialect)


if __name__ == "__main__":
    pass
