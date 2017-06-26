import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.vrac.iterators import subsubtrain_dir_path


def forest_reduction() -> None:
    _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                vector_size=env.instances_reference_database,
                                number_of_tnorms=env.t_norms,
                                subtrain_dir_path="{}/{}".format(env.original_database_name, env.subtrain_directory),
                                subsubtrain_directory_pattern=env.subsubtrain_directory_pattern,
                                vector_prefix=env.difficulty_vector_prefix,
                                vector_extension=env.vector_file_extension)


def _compute_difficulty_vectors(number_of_trees: int, vector_size: int, number_of_tnorms: int, subtrain_dir_path: str,
                                subsubtrain_directory_pattern: str, vector_prefix: str, vector_extension: str):
    for tnorm_num in range(number_of_tnorms + 1):
        tnorm_name = methodnum_to_str(tnorm_num)
        vector_path = "{}/{}{}.{}".format(subtrain_dir_path, vector_prefix, tnorm_name, vector_extension)

        _compute_difficulty_vector(vector_name=tnorm_name + "." + vector_extension,
                                   vector_path=vector_path,
                                   vector_size=vector_size,
                                   number_of_trees=number_of_trees,
                                   subsubtrain_directory_pattern=subsubtrain_directory_pattern)


def _compute_difficulty_vector(vector_name: str, vector_path: str, vector_size: int, number_of_trees: int,
                               subsubtrain_directory_pattern: str):
    difficulty_vector = [0] * vector_size

    for subsubtrain_dir in subsubtrain_dir_path(number_of_trees,
                                                env.cleaned_arguments[gpn.main_directory()],
                                                env.cleaned_arguments[gpn.subtrain_directory()],
                                                subsubtrain_directory_pattern):
        efficiency_vector = get_efficiency_vector(subsubtrain_dir + "/" + vector_name)
        difficulty_vector = [x + y for x, y in zip(difficulty_vector, efficiency_vector)]

    dump_difficulty_vector(vector_path, difficulty_vector)


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


if __name__ == "__main__":
    pass
