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
    _create_directories(classes_matrices_directory_name=env.classes_matrices_directory_name,
                        possibles_classes=env.possible_classes)


def _create_directories(classes_matrices_directory_name: str, possibles_classes: List[str]) -> None:
    """ Create the directories for the "class matrix" files, and one directory for each class. """
    create_dir(classes_matrices_directory_name)

    for class_name in possibles_classes:
        create_dir(os.path.join(classes_matrices_directory_name, class_name))

