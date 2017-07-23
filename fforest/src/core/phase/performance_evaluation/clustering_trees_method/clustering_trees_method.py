""" This module contains useful tools to manipulate the `Format` class.
This class enumerate methods to produce cluster of fuzzy trees.
"""
import enum


@enum.unique
class ClusteringTreesMethod(enum.IntEnum):
    HYPERSPHERE = 0
    JASON_FOREST = 1


class UnknownClusteringTreesMethod(Exception):
    def __init__(self, method_name: str = "unknown"):
        Exception.__init__(self, "The clustering trees method : \"{method_name}\" doesn't"
                                 " exists".format(method_name=method_name))


def str_to_clusteringtreesmethod(string: str):
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for clustering_method_name, clustering_method_value in zip(ClusteringTreesMethod.__members__.keys(),
                                                               ClusteringTreesMethod.__members__.values()):
        if string == clustering_method_name.lower():
            return clustering_method_value
    raise UnknownClusteringTreesMethod(string)
