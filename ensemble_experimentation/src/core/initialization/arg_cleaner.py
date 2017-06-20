import copy
import sys

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.learning_process.forest_construction import str_to_entropy_measure
from ensemble_experimentation.src.core.splitting_methods.split import str_to_splittingmethod, SplittingMethod
from ensemble_experimentation.src.file_tools.csv_tools import get_number_of_rows, str_to_quoting
from ensemble_experimentation.src.file_tools.format import str_to_format
from ensemble_experimentation.src.vrac.file_system import get_filename
from ensemble_experimentation.src.vrac.maths import is_a_percentage


class MissingClassificationAttribute(Exception):
    def __init__(self):
        Exception.__init__(self, "You need to pass a classification attribute")


class InvalidValue(Exception):
    def __init__(self, row_limit: str):
        Exception.__init__(self, "The value \"{row_limit}\" is neither a percentage nor"
                                 " a number of rows.".format(row_limit=row_limit))


def _check_default_value_id(args: dict) -> bool:
    """ Check if the user asked to use as an identifier the same string as the default identifier string.
    Calling this function prevent the program from overwriting all the identifier values in this specific case.
    """
    id_name = gpn.identifier()
    if args[id_name] == gdv.identifier():
        # Check if the parameter for the identifier has been used
        for option in sys.argv:
            if len(option) > len(id_name) and option[:len(id_name)] == id_name:
                return False  # User asked for the default identifier
        return True           # User didn't asked for an identifier at all
    return False              # User asked for a different identifier than the default


def convert_row_limit(row_limit: str, number_of_rows: int) -> int:
    """ Convert the parsed `row_limit` to a number of rows if it's a percentage, or raise an exception otherwise

        Example :
        >>> convert_row_limit("0.5", 1000)
        500
        >>> convert_row_limit("500", 1000)
        Traceback (most recent call last):
         ...
        arg_parser.InvalidValue: The value "500" is neither a percentage nor a number of rows.
        >>> convert_row_limit("500.1", 1000)
        Traceback (most recent call last):
         ...
        arg_parser.InvalidValue: The value "500.1" is neither a percentage nor a number of rows.
    """
    if not is_a_percentage(row_limit):
        raise InvalidValue(row_limit)
    percentage = float(row_limit)
    return int(round(percentage * number_of_rows))


def _get_preprocessed_db_name(args: dict, extension: str = "") -> str:
    """ Return the name of the modified database given the path of the original database. """
    return "~" + get_filename(args[gpn.database()], with_extension=False) + extension


def clean_args(args: dict) -> dict:
    """ Clean the arguments to make the `args` dictionary usable more easily.
    This mainly consist of converting strings to int, float or enum.
    """
    cleaned_args = copy.copy(args)

    # Rename parameter database
    cleaned_args[gpn.database()] = cleaned_args["<" + gpn.database() + ">"]
    del cleaned_args["<" + gpn.database() + ">"]

    # Count instances in initial database
    env.statistics[gsn.instances_in_database()] = get_number_of_rows(cleaned_args[gpn.database()])

    # Class name
    try:
        args[gpn.class_name()]
    except KeyError:
        raise MissingClassificationAttribute()

    # Delimiter

    # Discretization threshold
    cleaned_args[gpn.discretization_threshold()] = int(args[gpn.discretization_threshold()])

    # Encoding

    # Entropy measure
    cleaned_args[gpn.entropy_measure()] = str_to_entropy_measure(args[gpn.entropy_measure()])

    # Entropy threshold
    cleaned_args[gpn.entropy_threshold()] = float(args[gpn.entropy_threshold()])

    # Format
    cleaned_args[gpn.format_db()] = str_to_format(args[gpn.format_db()])
    extension = "." + args[gpn.format_db()].lower()

    # Have header

    # Header file name

    # Header extension

    # Help

    # ID
    if _check_default_value_id(args):
        # We must add a column as an identifier
        # It will be done in the preprocessing function
        cleaned_args[gpn.identifier()] = None

    # Initial split Method
    cleaned_args[gpn.initial_split_method()] = str_to_splittingmethod(args[gpn.initial_split_method()])
    if cleaned_args[gpn.initial_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and \
       cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute()

    # Main directory
    if cleaned_args[gpn.main_directory()] is None:
        cleaned_args[gpn.main_directory()] = get_filename(cleaned_args[gpn.database()])

    # Number of t-norms
    cleaned_args[gpn.number_of_tnorms()] = int(args[gpn.number_of_tnorms()])

    # Preprocessed database name
    if args[gpn.preprocessed_database_name()] is None:
        cleaned_args[gpn.preprocessed_database_name()] = _get_preprocessed_db_name(cleaned_args, extension=extension)
    else:
        cleaned_args[gpn.preprocessed_database_name()] = get_filename(cleaned_args[gpn.preprocessed_database_name()],
                                                                      with_extension=True)

    # Quote character

    # Quoting
    cleaned_args[gpn.quoting()] = str_to_quoting(args[gpn.quoting()])

    # Reference database name
    cleaned_args[gpn.reference_name()] = get_filename(cleaned_args[gpn.reference_name()],
                                                      with_extension=False) + extension

    # Reference split Method
    cleaned_args[gpn.reference_split_method()] = str_to_splittingmethod(args[gpn.reference_split_method()])
    if cleaned_args[gpn.reference_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and \
       cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute()

    # Reference split value

    # Statistics file name

    # Subsubtrain directory name pattern
    # TODO: I don't know why, but docopt can't parse the default value
    if cleaned_args[gpn.subsubtrain_directory_pattern()] is None:
        cleaned_args[gpn.subsubtrain_directory_pattern()] = gdv.subsubtrain_directory_pattern()

    # Subsubtrain split method
    # TODO: I don't know why, but docopt can't parse the default value
    if args[gpn.subsubtrain_split_method()] is None:
        cleaned_args[gpn.subsubtrain_split_method()] = gdv.subsubtrain_split_method()
    cleaned_args[gpn.subsubtrain_split_method()] = str_to_splittingmethod(cleaned_args[gpn.subsubtrain_split_method()])
    if cleaned_args[gpn.subsubtrain_split_method()] == SplittingMethod.KEEP_DISTRIBUTION and \
       cleaned_args[gpn.class_name()] is None:
        raise MissingClassificationAttribute()

    # Subsubtrain name pattern

    # Subtrain directory

    # Subtrain name
    cleaned_args[gpn.subtrain_name()] = get_filename(cleaned_args[gpn.subtrain_name()], with_extension=False) + extension

    # Test database name
    cleaned_args[gpn.test_name()] = get_filename(cleaned_args[gpn.test_name()], with_extension=False) + extension

    # Train database name
    cleaned_args[gpn.train_name()] = get_filename(cleaned_args[gpn.train_name()], with_extension=False) + extension

    # Training value
    cleaned_args[gpn.training_value()] = convert_row_limit(cleaned_args[gpn.training_value()],
                                                           env.statistics[gsn.instances_in_database()])

    # Tree file extension

    # Trees in forest
    cleaned_args[gpn.trees_in_forest()] = int(cleaned_args[gpn.trees_in_forest()])

    # Vector file extension

    print(cleaned_args)

    return cleaned_args
