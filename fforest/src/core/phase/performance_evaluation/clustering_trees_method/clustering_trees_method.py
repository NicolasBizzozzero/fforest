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
    string = string.lower()
    if string == "hypersphere":
        return ClusteringTreesMethod.HYPERSPHERE
    elif string == "jason_forest":
        return ClusteringTreesMethod.JASON_FOREST
    else:
        raise UnknownClusteringTreesMethod(string)
