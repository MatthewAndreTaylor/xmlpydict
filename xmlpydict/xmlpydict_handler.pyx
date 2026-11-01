# cython: boundscheck=False, wraparound=False, always_allow_keywords=False, binding=False, language_level=3, auto_pickle=False

from cpython.dict cimport PyDict_GetItemWithError
from cpython.ref cimport PyObject

cdef class _PyDictHandler:
    cdef readonly dict item
    cdef list _data
    cdef list stack
    cdef str attr_prefix, cdata_key

    def __cinit__(
        self,
        attr_prefix: str = "@",
        cdata_key: str = "#text",
        /,
    ):
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.item = {}
        self._data = []
        self.stack = []

    def characters(self, data):
        self._data.append(data)

    def startElement(self, name, dict attrs, /):
        self.stack.append(self.item)
        self.stack.append(self._data)
        self._data = []
        self.item = {self.attr_prefix + k: v for k, v in attrs.items()} if attrs else {}
                
    def endElement(self, name):
        if not self.stack:
            return
        
        text = "".join(self._data).strip() or None
        item = self.item
        self._data = self.stack.pop()
        self.item = self.stack.pop()

        if item and text:
            item[self.cdata_key] = text
        value = item or text

        cdef PyObject* existing
        existing = PyDict_GetItemWithError(self.item, name)

        if existing == NULL:
            self.item[name] = value
        elif type(<object>existing) is list:
            (<list>existing).append(value)
        else:
            self.item[name] = [<object>existing, value]
