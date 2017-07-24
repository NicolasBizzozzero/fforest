from typing import Callable

import numpy as np

from fforest.src.vrac.maths.maths import gamma
from fforest.src.vrac.maths.norms import euclidean


class HyperSphere:
    """ An HyperSphere, or n-Sphere is a mathematical generalization of the ordinary sphere in spaces of arbitrary
    dimension.

    Sources :
        https://en.wikipedia.org/wiki/N-sphere
        http://www.sciencedirect.com/science/article/pii/S0019995862906411

    Attributes :
        - center: np.array[float]
        - dimension: int
        - radius: float
        - norm: Callable, The norm used to compute distances. Default: euclidean
        - volume: float
        - surface: float
    """
    def __init__(self, center, radius: float, norm: Callable = euclidean):
        self.center = np.array(center)
        self.dimension = len(center)
        self.radius = radius
        self.volume = (np.power(np.pi, self.dimension / 2) / gamma((self.dimension / 2) + 1)) * self.radius
        self.surface = (np.power(2 * np.pi, (self.dimension + 1) / 2) / gamma((self.dimension + 1) / 2)) * self.radius
        self.norm = norm

    def __contains__(self, item):
        """
            Example :
            >>> sphere = HyperSphere(center=(1, 2), radius=1)
            >>> vector = (0, 3)
            >>> vector in sphere
            False
            >>> vector = (0, 2)
            >>> vector in sphere
            True
        """
        return self.norm(np.array(item) - self.center) <= self.radius


def hypersphere():
    pass


if __name__ == "__main__":
    pass
