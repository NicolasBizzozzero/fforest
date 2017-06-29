""" The only method called from outside this module should be `preprocessing`.
It'll backup the original database into a database called `preprocessed_database`, then'll clean this new database by
applying a set of operations on it. Theses operations consist of :
- Change its encoding, delimiter, format, quote character, quoting behavior and newline delimiter.
- Add an ID column if it's not already present.
- Move the ID column at the beginning of the database.
- Move the class column at the end of the database.
- Extract the header if it's present.
"""
import csv

import fforest.src.getters.environment as env
import fforest.src.getters.get_default_value as gdv
from fforest.src.file_tools.csv_tools import get_number_of_columns, preprend_column, append_column,\
    NamedAttributeButNoHeader, EmptyHeader, dump_content, get_header
from fforest.src.getters.get_output_message import Message, vprint
from fforest.src.vrac.file_system import create_dir, extract_first_line, dump_string
from fforest.src.vrac.maths import is_an_int
from fforest.src.file_tools.dialect import Dialect


def preprocessing() -> None:
    """ Prepare the original database to be processed.
    It'll backup the original database into a database called `preprocessed_database`, then'll clean this new database
    by applying a set of operations on it. Theses operations consist of :
        - Change its encoding, delimiter, format, quote character, quoting behavior and newline delimiter.
        - Add an ID column if it's not already present.
        - Move the ID column at the beginning of the database.
        - Move the class column at the end of the database.
        - Extract the header if it's present.
    """
    # Create the main directory of the application
    create_dir(env.main_directory_path)

    # Change the encoding, delimiter, format, quoting behavior and quoting character of the original
    # database to initialize the preprocessed database. Once it's done, we can forget about the original database.
    vprint(Message.INITIAL_PREPROCESSING)
    _init_preprocessed_database(original_database_path=env.original_database_path,
                                preprocessed_database_path=env.preprocessed_database_path,
                                input_encoding=env.encoding_input,
                                output_encoding=env.encoding_output,
                                input_delimiter=env.delimiter_input,
                                output_delimiter=env.delimiter_output,
                                input_format=env.format_input,
                                output_format=env.format_output,
                                input_quote_char=env.quote_character_input,
                                output_quote_char=env.quote_character_output,
                                input_quoting=env.quoting_input,
                                output_quoting=env.quoting_output,
                                input_line_delimiter=env.line_delimiter_input,
                                output_line_delimiter=env.line_delimiter_output)

    # Check if the database contains an identifier column
    if env.identifier is None:
        vprint(Message.ADD_ID)
        _add_id(input_path=env.preprocessed_database_path,
                output_path=env.preprocessed_database_path,
                id_name=gdv.identifier(),
                have_header=env.have_header,
                dialect=env.dialect)

        # An header as been added
        env.have_header = True

        # The default identifier column is always added at the first index
        env.identifier = 0

        # The class name's index must obviously be shifted to the right
        if env.class_name >= 0:
            env.class_name += 1

    # Check if the identifier column is at the beginning of the database
    if not _identifier_at_beginning(path=env.preprocessed_database_path,
                                    have_header=env.have_header,
                                    identifier=env.identifier,
                                    dialect=env.dialect):
        vprint(Message.PREPEND_ID)
        preprend_column(input_path=env.preprocessed_database_path,
                        output_path=env.preprocessed_database_path,
                        column=env.identifier,
                        dialect=env.dialect)

        # The identifier is now a the beginning of the database, we change it to the index 0
        env.identifier = 0

    # Check if the class column is at the end of the database
    if not _class_at_end(path=env.preprocessed_database_path, class_name=env.class_name, have_header=env.have_header,
                         dialect=env.dialect):
        vprint(Message.APPEND_CLASS)
        append_column(input_path=env.preprocessed_database_path,
                      output_path=env.preprocessed_database_path,
                      column=env.class_name,
                      dialect=env.dialect)

        # The class column is now a the end of the database, we change it to the last index
        env.class_name = get_number_of_columns(env.preprocessed_database_path, dialect=env.dialect) - 1

    # Check if the database have a header
    if env.have_header:
        vprint(Message.EXTRACT_HEADER)
        _extract_header(input_path=env.preprocessed_database_path,
                        header_path=env.header_path,
                        dialect=env.dialect)

        # The header have been extracted, we remove the boolean value attesting for its presence
        env.have_header = False


# TODO: Change also the format of the database
def _init_preprocessed_database(original_database_path, preprocessed_database_path, input_encoding, output_encoding,
                                input_delimiter, output_delimiter, input_format, output_format, input_quote_char,
                                output_quote_char, input_quoting, output_quoting, input_line_delimiter,
                                output_line_delimiter) -> None:
    """ Change the encoding, delimiter, format, quoting behavior and quoting character of the original database."""
    with open(original_database_path, encoding=input_encoding, newline=input_line_delimiter) as input_file,\
            open(preprocessed_database_path, "w", encoding=output_encoding,
                 newline=output_line_delimiter) as output_file:
        input_reader = csv.reader(input_file, delimiter=input_delimiter, quoting=input_quoting,
                                  quotechar=input_quote_char, skipinitialspace=True)
        output_writer = csv.writer(output_file, delimiter=output_delimiter, quoting=output_quoting,
                                   quotechar=output_quote_char, skipinitialspace=True)
        for row in input_reader:
            output_writer.writerow(row)


def _add_id(input_path: str, output_path: str, id_name: str, have_header: bool, dialect: Dialect) -> None:
    """ Add an identificator for each instance into the database.
    If the parameter id_name is provided, it'll be inserted as a header of the output_file.
    """
    with open(input_path, encoding=dialect.encoding, newline=dialect.line_delimiter) as input_file:
        input_reader = csv.reader(input_file, delimiter=dialect.delimiter, quoting=dialect.quoting,
                                  quotechar=dialect.quote_char, skipinitialspace=dialect.skip_initial_space)
        content = []

        if have_header:
            header = next(input_reader)
            header.insert(0, id_name)
            content.append(header)
        else:
            content.append([id_name])

        for row_index, row in enumerate(input_reader):
            if row:
                row.insert(0, str(row_index))
                content.append(row)

    # Prevent the input database to be erased if it's the same as the output database
    dump_content(path=output_path, content=content, dialect=dialect)


def _identifier_at_beginning(path: str, identifier: str, have_header: bool, dialect: Dialect) -> bool:
    """ Check if the identifier column is at the beginning of the database. """
    if is_an_int(identifier):
        return int(identifier) == 0

    if not have_header:
        raise NamedAttributeButNoHeader()
    else:
        header = get_header(path=path, dialect=dialect)
        if len(header) == 0:
            raise EmptyHeader(path)
        return header[0] == identifier


def _class_at_end(path: str, class_name: str, have_header: bool, dialect: Dialect) -> bool:
    """ Check if the class column is at the end of the database. """
    if is_an_int(class_name):
        return int(class_name) == -1 or \
               int(class_name) == get_number_of_columns(path, dialect=dialect) - 1

    if not have_header:
        raise NamedAttributeButNoHeader()
    else:
        header = get_header(path=path, dialect=dialect)
        if len(header) == 0:
            raise EmptyHeader(path)
        return header[-1] == class_name


def _extract_header(input_path: str, header_path: str, dialect: Dialect):
    """ Extract the header from a database then dump it elsewhere. """
    header = extract_first_line(input_path, dialect=dialect)
    dump_string(header_path, header, dialect=dialect)


if __name__ == '__main__':
    pass
