from enum import IntEnum
from os import path
from typing import List, Dict

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.vrac.iterators import grouper
from ensemble_experimentation.src.vrac.process import execute_and_get_stdout

HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "../../../bin/Salammbo"
MANDATORY_OPTIONS = ("-R", "-L", "-M")

# Key values
KEY_DEFAULT_METHOD = "method_"
KEY_TRUECLASS = "trueclass"


class ClassificationMethod(IntEnum):
    CLASSIC = 0
    ZADEH = 1
    LUKA = 2


def _methodnum_to_string(method_number: int) -> str:
    if method_number == ClassificationMethod.CLASSIC.value:
        return "classic"
    elif method_number == ClassificationMethod.ZADEH.value:
        return "zadeh"
    elif method_number == ClassificationMethod.LUKA.value:
        return "luka"
    else:
        return KEY_DEFAULT_METHOD + str(method_number)


def _construct_tree(path_to_db: str, choosen_options: iter) -> str:
    """ Call the Salammbo executable with the choosen options and parameters, then return the output. """
    result = execute_and_get_stdout(PATH_TO_SALAMMBO,
                                    *MANDATORY_OPTIONS,
                                    *choosen_options,
                                    path_to_db,
                                    env.statistics[gsn.reference_path()])
    return result


def _parse_result(lines: str, number_of_methods: int) -> dict:
    """ Parse lines outputted from the Salammbo executable.
    Construct a dictionary of result.
    Each key is an identifier of an instance and has for value another dictionary. Each of theses dictionary contains
    the "realclass" key, redirecting to the real class of an instance. They also contains a keys for each classification
    method used to find a classification result. These keys redirect to a last dictionary containing the class found by
    this method associated with a degree of membership.
    """
    # Each lines format is as follows :
    # Null METHODCLASSIFICATION IDENT TRUECLASS [(FOUNDCLASSX MEMBERSHIPDEGREEX) (FOUNDCLASSY MEMBERSHIPDEGREEY) ...]

    result = dict()
    try:
        for method_chunk in grouper(number_of_methods, lines.split("\n")):
            for instance in method_chunk:
                _, method, identifier, true_class, *rest = instance.split()
                identifier = int(identifier)
                try:
                    result[identifier][_methodnum_to_string(int(method))] = {class_found: float(membership_degree)
                                                                             for class_found, membership_degree in
                                                                             grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class
                    result[identifier][_methodnum_to_string(int(method))] = {class_found: float(membership_degree)
                                                                             for class_found,
                                                                             membership_degree in grouper(2, rest)}
    except ValueError:  # For the last empty line
        pass
    return result


def _clean_result(result: dict, number_of_methods: int) -> None:
    """ Map to every classification method for each identifier of the result dictionary, True if this method has
    correctly predicted the real class, or False otherwise. """
    for identifier in result.keys():
        real_class = result[identifier][KEY_TRUECLASS]
        for method_number in range(number_of_methods):
            dict_classesfound = result[identifier][_methodnum_to_string(method_number)]
            class_found = max(dict_classesfound.keys(), key=(lambda key: dict_classesfound[key]))
            result[identifier][_methodnum_to_string(method_number)] = class_found == real_class


def _get_boolean_vectors(result: dict, number_of_methods: int) -> Dict[str, List[bool]]:
    vectors = dict()
    for method_number in range(number_of_methods):
        method_key = _methodnum_to_string(method_number)
        vectors[method_key] = [result[identifier][method_key] for identifier in result]
    return vectors


def save_vectors(vectors: Dict[str, List[bool]], dir_path: str) -> None:
    pass


def save_vector(name: str, vector: List[bool], dir_path: str) -> None:
    pass


if __name__ == "__main__":
    from ensemble_experimentation.src.vrac.file_system import get_file_content
    from pprint import pprint

    NUMBER_OF_METHODS = 3
    LINES = get_file_content("../../../bin/log2.txt")

    result = _parse_result(LINES, NUMBER_OF_METHODS)
    pprint(result)
    _clean_result(result, NUMBER_OF_METHODS)
    pprint(result)
    vectors = _get_boolean_vectors(result, NUMBER_OF_METHODS)
    pprint(vectors)
