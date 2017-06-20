from enum import IntEnum
from multiprocessing import Process
from os import path
from typing import List, Dict

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.vrac.file_system import dump_string, get_path
from ensemble_experimentation.src.vrac.iterators import grouper
from ensemble_experimentation.src.vrac.process import execute_and_get_stdout

HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "/../../../bin/Salammbo"
MANDATORY_OPTIONS = ["-R", "-L", "-M", "-N"]

# Key values
KEY_DEFAULT_METHOD = "method_"
KEY_TRUECLASS = "trueclass"


class EntropyMeasure(IntEnum):
    UNKNOWN = 0
    SHANNON = 1


def str_to_entropy_measure(string: str) -> EntropyMeasure:
    string = string.lower()
    if string == "shannon":
        return EntropyMeasure.SHANNON
    else:
        return EntropyMeasure.UNKNOWN


class ClassificationMethod(IntEnum):
    CLASSIC = 0
    ZADEH = 1
    LUKA = 2


def _methodnum_to_str(method_number: int) -> str:
    if method_number == ClassificationMethod.CLASSIC.value:
        return "classic"
    elif method_number == ClassificationMethod.ZADEH.value:
        return "zadeh"
    elif method_number == ClassificationMethod.LUKA.value:
        return "luka"
    else:
        return KEY_DEFAULT_METHOD + str(method_number)


def _construct_tree(path_to_db: str, chosen_options: iter) -> str:
    """ Call the Salammbo executable with the choosen options and parameters, then return the output. """
    parameters = MANDATORY_OPTIONS + chosen_options
    parameters.append(path_to_db)
    parameters.append(env.statistics[gsn.reference_path()])
    result = execute_and_get_stdout(PATH_TO_SALAMMBO,
                                    *parameters)
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
                    result[identifier][_methodnum_to_str(int(method))] = {class_found: float(membership_degree)
                                                                          for class_found, membership_degree in
                                                                          grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class
                    result[identifier][_methodnum_to_str(int(method))] = {class_found: float(membership_degree)
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
            try:
                dict_classesfound = result[identifier][_methodnum_to_str(method_number)]
                class_found = max(dict_classesfound.keys(), key=(lambda key: dict_classesfound[key]))
                result[identifier][_methodnum_to_str(method_number)] = class_found == real_class
            except KeyError:
                result[identifier][_methodnum_to_str(method_number)] = False
            except ValueError:
                result[identifier][_methodnum_to_str(method_number)] = False


def _get_boolean_vectors(result: dict, number_of_methods: int) -> Dict[str, List[bool]]:
    vectors = dict()
    for method_number in range(number_of_methods + 1):
        method_key = _methodnum_to_str(method_number)
        vectors[method_key] = [result[identifier][method_key] for identifier in result]
    return vectors


def _save_vectors(vectors: Dict[str, List[bool]], subsubtrain_dir_path: str) -> None:
    for method_name in vectors.keys():
        path = subsubtrain_dir_path + "/" + method_name + "." + env.cleaned_arguments[gpn.vector_file_extension()]
        _save_vector(path, vectors[method_name])


def _save_vector(path: str, vector: List[bool]) -> None:
    content = "".join("1" if result else "0" for result in vector)
    dump_string(path, content)


def _parameters_to_salammbo_options(parameters: dict) -> iter:
    options = list()

    # Discretization threshold
    options.append("-c")
    options.append(str(parameters[gpn.discretization_threshold()]))

    # Entropy measure
    if parameters[gpn.discretization_threshold()] == EntropyMeasure.SHANNON:
        options.append("-u")

    # Number of t-norms
    options.append("-f")
    options.append(str(parameters[gpn.number_of_tnorms()]))

    return options


def _tree_construction(path_to_db: str, number_of_methods: int, choosen_options: iter):
    lines = _construct_tree(path_to_db, choosen_options)
    result = _parse_result(lines, number_of_methods)
    _clean_result(result, number_of_methods)
    vectors = _get_boolean_vectors(result, number_of_methods)
    _save_vectors(vectors, get_path(path_to_db))


def forest_construction():
    # Create the threads
    subtrain_dir_path = get_path(env.statistics[gsn.subtrain_path()])
    number_of_methods = env.cleaned_arguments[gpn.number_of_tnorms()]
    chosen_options = _parameters_to_salammbo_options(env.cleaned_arguments)
    number_of_trees = env.cleaned_arguments[gpn.trees_in_forest()]
    counter_size = len(str(number_of_trees))
    threads = list()
    for tree_index in range(1, number_of_trees + 1):
        db_name = env.cleaned_arguments[gpn.subsubtrain_directory_pattern()] % str(tree_index).zfill(counter_size)
        thread = Process(target=_tree_construction,
                         args=(subtrain_dir_path + "/" + db_name + "/" + db_name + "." + "csv",
                               number_of_methods,
                               chosen_options))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
# Execution time for "forest_construction" : 0.5033886432647705 seconds


def forest_construction_synchronous():
    # Create the threads
    subtrain_dir_path = get_path(env.statistics[gsn.subtrain_path()])
    number_of_methods = env.cleaned_arguments[gpn.number_of_tnorms()]
    chosen_options = _parameters_to_salammbo_options(env.cleaned_arguments)
    number_of_trees = env.cleaned_arguments[gpn.trees_in_forest()]
    counter_size = len(str(number_of_trees))

    for tree_index in range(1, number_of_trees + 1):
        db_name = env.cleaned_arguments[gpn.subsubtrain_directory_pattern()] % str(tree_index).zfill(counter_size)
        _tree_construction(subtrain_dir_path + "/" + db_name + "/" + db_name + "." + "csv",
                           number_of_methods,
                           chosen_options)
# Execution time for "forest_construction_synchronous" : 3.3870317935943604 seconds


if __name__ == "__main__":
    pass
