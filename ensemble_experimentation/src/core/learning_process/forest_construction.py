""" Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the
Salammbô software, located inside the `bin` directory, at the root of the software. Then, compute booleans and result
vectors for each tree and save it.
"""
from multiprocessing import Process
from os import path
from typing import List, Dict

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.core.learning_process.entropy_measures import EntropyMeasure
from ensemble_experimentation.src.vrac.file_system import dump_string, get_path
from ensemble_experimentation.src.vrac.iterators import grouper
from ensemble_experimentation.src.vrac.process import execute_and_get_stdout
from ensemble_experimentation.src.file_tools.format import format_to_string


HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "/../../../bin/Salammbo"
MANDATORY_OPTIONS = ["-R", "-L", "-M", "-N"]

# Key values
KEY_TRUECLASS = "trueclass"


def forest_construction():
    """ Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory. Then, compute
    booleans and result vectors for each tree and save it.
    """
    subtrain_dir_path = get_path(env.statistics[gsn.subtrain_path()])
    chosen_options = _parameters_to_salammbo_options(discretization_threshold=env.discretization_threshold,
                                                     entropy_measure=env.entropy_measure,
                                                     number_of_tnorms=env.t_norms,
                                                     entropy_threshold=env.entropy_threshold,
                                                     min_size_leaf=env.minimal_size_leaf)
    counter_size = len(str(env.trees_in_forest))
    processes = list()
    for tree_index in range(1, env.trees_in_forest + 1):
        db_name = env.subsubtrain_directory_pattern % str(tree_index).zfill(counter_size)
        process = Process(target=_tree_construction,
                          args=("{}/{}/{}.{}".format(subtrain_dir_path, db_name, db_name,
                                                     format_to_string(env.format_output)),
                                env.reference_database_path,
                                env.t_norms,
                                chosen_options))
        processes.append(process)

    # Start the processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()


def _parameters_to_salammbo_options(discretization_threshold: str, entropy_measure: EntropyMeasure,
                                    number_of_tnorms: str, entropy_threshold: str, min_size_leaf: str) -> List:
    """ Compute then return a list of options which'll be understood and used by the Salammbô executable, located inside
    the `bin` directory, at the root of the software.
    """
    options = list()

    # Discretization threshold
    options.append("-c")
    options.append(discretization_threshold)

    # Entropy measure
    if entropy_measure == EntropyMeasure.SHANNON:
        options.append("-u")

    # Number of t-norms
    options.append("-f")
    options.append(number_of_tnorms)

#    # Entropy threshold
#    options.append("-e")
#    options.append(entropy_threshold)

    # Min size leaf
#    if is_a_percentage(min_size_leaf):
#        options.append("-i")
#    else:
#        options.append("-I")
#    options.append(min_size_leaf)

    return options


def _tree_construction(path_to_database: str, path_to_reference_database: str, number_of_tnorms: int,
                       chosen_options: iter):
    lines = _construct_tree(path_to_database=path_to_database,
                            path_to_reference_database=path_to_reference_database,
                            chosen_options=chosen_options)
    result = _parse_result(lines=lines,
                           number_of_tnorms=number_of_tnorms)
    _clean_result(result=result,
                  number_of_tnorms=number_of_tnorms)
    vectors = _get_boolean_vectors(result=result,
                                   number_of_tnorms=number_of_tnorms)
    _save_vectors(vectors, get_path(path_to_database))


def _construct_tree(path_to_database: str, path_to_reference_database: str, chosen_options: iter) -> str:
    """ Call the Salammbô executable with the chosen options and parameters, then return the output. """
    parameters = MANDATORY_OPTIONS + chosen_options
    parameters.append(path_to_database)
    parameters.append(path_to_reference_database)
    return execute_and_get_stdout(PATH_TO_SALAMMBO, *parameters)


def _parse_result(lines: str, number_of_tnorms: int) -> dict:
    """ Parse lines outputted from the Salammbo executable.
    Construct a dictionary of result.
    Each key is an identifier of an instance and has for value another dictionary. Each of theses dictionary contains
    the "realclass" key, redirecting to the real class of an instance. They also contains a keys for each t-norm used to
    find a classification result. These keys redirect to a last dictionary containing the class found by this t-norm
    associated with a degree of membership.
    """
    # Each lines format is as follows :
    # Null T-NORM IDENTIFIER TRUECLASS [(FOUNDCLASSX MEMBERSHIPDEGREEX) (FOUNDCLASSY MEMBERSHIPDEGREEY) ...]
    result = dict()
    try:
        for tnorm_chunk in grouper(number_of_tnorms, lines.split("\n")):
            for instance in tnorm_chunk:
                _, tnorm, identifier, true_class, *rest = instance.split()
                identifier = int(identifier)
                try:
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found: float(membership_degree)
                                                                        for class_found, membership_degree in
                                                                        grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found: float(membership_degree)
                                                                        for class_found,
                                                                        membership_degree in grouper(2, rest)}
    except ValueError:  # For the last empty line
        pass
    return result


def _clean_result(result: dict, number_of_tnorms: int) -> None:
    """ Map to every t-norm for each identifier of the result dictionary, True if this t-norm has correctly predicted
    the real class, or False otherwise.
    """
    for identifier in result.keys():
        real_class = result[identifier][KEY_TRUECLASS]
        for tnorm in range(number_of_tnorms):
            try:
                classes_found = result[identifier][methodnum_to_str(tnorm)]
                class_found = max(classes_found.keys(), key=(lambda key: classes_found[key]))
                result[identifier][methodnum_to_str(tnorm)] = class_found == real_class
            except KeyError:
                result[identifier][methodnum_to_str(tnorm)] = False
            except ValueError:
                result[identifier][methodnum_to_str(tnorm)] = False


def _get_boolean_vectors(result: dict, number_of_tnorms: int) -> Dict[str, List[bool]]:
    vectors = dict()
    for tnorm_number in range(number_of_tnorms + 1):
        tnorm_key = methodnum_to_str(tnorm_number)
        vectors[tnorm_key] = [result[identifier][tnorm_key] for identifier in result]
    return vectors


def _save_vectors(vectors: Dict[str, List[bool]], subsubtrain_dir_path: str, vector_file_extension: str) -> None:
    for method_name in vectors.keys():
        vector_path = "{}/{}.{}".format(subsubtrain_dir_path, method_name, vector_file_extension)
        vector_content = vectors[method_name]
        _save_vector(vector_path, vector_content)


def _save_vector(vector_content: str, vector: List[bool]) -> None:
    content = "".join("1" if result else "0" for result in vector)
    dump_string(vector_content, content)


if __name__ == "__main__":
    pass
