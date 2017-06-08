import csv
import ensemble_experimentation.src.getters.get_default_value as gdv


def _add_id(input_path: str, output_path: str, id_name: str, keep_header: bool, delimiter: str = ','):
    """ Add an identificator for each instance into the database.
    If the parameter id_name is provided, it'll be inserted as a header of the output_file.
    """
    with open(input_path) as input_file, open(output_path, "w") as output_file:
        output_writer = csv.writer(output_file)
        input_reader = csv.reader(input_file, delimiter=delimiter)

        if keep_header:
            header = next(input_reader)
            header.insert(0, id_name)
            output_writer.writerow(header)

        for row_index, row in enumerate(input_reader):
            if row:
                row.insert(0, row_index)
                output_writer.writerow(row)


def preprocessing(*, input_path: str, output_path: str, identificator: str, keep_header: bool, delimiter: str = ','):
    if identificator is None:
        # We must add an identificator column
        _add_id(input_path=input_path, output_path=output_path, id_name=gdv.identificator(), keep_header=keep_header,
                delimiter=delimiter)
        return output_path
    return input_path


if __name__ == '__main__':
    pass
