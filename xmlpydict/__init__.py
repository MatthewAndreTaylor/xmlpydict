from pyxmlhandler import _PyDictHandler
from xml.parsers import expat


def parse(xml_content, attr_prefix: str = "@", cdata_key: str = "#text") -> dict:
    """
    Parse XML content into a python dictionary.

    Args:
        xml_content: The XML content to be parsed.
        attr_prefix: The prefix to use for attributes in the resulting dictionary.
        cdata_key: The key to use for character data in the resulting dictionary.

    Returns:
        A dictionary representation of the XML content.
    """
    handler = _PyDictHandler(attr_prefix=attr_prefix, cdata_key=cdata_key)
    parser = expat.ParserCreate()
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    parser.Parse(xml_content, True)
    return handler.item


def parse_file(file_path, attr_prefix: str = "@", cdata_key: str = "#text") -> dict:
    """
    Parse an XML file into a python dictionary.

    Args:
        file_path: The path to the XML file to be parsed.
        attr_prefix: The prefix to use for attributes in the resulting dictionary.
        cdata_key: The key to use for character data in the resulting dictionary.

    Returns:
        A dictionary representation of the XML file content.
    """
    handler = _PyDictHandler(attr_prefix=attr_prefix, cdata_key=cdata_key)
    parser = expat.ParserCreate()
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    with open(file_path, "r", encoding="utf-8") as f:
        parser.ParseFile(f)
    return handler.item
