from pyxmlhandler import _PyDictHandler
from xml.parsers import expat


def parse(xml_content, **kwargs) -> dict:
    handler = _PyDictHandler(**kwargs)
    parser = expat.ParserCreate()
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    parser.Parse(xml_content, True)
    return handler.item


def parse_file(file_path, **kwargs) -> dict:
    handler = _PyDictHandler(**kwargs)
    parser = expat.ParserCreate()
    parser.CharacterDataHandler = handler.characters
    parser.StartElementHandler = handler.startElement
    parser.EndElementHandler = handler.endElement
    with open(file_path, "r", encoding="utf-8") as f:
        parser.ParseFile(f)
    return handler.item
