import time
from typing import Callable


def timeit(func: Callable) -> Callable:
    """ Decorator who calculate and print execution time of a function into the standard output. """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Execution time for \"" + str(func.__name__) + "\" : " + str(end - start) + " seconds")
        return result
    return wrapper
