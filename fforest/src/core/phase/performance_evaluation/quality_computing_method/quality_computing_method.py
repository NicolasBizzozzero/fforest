import enum


class QualityComputingMethod(enum.IntEnum):
    KAPPARIFQIMARSALA = 0


class UnknownQualityComputingMethod(Exception):
    def __init__(self, method_name: str = "unknown"):
        Exception.__init__(self, "The quality computing method : \"{method_name}\" doesn't"
                                 " exists".format(method_name=method_name))


def str_to_qualitycomputingmethod(string: str):
    string = string.lower()
    if string == "kapparifqimarsala":
        return QualityComputingMethod.KAPPARIFQIMARSALA
    else:
        raise UnknownQualityComputingMethod(string)
