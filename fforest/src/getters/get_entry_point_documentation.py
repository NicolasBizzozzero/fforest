""" This module defines functions to easily access values stored in the file `entry_points_documentation.xml`, located
in the `res` folder at the root of the program's package.
This file contains documentation of all entry points, which will be parsed by the `docopt` program.

It follows the following strict guidelines:
- Any value stored in the file must have its own access function.
- All access functions must have the same name as its respective entry point in the file. The only exception is a key is
named after a built-in function or variable. In this case, the programmer is free to prepend a word to its access
function name.
- Except for the access functions, this module mustn't have any side-effect to the program's namespace nor the files it
tries to access.

The XML format has been chosen over the JSON format because the JSON format can't store linebreak without using the '\n'
symbol.

If you want to add an entry point to the file, add it inside the `<entry_points>` root element in the following format :
<entry_point name="YOUR ENTRY POINT NAME">
        <documentation>
            YOUR DOCUMENTATION HERE
        </documentation>
</entry_point>
"""
import os
from xml.etree.ElementTree import parse as xml_parse

_FILE_PATH = "../../res/entry_points_documentation.xml"
_KEY_NAME = "name"
_KEY_DOCUMENTATION = "documentation"


def _get_entry_point_documentation(entry_point_name: str) -> str:
    global _KEY_NAME
    global _KEY_DOCUMENTATION

    root = _get_root()
    for entry_point in root:
        if entry_point.attrib[_KEY_NAME] == entry_point_name:
            return entry_point.find(_KEY_DOCUMENTATION).text


def _get_root():
    global _FILE_PATH

    path = os.path.join(os.path.dirname(__file__), _FILE_PATH)
    tree = xml_parse(path)
    return tree.getroot()


def main_entry_point() -> str:
    return _get_entry_point_documentation("main_entry_point")


def preprocessing_entry_point() -> str:
    return _get_entry_point_documentation("preprocessing_entry_point")


def initial_split_entry_point() -> str:
    return _get_entry_point_documentation("initial_split_entry_point")


def reference_split_entry_point() -> str:
    return _get_entry_point_documentation("reference_split_entry_point")


def subsubtrain_split_entry_point() -> str:
    return _get_entry_point_documentation("subsubtrain_split_entry_point")


def learning_entry_point() -> str:
    return _get_entry_point_documentation("learning_entry_point")


def reduction_entry_point() -> str:
    return _get_entry_point_documentation("reduction_entry_point")


def quality_entry_point() -> str:
    return _get_entry_point_documentation("quality_entry_point")


def classes_matrices_entry_point() -> str:
    return _get_entry_point_documentation("classes_matrices_entry_point")
