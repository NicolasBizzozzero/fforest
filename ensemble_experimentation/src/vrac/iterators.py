import itertools


def grouper(n: int, iterable: iter, fillvalue=None) -> iter:
    """ Group an iterable by chunks of `n` pieces. Fill the last iterable with `fillvalue` if it's smaller than `n`.
    Taken from

    Example:
    >>> for chunk in grouper(3, "ABCDEFG", fillvalue="x"):
     ...    print(chunk)
    ('A', 'B', 'C')
    ('D', 'E', 'F')
    ('G', 'x', 'x')
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


if __name__ == '__main__':
    # Null ALGO REALCLASS [(CLASS PROBABILITY) (CLASS PROBABILITY) ...]
    lines = """Null 0 1 2 1 1.00000
    Null 1 2 2 1 0.8979 2 0.0014 3 0.00012
    Null 2 3 1 1 0.883 2 0.091092 3 0.00092"""


    result = dict()
    number_of_algorithms = 3
    for algorithms_chunk in grouper(number_of_algorithms, lines.split("\n")):
        for instance in algorithms_chunk:
            _, algorithm, identifier, real_class, *rest = instance.split()
            result[identifier] = dict()
            result[identifier]["class"] = real_class
            result[identifier]["algorithm_" + str(algorithm)] = {class_found: float(probability) for class_found, probability in grouper(2, rest)}

    assert result == \
    {
        '1': {
            'algorithm_0': {
                '1': 1.00000
            },
            'class': '2'
        },
        '2': {
            'algorithm_1': {
                '1': 0.8979,
                '2': 0.0014,
                '3': 0.00012
            },
           'class': '2'
        },
        '3': {
            'algorithm_2': {
                '1': '0.883',
                '2': '0.091092',
                '3': '0.00092'
            },
           'class': '1'
        }
    }