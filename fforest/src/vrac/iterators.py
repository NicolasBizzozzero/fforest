import itertools


def grouper(n: int, iterable: iter, fillvalue=None) -> iter:
    """ Group an iterable by chunks of `n` pieces. Fill the last iterable with `fillvalue` if it's smaller than `n`.
    Shamelessly taken from : https://docs.python.org/3/library/itertools.html#itertools-recipes

        Example:
        >>> for chunk in grouper(3, "ABCDEFG", fillvalue="x"):
        ...     print(chunk)
        ('A', 'B', 'C')
        ('D', 'E', 'F')
        ('G', 'x', 'x')
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def repeat_cycle(iterable: iter, count: int):
    """ Iterate infinitely over elements in iterable, repeated `count` times.

        Example :
        >>> counter = 0
        >>> for char in repeat_cycle("AB", 2):
        ...     print(char)
        ...     counter += 1
        ...     if counter == 8:
        ...         break
        A
        A
        B
        B
        A
        A
        B
        B
    """
    for item in itertools.cycle(iterable):
        for _ in range(count):
            yield item


if __name__ == '__main__':
    pass
