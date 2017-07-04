""" This module will create a "classes matrices" directory, and compute a "class matrix" for each class and for each
triangular norm.
A class matrix depends of a specific class and link one instance to the % of membership a fuzzy tree gave it for this
class.
"""
from typing import List
from fforest.src.vrac.file_system import create_dir
import fforest.src.getters.environment as env
import os


def classes_matrices() -> None:
    _create_directories(classes_matrices_directory=env.classes_matrices_directory,
                        possibles_classes=env.possible_classes)


def _create_directories(classes_matrices_directory: str, possibles_classes: List[str]) -> None:
    """ Create the directories for the "class matrix" files, and one directory for each class. """
    create_dir(classes_matrices_directory)

    for class_name in possibles_classes:
        create_dir(os.path.join(classes_matrices_directory, class_name))

