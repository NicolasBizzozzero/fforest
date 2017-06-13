from ensemble_experimentation.src.core.splitting_methods.split import SplittingMethod, splittingmethod_to_str


class InvalidValue(Exception):
    def __init__(self, row_limit: int):
        Exception.__init__(self, "The value \"{row_limit}\" is neither a percentage nor a number of rows.".format(row_limit=str(row_limit)))


class UnknownSplittingMethod(Exception):
    def __init__(self, method_name: str):
        Exception.__init__(self, "The splitting method : \"{method_name}\" doesn't exists".format(method_name=method_name))


class MissingClassificationAttribute(Exception):
    def __init__(self, splitting_method: SplittingMethod):
        Exception.__init__(self, "You need to pass a classification attribute for the splitting method : {method}".format(method=splittingmethod_to_str(splitting_method)))
