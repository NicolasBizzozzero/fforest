import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.vrac.iterators import subsubtrain_dir_path


def get_efficiency_vector(vector_path: str, encoding: str = "utf8") -> list:
    with open(vector_path, encoding=encoding) as file:
        vector = list(file.readline())
    if vector[-1] == "\n":
        vector.pop()
    return [int(v) for v in vector]


def dump_difficulty_vector(vector_path: str, vector: list, encoding: str = "utf8"):
    vector = "".join([str(v) for v in vector])
    with open(vector_path, "w", encoding=encoding) as file:
        file.write(vector)


def compute_difficulty_vectors(number_of_trees: int, vector_size: int, number_of_methods: int, subtrain_dir_path: str,
                               subsubtrain_directory_pattern: str, vector_prefix: str, vector_extension: str):
    for method_num in range(number_of_methods + 1):
        method_name = methodnum_to_str(method_num)
        vector_path = subtrain_dir_path + "/" + vector_prefix + method_name + "." + vector_extension

        compute_difficulty_vector(vector_name=method_name + "." + vector_extension,
                                  vector_path=vector_path,
                                  vector_size=vector_size,
                                  number_of_trees=number_of_trees,
                                  subsubtrain_directory_pattern=subsubtrain_directory_pattern)


def compute_difficulty_vector(vector_name: str, vector_path: str, vector_size: int, number_of_trees: int,
                              subsubtrain_directory_pattern: str):
    difficulty_vector = [0] * vector_size

    for subsubtrain_dir in subsubtrain_dir_path(number_of_trees,
                                                env.cleaned_arguments[gpn.main_directory()],
                                                env.cleaned_arguments[gpn.subtrain_directory()],
                                                subsubtrain_directory_pattern):
        efficiency_vector = get_efficiency_vector(subsubtrain_dir + "/" + vector_name)
        difficulty_vector = [x + y for x, y in zip(difficulty_vector, efficiency_vector)]

    dump_difficulty_vector(vector_path, difficulty_vector)


def forest_reduction() -> None:
    compute_difficulty_vectors(number_of_trees=env.cleaned_arguments[gpn.trees_in_forest()],
                               vector_size=env.statistics[gsn.instances_in_reference()],
                               number_of_methods=env.cleaned_arguments[gpn.number_of_tnorms()],
                               subtrain_dir_path=env.statistics[gsn.database_name()] + "/" + env.cleaned_arguments[gpn.subtrain_directory()],
                               subsubtrain_directory_pattern=env.cleaned_arguments[gpn.subsubtrain_directory_pattern()],
                               vector_prefix=env.cleaned_arguments[gpn.difficulty_vector_prefix()],
                               vector_extension=env.cleaned_arguments[gpn.vector_file_extension()])
