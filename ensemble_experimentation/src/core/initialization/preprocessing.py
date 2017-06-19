import csv

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.file_tools.csv_tools import iter_rows, get_number_of_columns, preprend_column,\
    append_column, find_index_for_class
from ensemble_experimentation.src.getters.get_output_message import Message, vprint
from ensemble_experimentation.src.vrac.file_system import create_dir, extract_first_line, dump_string
from ensemble_experimentation.src.vrac.maths import is_an_int


class NamedAttributeButNoHeader(Exception):
    def __init__(self):
        Exception.__init__(self, "Impossible to access a named attribute with no header")


def _add_id(input_path: str, output_path: str, id_name: str, have_header: bool, delimiter: str) -> None:
    """ Add an identificator for each instance into the database.
    If the parameter id_name is provided, it'll be inserted as a header of the output_file.
    """
    with open(input_path) as input_file, open(output_path, "w") as output_file:
        output_writer = csv.writer(output_file, delimiter=delimiter)
        input_reader = csv.reader(input_file, delimiter=delimiter)

        if have_header:
            header = next(input_reader)
            header.insert(0, id_name)
            output_writer.writerow(header)

        for row_index, row in enumerate(input_reader):
            if row:
                row.insert(0, row_index)
                output_writer.writerow(row)


def _identifier_at_beginning(path: str, identifier: str):
    if is_an_int(identifier):
        return int(identifier) == 0

    if not env.cleaned_arguments[gpn.have_header()]:
        raise NamedAttributeButNoHeader()
    else:
        header = next(iter_rows(path, delimiter=env.cleaned_arguments[gpn.delimiter()],
                                encoding=env.cleaned_arguments[gpn.encoding()]))
        return header[0] == identifier


def _class_at_end(path: str, class_name: str):
    if is_an_int(class_name):
        return int(class_name) == -1 or \
               int(class_name) == get_number_of_columns(path, delimiter=env.cleaned_arguments[gpn.delimiter()],
                                                        encoding=env.cleaned_arguments[gpn.encoding()]) - 1

    if not env.cleaned_arguments[gpn.have_header()]:
        raise NamedAttributeButNoHeader()
    else:
        header = next(iter_rows(path, delimiter=env.cleaned_arguments[gpn.delimiter()],
                                encoding=env.cleaned_arguments[gpn.encoding()]))
        return header[-1] == class_name


def _extract_header(input_path: str, header_path: str, encoding: str = "utf8"):
    header = extract_first_line(input_path, encoding=encoding)
    dump_string(header_path, header)


def preprocessing() -> None:
    """ Prepare the original database to be processed. """
    env.initial_split_input_path = env.statistics[gsn.database_path()]

    # Create the main directory of the application
    create_dir(env.cleaned_arguments[gpn.main_directory()])

    # Check if the database contains an identifier column
    if env.cleaned_arguments[gpn.identifier()] is None:
        _add_id(input_path=env.cleaned_arguments[gpn.database()],
                output_path=env.statistics[gsn.preprocessed_database_path()],
                id_name=gdv.identifier(), have_header=env.cleaned_arguments[gpn.have_header()],
                delimiter=env.cleaned_arguments[gpn.delimiter()])
        env.cleaned_arguments[gpn.identifier()] = gdv.identifier()

        # Change the database path to the modified database
        env.initial_split_input_path = env.statistics[gsn.preprocessed_database_path()]

    # Check if the identifier column is at the beginning of the database
    if not _identifier_at_beginning(env.initial_split_input_path, env.cleaned_arguments[gpn.identifier()]):
        vprint(Message.PREPEND_ID)
        preprend_column(input_path=env.initial_split_input_path,
                        output_path=env.statistics[gsn.preprocessed_database_path()],
                        column=env.cleaned_arguments[gpn.identifier()],
                        encoding=env.cleaned_arguments[gpn.encoding()],
                        delimiter=env.cleaned_arguments[gpn.delimiter()])

        # The identifier is now a the beginning of the database, we change it to the index 0
        env.cleaned_arguments[gpn.identifier()] = "0"

        # Change the database path to the modified database
        env.initial_split_input_path = env.statistics[gsn.preprocessed_database_path()]

    # Check if the class column is at the end of the database
    if not _class_at_end(env.initial_split_input_path, env.cleaned_arguments[gpn.class_name()]):
        vprint(Message.APPEND_CLASS)
        append_column(input_path=env.initial_split_input_path,
                      output_path=env.statistics[gsn.preprocessed_database_path()],
                      column=env.cleaned_arguments[gpn.class_name()],
                      encoding=env.cleaned_arguments[gpn.encoding()],
                      delimiter=env.cleaned_arguments[gpn.delimiter()])

        # The class column is now a the end of the database, we change it to the index -1
        env.cleaned_arguments[gpn.class_name()] = str(get_number_of_columns(env.initial_split_input_path,
                                                                            delimiter=env.cleaned_arguments[gpn.delimiter()],
                                                                            encoding=env.cleaned_arguments[gpn.encoding()]) - 1)

        # Change the database path to the modified database
        env.initial_split_input_path = env.statistics[gsn.preprocessed_database_path()]

    # Check if the database have a header
    if env.cleaned_arguments[gpn.have_header()]:
        vprint(Message.EXTRACT_HEADER)

        header_path = env.cleaned_arguments[gpn.main_directory()] + "/" + env.cleaned_arguments[gpn.header_name()] + "." + env.cleaned_arguments[gpn.header_extension()]
        _extract_header(input_path=env.initial_split_input_path,
                        header_path=header_path,
                        encoding=env.cleaned_arguments[gpn.encoding()])

        # The header have been extracted, we store its path
        env.statistics[gsn.header_path()] = header_path
        env.cleaned_arguments[gpn.class_name()] = find_index_for_class(header_path,
                                                                       env.cleaned_arguments[gpn.class_name()],
                                                                       delimiter=env.cleaned_arguments[gpn.delimiter()])
        env.cleaned_arguments[gpn.have_header()] = False


if __name__ == '__main__':
    pass
