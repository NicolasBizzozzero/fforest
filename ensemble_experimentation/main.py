import sys
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_default_value as gdv
from ensemble_experimentation.src.initialization import pretraitement
from ensemble_experimentation.src.initialization.arg_parser import parse_args_main_entry_point


def _check_add_id(args: dict) -> bool:
    """Check if the user asked to use as an identificator the same string as the default identificator string.
    If this function is not called, the program will overwrite all the identificator values in this specific case.
    """
    id_value = gdv.id()
    id_name = gpn.id()
    if args[id_name] == id_value:
        # Check if the parameter for the identificator has been used
        for option in sys.argv:
            if len(option) > len(id_name) and option[:len(id_name)] == id_name:
                # User asked for "_ID"as identificator
                return False
        return True
    return False


def main_entry_point():
    print("Hello main_entry_point")
    args = parse_args_main_entry_point()

    if _check_add_id(args):
        # We must add a column as identificator
        args[gpn.id()] = None

    #pretraitement(database)


def forest_entry_point():
    print("Hello forest_entry_point")
    pass


def forest_reduction_entry_point():
    print("Hello forest_reduction_entry_point")
    pass


if __name__ == "__main__":
    pass
