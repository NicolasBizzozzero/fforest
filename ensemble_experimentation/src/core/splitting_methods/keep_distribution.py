from typing import Tuple, List

from ensemble_experimentation.src.vrac import is_an_int


def keep_distribution(input_reader, row_limit: int, out_writers, number_of_trees: int, class_name,
                      number_of_rows: int) -> List:
    rows_count = [0 for _ in range(number_of_trees)]
    # We store rows into the distribution dictionary
    distribution_dictionary = dict()

    if is_an_int(class_name):
        class_name = int(class_name)
    for row in input_reader:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_per_db = row_limit / number_of_rows
    # If the class name is an index
    if isinstance(class_name, int):
        for class_name in distribution_dictionary.keys():
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_per_db))
            for index, writer in enumerate(out_writers[:-1]):
                rows_count[index] += rows_to_give
                for _ in range(rows_to_give):
                    writer.writerow(distribution_dictionary[class_name].pop(0))

            # Then the rest to the last writer
            for row in distribution_dictionary[class_name]:
                out_writers[-1].writerow(row)
                rows_count[-1] += 1
    # If it's a name
    else:
        for class_name in distribution_dictionary.keys():
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_per_db))
            for index, writer in enumerate(out_writers[:-1]):
                rows_count[index] += rows_to_give
                for _ in range(rows_to_give):
                    writer.writerow(distribution_dictionary[class_name].pop(0).values())

            # Then the rest to the last writer
            for row in distribution_dictionary[class_name]:
                out_writers[-1].writerow(row.values())
                rows_count[-1] += 1

    return rows_count


def keep_distribution2(content, row_limit, out_writer_train, out_writer_test, class_name, number_of_rows: int) ->\
        Tuple[int, int]:
    row_count_train, row_count_test = 0, 0
    # We store rows into the distribution dictionary
    distribution_dictionary = dict()

    if is_an_int(class_name):
        class_name = int(class_name)
    for row in content:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_train = row_limit / number_of_rows
    # If the class name is an index
    if isinstance(class_name, int):
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0))

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row)
                row_count_test += 1
    # If it's a name
    else:
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0).values())

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row.values())
                row_count_test += 1

    return row_count_train, row_count_test
