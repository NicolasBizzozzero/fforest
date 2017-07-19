import xml.etree.ElementTree as ET


_FILE_PATH = "entry_points.xml"
_KEY_NAME = "name"
_KEY_DOCUMENTATION = "documentation"


def _get_root():
    global _FILE_PATH

    tree = ET.parse(_FILE_PATH)
    return tree.getroot()


def _get_entry_point_documentation(root, entry_point_name: str) -> str:
    global _KEY_NAME
    global _KEY_DOCUMENTATION

    for entry_point in root:
        if entry_point.attrib[_KEY_NAME] == entry_point_name:
            return entry_point.find(_KEY_DOCUMENTATION).text


def main_entry_point() -> str:
    root = _get_root()
    return _get_entry_point_documentation(root, "main_entry_point")
