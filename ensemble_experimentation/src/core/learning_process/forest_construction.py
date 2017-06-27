""" Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the
Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute quality and
classes_found vectors for each t_norms on each tree and save it inside the tree directory.
"""
import csv
from multiprocessing import Process
from os import path
from typing import List, Dict

import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.core.learning_process.entropy_measures import EntropyMeasure
from ensemble_experimentation.src.file_tools.format import format_to_string
from ensemble_experimentation.src.vrac.file_system import get_path
from ensemble_experimentation.src.vrac.iterators import grouper
from ensemble_experimentation.src.vrac.process import execute_and_get_stdout

HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "/../../../bin/Salammbo"
MANDATORY_OPTIONS = ["-R", "-L", "-M", "-N"]

KEY_TRUECLASS = "trueclass"
KEY_WELL_PREDICTED = "wellpredicted"
KEY_ID = "ID"


def forest_construction():
    """ Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of
    the Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute quality and
    classes_found vectors for each t_norms on each tree and save it inside the tree directory.
    """
    subtrain_dir_path = get_path(env.subtrain_database_path)
    chosen_options = _parameters_to_salammbo_options(discretization_threshold=str(env.discretization_threshold),
                                                     entropy_measure=env.entropy_measure,
                                                     number_of_tnorms=str(env.t_norms),
                                                     entropy_threshold=env.entropy_threshold,
                                                     min_size_leaf=env.minimal_size_leaf)
    counter_size = len(str(env.trees_in_forest))
    processes = list()
    for tree_index in range(1, env.trees_in_forest + 1):
        database_name = env.subsubtrain_directory_pattern % str(tree_index).zfill(counter_size)
        database_path = "{0}/{1}/{1}.{2}".format(subtrain_dir_path, database_name, format_to_string(env.format_output))
        process = Process(target=_tree_construction,
                          kwargs={"path_to_database": database_path,
                                  "path_to_reference_database": env.reference_database_path,
                                  "number_of_tnorms": env.t_norms,
                                  "chosen_options": chosen_options,
                                  "delimiter": env.delimiter_output,
                                  "quoting": env.quoting_output,
                                  "quote_char": env.quote_character_output,
                                  "encoding": env.encoding_output,
                                  "quality_vector_prefix": env.quality_vector_prefix,
                                  "class_found_vector_prefix": env.class_found_vector_prefix,
                                  "vector_file_extension": env.vector_file_extension,
                                  "possible_classes": env.possible_classes
                                  })
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
                       chosen_options: iter, delimiter: str, quoting: int, quote_char: str, encoding: str,
                       vector_file_extension: str, quality_vector_prefix: str, class_found_vector_prefix: str,
                       possible_classes: List[str]) -> None:
    """ Create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the Salammbô
    executable, located inside the `bin` directory, at the root of the software. Then, compute quality and classes_found
    vectors for each t_norms on each tree and save it inside the tree directory.
    """
    lines = _construct_tree(path_to_database=path_to_database,
                            path_to_reference_database=path_to_reference_database,
                            chosen_options=chosen_options)
    classes_found = _parse_result(lines=lines,
                                  number_of_tnorms=number_of_tnorms)
    quality = _get_quality_dictionary(classes_found=classes_found,
                                      number_of_tnorms=number_of_tnorms)
    _save_vectors(quality_vector=quality,
                  class_found_vector=classes_found,
                  number_of_tnorms=number_of_tnorms,
                  subsubtrain_dir_path=get_path(path_to_database),
                  quality_vector_prefix=quality_vector_prefix,
                  class_found_vector_prefix=class_found_vector_prefix,
                  vector_file_extension=vector_file_extension,
                  delimiter=delimiter,
                  quoting=quoting,
                  quote_char=quote_char,
                  encoding=encoding,
                  possible_classes=possible_classes,
                  skip_initial_space=True)


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
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found.strip("\""): float(membership_degree)
                                                                        for class_found, membership_degree in
                                                                        grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class.strip("\"")
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found.strip("\""): float(membership_degree)
                                                                        for class_found,
                                                                        membership_degree in grouper(2, rest)}
    except ValueError:  # For the last empty line
        pass
    return result


def _get_quality_dictionary(classes_found: dict, number_of_tnorms: int) -> dict:
    """ Return a quality dictionary, mapping to every t-norm for each identifier of the `classes_found` dictionary,
    True if this t-norm has correctly predicted the real class, or False otherwise.
    """
    tnorms = [methodnum_to_str(tnorm) for tnorm in range(number_of_tnorms + 1)]
    quality = dict()
    for identifier in classes_found.keys():
        quality[identifier] = dict()
        real_class = classes_found[identifier][KEY_TRUECLASS]
        for tnorm in tnorms:
            try:
                classes = classes_found[identifier][tnorm]
                class_found = max(classes, key=(lambda key: classes[key]))
                quality[identifier][tnorm] = class_found == real_class
            except KeyError:
                quality[identifier][tnorm] = False
            except ValueError:
                quality[identifier][tnorm] = False
    return quality


def _save_vectors(quality_vector: Dict[str, Dict[str, bool]], class_found_vector: Dict, number_of_tnorms: int,
                  subsubtrain_dir_path: str, quality_vector_prefix: str, class_found_vector_prefix: str,
                  vector_file_extension: str, delimiter: str, quoting: int, quote_char: str, encoding: str,
                  possible_classes: List[str], skip_initial_space: bool = True) -> None:
    """ Dump the content of the vectors inside the subsubtrain directory. This method'll dump for each tnorm, a quality
    vector and a classes_found vector.
    """
    for tnorm in range(number_of_tnorms + 1):
        tnorm_name = methodnum_to_str(tnorm)
        quality_vector_path = "{}/{}{}.{}".format(subsubtrain_dir_path, quality_vector_prefix, tnorm_name,
                                                  vector_file_extension)
        class_found_vector_path = "{}/{}{}.{}".format(subsubtrain_dir_path, class_found_vector_prefix, tnorm_name,
                                                      vector_file_extension)
        _save_quality_vector(vector_path=quality_vector_path,
                             quality_vector=quality_vector,
                             tnorm_name=tnorm_name,
                             delimiter=delimiter,
                             quoting=quoting,
                             quote_char=quote_char,
                             encoding=encoding,
                             skip_initial_space=skip_initial_space)

        _save_class_found_vector(vector_path=class_found_vector_path,
                                 class_found_vector=class_found_vector,
                                 possible_classes=possible_classes,
                                 real_class_name=KEY_TRUECLASS,
                                 delimiter=delimiter,
                                 quoting=quoting,
                                 quote_char=quote_char,
                                 encoding=encoding,
                                 skip_initial_space=skip_initial_space,
                                 identifier_name=KEY_ID,
                                 tnorm_name=tnorm_name)


def _save_quality_vector(vector_path: str, quality_vector: Dict[str, Dict[str, bool]], tnorm_name: str, delimiter: str,
                         quoting: int, quote_char: str, encoding: str, skip_initial_space: bool = True) -> True:
    """ Dump the quality vector inside the subsubtrain directory for one t-norm. """
    with open(vector_path, "w", encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)

        for identifier in quality_vector.keys():
            writer.writerow([identifier, 1.0 if quality_vector[identifier][tnorm_name] else 0.0])


def _save_class_found_vector(vector_path: str, class_found_vector: Dict, identifier_name: str, real_class_name: str,
                             delimiter: str, quoting: int, quote_char: str, encoding: str, possible_classes: List[str],
                             tnorm_name: str, skip_initial_space: bool = True) -> True:
    """ Dump the classes_found vector inside the subsubtrain directory for one t-norm. """
    with open(vector_path, "w", encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)

        # Write header
        header = [identifier_name, real_class_name, *(possible_class for possible_class in possible_classes)]
        writer.writerow(header)

        for identifier in class_found_vector.keys():
            row = [identifier, class_found_vector[identifier][KEY_TRUECLASS]]
            for possible_class in possible_classes:
                try:
                    row.append(class_found_vector[identifier][tnorm_name][possible_class])
                except KeyError:
                    row.append(0.0)
            writer.writerow(row)


if __name__ == "__main__":
    pass
