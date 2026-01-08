# xmlpydict 📑

[![XML Tests](https://github.com/MatthewAndreTaylor/xml-to-pydict/actions/workflows/tests.yml/badge.svg)](https://github.com/MatthewAndreTaylor/xml-to-pydict/actions/workflows/tests.yml)
[![PyPI versions](https://img.shields.io/badge/python-3.8%2B-blue)](https://github.com/MatthewAndreTaylor/xml-to-pydict)
[![PyPI](https://img.shields.io/pypi/v/xmlpydict.svg)](https://pypi.org/project/xmlpydict/)

## Requirements

- `python 3.8+`

## Installation

To install xmlpydict, using pip:

```bash
pip install xmlpydict
```

## Quickstart

```py
>>> from xmlpydict import parse
>>> parse("<package><xmlpydict language='python'/></package>")
{'package': {'xmlpydict': {'@language': 'python'}}}
>>> parse("<person name='Matthew'>Hello!</person>")
{'person': {'@name': 'Matthew', '#text': 'Hello!'}}
```

## Goals

Create a consistent parsing strategy between XML and Python dictionaries using the specification found [here](https://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html). `xmlpydict` focuses on speed; see the benchmarks below.

<img width="256" alt="small_xml_document" src="https://github.com/user-attachments/assets/0248a408-6bb6-4790-bd0f-f90537e2f21a" />
<img width="256" alt="large_xml_document" src="https://github.com/user-attachments/assets/539a2a69-f475-46a5-bffc-1e8805a5a5e7" />


### xmlpydict supports the following 

[CDataSection](https://www.w3.org/TR/xml/#sec-cdata-sect):  CDATA Sections are stored as {'#text': CData}.

[Comments](https://www.w3.org/TR/xml/#sec-comments):  Comments are tokenized for corectness, but have no effect in what is returned.

[Element Tags](https://www.w3.org/TR/xml/#sec-starttags):  Allows for duplicate attributes, however only the latest defined will be taken. 

[Characters](https://www.w3.org/TR/xml/#charsets):  Similar to CDATA text is stored as {'#text': Char} , however this text is stripped.

```py
# Empty tags are containers
>>> from xmlpydict import parse
>>> parse("<a></a>")
{'a': None}
>>> parse("<a/>")
{'a': None}
>>> parse("<a/>").get('href')
None
```

### Attribute prefixing

```py
# Change prefix from default "@" with keyword argument attr_prefix
>>> from xmlpydict import parse
>>> parse('<p width="10" height="5"></p>', attr_prefix="$")
{"p": {"$width": "10", "$height": "5"}}
```


### Exceptions

```py
# Grammar and structure of the xml_content is checked while parsing
>>> from xmlpydict import parse
>>> parse("<a></ a>")
xml.parsers.expat.ExpatError: not well-formed (invalid token): line 1, column 5
```


### Unsupported

Prolog / Enforcing Document Type Definition and Element Type Declarations

Entity Referencing

Namespaces
