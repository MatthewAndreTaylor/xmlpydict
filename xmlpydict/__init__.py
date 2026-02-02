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
    with open(file_path, "rb") as f:
        parser.ParseFile(f)
    return handler.item


def iter_xml_documents(
    file_path, chunk_size: int = 64 * 1024, start_token: bytes = b"<?xml"
):
    buffer = b""
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                if buffer.strip():
                    yield buffer
                break
            buffer += chunk
            while True:
                start_index = buffer.find(start_token, 1)
                if start_index == -1:
                    break
                yield buffer[:start_index]
                buffer = buffer[start_index:]


def parse_xml_collections(
    file_path,
    attr_prefix: str = "@",
    cdata_key: str = "#text",
    start_token: bytes = b"<?xml",
):
    """
    Parse collections of xml documents based on a delimeter start_token

    Args:
        file_path: The path to the XML file to be parsed.
        attr_prefix: The prefix to use for attributes in the resulting dictionary.
        cdata_key: The key to use for character data in the resulting dictionary.
        start_token: The byte sequence that delimits the start of each XML document.

    Returns:
        A generator yielding dictionaries representing each XML document in the collection.
    """
    for xml_content in iter_xml_documents(file_path, start_token=start_token):
        yield parse(
            xml_content.decode("utf-8"), attr_prefix=attr_prefix, cdata_key=cdata_key
        )
