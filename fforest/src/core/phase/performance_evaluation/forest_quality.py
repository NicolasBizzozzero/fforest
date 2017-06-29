""" Compute a quality's forest vector for each triangular norm chosed. A quality's forest vector map each tree of the
forest to its quality. It exists many ways to compute the quality of a tree. The main one sum all instances' score then
divide this sum by the number of instances to normalize the result. An instance score is the product of its difficult
by the % of membership found by the tree. Theses quality's forest vectors will be dumped into the subtrain directory.
"""


import fforest.src.getters.environment as env
from fforest.src.core.phase.learning_process.forest_construction import KEY_ID, KEY_TRUECLASS
from fforest.src.file_tools.csv_tools import get_identified_row


def forest_quality() -> None:
    difficulty_vectors = \
        _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                    quality_vectors_dict=env.quality_vectors_paths,
                                    delimiter=env.delimiter_output,
                                    quoting=env.quoting_output,
                                    quote_char=env.quote_character_output,
                                    encoding=env.encoding_output,
                                    line_delimiter=env.line_delimiter_output)

    _dump_difficulty_vectors(difficulty_vectors=difficulty_vectors,
                             difficulty_vectors_paths=env.difficulty_vectors_paths,
                             delimiter=env.delimiter_output,
                             quoting=env.quoting_output,
                             quote_char=env.quote_character_output,
                             encoding=env.encoding_output,
                             line_delimiter=env.line_delimiter_output,
                             skip_initial_space=True)


def _get_instance_score(instance_identifier: str, difficulty_vector_path: str, quality_vector_path: str):
    pass


def _get_instance_difficulty(instance_identifier: str, difficulty_vector_path: str) -> float:
    row = get_identified_row(difficulty_vector_path, KEY_ID, instance_identifier, delimiter=";", quoting=2, quote_character= "\"", encoding="utf8")
    trueclass = row[KEY_TRUECLASS]
    return float(row[trueclass])


if __name__ == "__main__":
    pass
