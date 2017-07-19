from xml.etree.ElementTree import parse as xml_parse
import os


_FILE_PATH = "../../res/entry_points_documentation.xml"
_KEY_NAME = "name"
_KEY_DOCUMENTATION = "documentation"


def _get_root():
    global _FILE_PATH

    path = os.path.join(os.path.dirname(__file__), _FILE_PATH)
    tree = xml_parse(path)
    return tree.getroot()


def _get_entry_point_documentation(entry_point_name: str) -> str:
    global _KEY_NAME
    global _KEY_DOCUMENTATION

    root = _get_root()
    for entry_point in root:
        if entry_point.attrib[_KEY_NAME] == entry_point_name:
            return entry_point.find(_KEY_DOCUMENTATION).text


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
