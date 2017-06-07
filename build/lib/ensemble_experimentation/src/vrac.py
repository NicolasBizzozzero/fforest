import time


def timeit(func: function) -> function:
    """ Calculate and print execution time of a function into the standard output. """
    def wrapper(*args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print("Execution time for \"" + str(func.func_name) + "\" : " + str(end - start) + " seconds")
        return result
    return wrapper
