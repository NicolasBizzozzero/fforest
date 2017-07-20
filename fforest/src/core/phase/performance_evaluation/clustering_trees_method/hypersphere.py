from typing import Iterable, Tuple, Callable

from fforest.src.vrac.maths.norms import euclidean


class HyperSphere:
    """ An HyperSphere, or n-Sphere is a mathematical generalization of the ordinary sphere in spaces of arbitrary
    dimension.

    Inspirations :
        https://en.wikipedia.org/wiki/N-sphere
        http://www.sciencedirect.com/science/article/pii/S0019995862906411

    Attributes :
        - center: Tuple[float]
        - dimension: int
        - radius: float
        - norm: Callable, The norm used to compute distances. Default: euclidean
    """
    def __init__(self, center: Tuple[float], radius: float, norm: Callable = euclidean):
        self.center = center
        self.dimension = len(center)
        self.radius = radius
        self.norm = norm

    def __contains__(self, item: Tuple[float]):
        self._assert_dimension(item)
        return

    def _assert_dimension(self, instance: Tuple[float]):
        assert self.dimension == len(instance)


def hypersphere():
    pass
