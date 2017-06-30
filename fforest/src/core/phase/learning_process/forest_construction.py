""" Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the
Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute cclassified and
salammbo vectors for each t_norms on each tree and save it inside the tree directory.
"""
from multiprocessing import Process
from os import path
from typing import List, Dict

import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.triangular_norms import tnorm_to_str
from fforest.src.core.phase.learning_process.entropy_measures import EntropyMeasure
from fforest.src.file_tools.csv_tools import dump_csv_content
from fforest.src.file_tools.format import format_to_string
from fforest.src.vrac.file_system import get_path
from fforest.src.vrac.iterators import grouper
from fforest.src.vrac.process import execute_and_get_stdout
from fforest.src.file_tools.csv_tools import Dialect


HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "/../../../../bin/Salammbo"
MANDATORY_OPTIONS = ["-R", "-L", "-M", "-N"]

KEY_TRUECLASS = "trueclass"
KEY_CCLASSIFIED = "cclassified"
KEY_ID = "ID"


def forest_construction():
    """ Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of
    the Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute cclassified
    and salammbo vectors for each t_norms on each tree and save it inside the tree directory.
    """
    chosen_options = _parameters_to_salammbo_options(discretization_threshold=str(env.discretization_threshold),
                                                     entropy_measure=env.entropy_measure,
                                                     number_of_tnorms=str(env.t_norms),
                                                     entropy_threshold=env.entropy_threshold,
                                                     min_size_leaf=env.minimal_size_leaf)

    processes = list()
    for tree_index in range(1, env.trees_in_forest + 1):
        process = Process(target=_tree_construction,
                          kwargs={"path_to_database": env.subsubtrain_databases_paths[tree_index - 1],
                                  "path_to_reference_database": env.reference_database_path,
                                  "chosen_options": chosen_options,
                                  "cclassified_vectors_paths": env.cclassified_vectors_paths,
                                  "salammbo_vectors_paths": env.salammbo_vectors_paths,
                                  "possible_classes": env.possible_classes,
                                  "tree_index": tree_index,
                                  "dialect_output": env.dialect_output,
                                  })
        processes.append(process)

    # Start the processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()


def _parameters_to_salammbo_options(discretization_threshold: str, entropy_measure: EntropyMeasure,
                                    number_of_tnorms: str, entropy_threshold: str, min_size_leaf: str) -> List[str]:
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

    # Entropy threshold
    options.append("-e")
    options.append(entropy_threshold)

    # Min size leaf
    # The `-i` option is deprecated by Salammbo, we ignore it
    options.append("-I")
    options.append(min_size_leaf)

    return options


def _tree_construction(path_to_database: str, path_to_reference_database: str, chosen_options: iter,
                       cclassified_vectors_paths: Dict[str, List[str]], salammbo_vectors_paths: Dict[str, List[str]],
                       possible_classes: List[str], tree_index: int, dialect: Dialect) -> None:
    """ Create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the Salammbô
    executable, located inside the `bin` directory, at the root of the software. Then, compute cclassified and salammbo
    vectors for each t_norms on each tree and save it inside the tree directory.
    """
    number_of_tnorms = len(cclassified_vectors_paths.keys())
    lines = _construct_tree(path_to_database=path_to_database,
                            path_to_reference_database=path_to_reference_database,
                            chosen_options=chosen_options)
    salammbo_vectors = _parse_result(lines=lines,
                                     number_of_tnorms=number_of_tnorms)
    cclassified_vectors = _get_cclassified_dictionary(salammbo_dict=salammbo_vectors,
                                                      number_of_tnorms=number_of_tnorms)
    _save_cclassified_vectors(cclassified_vector=cclassified_vectors,
                              vectors_path=cclassified_vectors_paths,
                              tree_index=tree_index,
                              dialect=dialect)
    _save_salammbo_vectors(vector_content=salammbo_vectors,
                           vectors_path=salammbo_vectors_paths,
                           tree_index=tree_index,
                           possible_classes=possible_classes,
                           dialect=dialect)


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
    Each lines format is as follows :
    Null T-NORM IDENTIFIER TRUECLASS [(FOUNDCLASSX MEMBERSHIPDEGREEX) (FOUNDCLASSY MEMBERSHIPDEGREEY) ...]
    """
    result = dict()
    try:
        for tnorm_chunk in grouper(number_of_tnorms, lines.split("\n")):
            for instance in tnorm_chunk:
                _, tnorm, identifier, true_class, *rest = instance.strip("\"").split()
                identifier = identifier.strip("\"")
                try:
                    result[identifier][tnorm_to_str(int(tnorm))] = {class_found.strip('"'): float(membership_degree)
                                                                    for class_found, membership_degree in
                                                                    grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class.strip("\"")
                    result[identifier][tnorm_to_str(int(tnorm))] = {class_found.strip('"'): float(membership_degree)
                                                                    for class_found, membership_degree in
                                                                    grouper(2, rest)}
    except ValueError:  # For the last empty line
        pass
    return result


def _get_cclassified_dictionary(salammbo_dict: dict, number_of_tnorms: int) -> Dict[str, Dict[str, bool]]:
    """ Return a correctly classified dictionary, mapping to every t-norm for each identifier of the salammbo
    dictionary, True if this t-norm has correctly predicted the real class, or False otherwise.
    """
    tnorms = [tnorm_to_str(tnorm) for tnorm in range(number_of_tnorms + 1)]
    cclassified = dict()
    for identifier in salammbo_dict.keys():
        cclassified[identifier] = dict()
        real_class = salammbo_dict[identifier][KEY_TRUECLASS]
        for tnorm in tnorms:
            try:
                classes = salammbo_dict[identifier][tnorm]
                class_found = max(classes, key=(lambda key: classes[key]))
                cclassified[identifier][tnorm] = class_found == real_class
            except KeyError:
                cclassified[identifier][tnorm] = False
            except ValueError:
                cclassified[identifier][tnorm] = False
    return cclassified


def _save_cclassified_vectors(cclassified_vector: Dict[str, Dict[str, bool]], vectors_path: Dict[str, List[str]],
                              tree_index: int, dialect: Dialect) -> None:
    """ Dump the content of the cclassified vectors inside the subsubtrain directory. """
    for tnorm in vectors_path.keys():
        _save_cclassified_vector(vector_path=vectors_path[tnorm][tree_index - 1],
                                 vector_content=cclassified_vector,
                                 tnorm_name=tnorm,
                                 dialect=dialect)


def _save_cclassified_vector(vector_path: str, vector_content: Dict[str, Dict[str, bool]], tnorm_name: str,
                             dialect: Dialect) -> None:
    """ Dump the cclassified vector inside the subsubtrain directory for one t-norm. """
    content = list()
    for identifier in vector_content.keys():
        content.append([identifier, 1.0 if vector_content[identifier][tnorm_name] else 0.0])

    dump_csv_content(path=vector_path, content=content, dialect=dialect)


def _save_salammbo_vectors(vector_content: Dict, vectors_path: Dict[str, List[str]], possible_classes: List[str],
                           tree_index: int, dialect: Dialect) -> None:
    """ Dump the content of the salammbo vectors inside the subsubtrain directory. """
    for tnorm in vectors_path.keys():
        _save_salammbo_vector(vector_path=vectors_path[tnorm][tree_index - 1],
                              vector_content=vector_content,
                              tnorm=tnorm,
                              possible_classes=possible_classes,
                              dialect=dialect)


def _save_salammbo_vector(vector_path: str, vector_content: Dict, tnorm: str, possible_classes: List[str],
                          dialect: Dialect) -> None:
    """ Dump the salammbo vector inside the subsubtrain directory for one t-norm. """
    content = list()

    # Add header
    content.append([KEY_ID, KEY_TRUECLASS, *(possible_class for possible_class in possible_classes)])

    # Add rows
    for identifier in vector_content.keys():
        row = [identifier, vector_content[identifier][KEY_TRUECLASS]]
        for possible_class in possible_classes:
            try:
                row.append(vector_content[identifier][tnorm][possible_class])
            except KeyError:
                row.append(0.0)
        content.append(row)

    dump_csv_content(path=vector_path, content=content, dialect=dialect)


if __name__ == "__main__":
    pass
