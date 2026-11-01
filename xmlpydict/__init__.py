try:
    from xmlpydict_handler import _PyDictHandler
except ImportError:
    from .core import NativePyDictHandler as _PyDictHandler
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
    handler = _PyDictHandler(attr_prefix, cdata_key)
    parser = expat.ParserCreate()
    parser.buffer_text = True
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
    handler = _PyDictHandler(attr_prefix, cdata_key)
    parser = expat.ParserCreate()
    parser.buffer_text = True
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    with open(file_path, "rb") as f:
        parser.ParseFile(f)
    return handler.item


def pydict_parser(attr_prefix: str = "@", cdata_key: str = "#text"):
    handler = _PyDictHandler(attr_prefix, cdata_key)
    parser = expat.ParserCreate()
    parser.buffer_text = True
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    return handler, parser


def parse_xml_archive(
    file,
    attr_prefix: str = "@",
    cdata_key: str = "#text",
    chunk_size: int = 65536,
    start_token: bytes = b"<?xml",
):
    """
    Parse an archive of xml documents based on a delimeter start_token

    Args:
        file: The file object containing the XML content to be parsed.
        attr_prefix: The prefix to use for attributes in the resulting dictionary.
        cdata_key: The key to use for character data in the resulting dictionary.
        start_token: The byte sequence that delimits the start of each XML document.

    Returns:
        A generator yielding dictionaries representing each XML document in the collection.
    """
    handler, parser = pydict_parser(attr_prefix, cdata_key)
    buffer = bytearray()

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            if buffer:
                parser.Parse(buffer, True)
                yield handler.item
            break

        buffer.extend(chunk)
        while True:
            idx = buffer.find(start_token, 1)
            if idx == -1:
                break

            parser.Parse(buffer[:idx], True)
            yield handler.item

            handler, parser = pydict_parser(
                attr_prefix=attr_prefix, cdata_key=cdata_key
            )
            del buffer[:idx]
