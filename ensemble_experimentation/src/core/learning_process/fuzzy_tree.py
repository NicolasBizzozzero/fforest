def construct_tree():
    result = execute_and_get_output()
    return result


def parse_result() -> dict:
    pass


# Exemple d'output voulu :
"""
{
    "instance1": {
        "class": "2",
        "algo1": {
            "1": 0.1563,
            "2": 0.005,
            "3": 0.8445
        },
        "algo2": {
            "1": 0.1563,
            "2": 0.005,
            "3": 0.8445
        },
        "algo3": {
            "1": 1,
            "2": 0,
            "3": 0
        },
    },
    "instance2": {
        "class": "1",
        "algo1": {
            "1": 0.1563,
            "2": 0.005,
            "3": 0.8445
        },
        "algo2": {
            "1": 0.1563,
            "2": 0.005,
            "3": 0.8445
        },
        "algo3": {
            "1": 1,
            "2": 0,
            "3": 0
        },
    }
}
"""