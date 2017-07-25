def jason_forest():
    pass


def _data_normalization(file_path: str, dialect: Dialect):
    matrix = _load_matrix(file_path=file_path, dialect=dialect)
    for attribute in _get_attributes():
        mean = _compute_mean(matrix=matrix, attribute=attribute)
        ecart_type = _compute_ecart_type(matrix=matrix, attribute=attribute, mean=mean)
        for tree_name in matrix.keys():
            matrix[tree_name][attribute] = (matrix[tree_name][attribute] - mean) / ecart_type


def _get_attributes(file_path: str, dialect: Dialect) -> List[str]:
    return get_header(file_path=file_path, dialect=dialect)[1:]
