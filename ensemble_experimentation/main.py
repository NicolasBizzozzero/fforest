import sys
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_default_value as gdv
from ensemble_experimentation.src.initialization import pretraitement
from ensemble_experimentation.src.csv_tools import halfing
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point
from ensemble_experimentation.src.csv_tools import get_number_of_rows
from ensemble_experimentation.src.exceptions import InvalidValue
from ensemble_experimentation.src.vrac import is_a_percentage


def _check_add_id(args: dict) -> bool:
    """Check if the user asked to use as an identificator the same string as the default identificator string.
    If this function is not called, the program will overwrite all the identificator values in this specific case.
    """
    id_name = gpn.id()
    if args[id_name] == gdv.id():
        # Check if the parameter for the identificator has been used
        for option in sys.argv:
            if len(option) > len(id_name) and option[:len(id_name)] == id_name:
                return False  # User asked for "_ID" as identificator
        return True           # User didn't asked for an identificator at all
    return False              # User asked for a different identificator than "_ID"


def _convert_row_limit(row_limit: str, number_of_rows: int) -> int:
    """ Convert the parsed `row_limit` to a number of rows if it's a percentage, or return it if it's already a number
    of rows.

        Example :
        >>> _convert_row_limit("0.5", 1000)
        500
        >>> _convert_row_limit("500", 1000)
        500
        >>> _convert_row_limit("500.1", 1000)
        InvalidValue: The value "500.1" is neither a percentage nor a number of rows.
    """
    if not is_a_percentage(row_limit):
        raise InvalidValue("The value \"" + row_limit + "\" is neither a percentage nor a number of rows.")
    percentage = float(row_limit)
    return int(round(percentage * number_of_rows))


def main_entry_point():
    print("Hello main_entry_point")
    args = parse_args_main_entry_point()

    if _check_add_id(args):
        # We must add a column as identificator
        args[gpn.id()] = None

    #pretraitement(database)
    row_limit = _convert_row_limit(args[gpn.training_values()], get_number_of_rows(args[gpn.database()]))

    halfing(filepath=args[gpn.database()], row_limit=row_limit)


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
