from typing import Tuple, List, Union

from ensemble_experimentation.src.vrac.maths import is_an_int


class TooManyTreesToSplit(Exception):
    def __init__(self, number_of_trees, number_of_rows, percentage_per_db):
        Exception.__init__(self, "You can't split {number_of_rows} rows into {number_of_trees} trees with "
                                 "a {percentage_per_db} distribution".format(number_of_trees=number_of_trees,
                                                                             number_of_rows=number_of_rows,
                                                                             percentage_per_db=percentage_per_db))


def keep_distribution(input_reader, row_limit: int, out_writers, number_of_trees: int, class_name: Union[str, int],
                      number_of_rows: int) -> List[int]:
    """ Splits a CSV file into multiple pieces with the `keep_distribution` method.
    The keep_distribution method regroup the database content into its class subgroup. then redistribute each instance
    with the same proportion as the initial content.
    """
    rows_count = [0 for _ in range(number_of_trees)]

    if is_an_int(class_name):
        class_name = int(class_name)

    # We store rows into the distribution dictionary
    distribution_dictionary = dict()
    for row in input_reader:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_per_db = row_limit / number_of_rows
    for class_name in distribution_dictionary.keys():
        rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_per_db))
        for index, writer in enumerate(out_writers[:-1]):
            for _ in range(rows_to_give):
                try:
                    writer.writerow(distribution_dictionary[class_name].pop(0))
                    rows_count[index] += 1
                except IndexError:
                    raise TooManyTreesToSplit(number_of_trees, number_of_rows, percentage_per_db)

        # Then the rest to the last writer
        for row in distribution_dictionary[class_name]:
            out_writers[-1].writerow(row)
            rows_count[-1] += 1

    return rows_count


def keep_distribution2(input_reader, row_limit, out_writer_train, out_writer_test, class_name: Union[str, int],
                       number_of_rows: int) -> Tuple[int, int]:
    """ Splits a CSV file into two pieces with the `keep_distribution` method.
    The keep_distribution method regroup the database content into its class subgroup. then redistribute each instance
    with the same proportion as the initial content.
    """
    row_count_train, row_count_test = 0, 0

    if is_an_int(class_name):
        class_name = int(class_name)

    # We store rows into the distribution dictionary
    distribution_dictionary = dict()
    for row in input_reader:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_train = row_limit / number_of_rows
    for class_name in distribution_dictionary.keys():
        # Distribute to train
        rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
        row_count_train += rows_to_give
        for _ in range(rows_to_give):
            row_to_write = distribution_dictionary[class_name].pop(0)
            out_writer_train.writerow(row_to_write)

        # Then the rest to test
        for row in distribution_dictionary[class_name]:
            out_writer_test.writerow(row)
            row_count_test += 1

    return row_count_train, row_count_test
