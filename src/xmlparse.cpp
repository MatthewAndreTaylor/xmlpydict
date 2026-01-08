/**
 * Copyright (c) 2023 Matthew Andre Taylor
 */
#include <Python.h>
#include <stdio.h>
#include <string>
#include <vector>

static PyObject* strip(PyObject* s_obj) {
    Py_ssize_t start = 0;
    Py_ssize_t end = PyUnicode_GetLength(s_obj);
    while (start < end && std::isspace(PyUnicode_ReadChar(s_obj, start))) {
      ++start;
    }
    while (end > start && std::isspace(PyUnicode_ReadChar(s_obj, end - 1))) {
      --end;
    }
    return PyUnicode_Substring(s_obj, start, end);
}

typedef struct {
    PyObject_HEAD PyObject* item;          // current dict
    PyObject* data;        // character data buffer
    std::vector<PyObject*> item_stack;
    std::vector<PyObject*> data_stack;
    PyObject* attr_prefix;
    PyObject* cdata_key;
} PyDictHandler;

static PyObject* PyDictHandler_new(PyTypeObject* type, PyObject* args,
                            PyObject* kwargs) {
    PyDictHandler* self;
    self = (PyDictHandler*)type->tp_alloc(type, 0);
    return (PyObject*)self;
}

static int PyDictHandler_init(PyDictHandler* self, PyObject* args,
                          PyObject* kwargs) {
    const char* attr_prefix = "@";
    const char* cdata_key = "#text";
    static char* kwlist[] = {"attr_prefix", "cdata_key", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|ss", kwlist,
                                     &attr_prefix, &cdata_key))
        return -1;

    self->item = Py_None;
    self->data = PyUnicode_New(0, 127); // empty string
    self->attr_prefix = PyUnicode_FromString(attr_prefix);
    self->cdata_key = PyUnicode_FromString(cdata_key);
    return 0;
}

static PyObject* characters(PyDictHandler* self, PyObject* data_obj) {
    PyUnicode_Append(&self->data, data_obj);
    Py_RETURN_NONE;
}

static PyObject* startElement(PyDictHandler* self, PyObject* args) {
    self->item_stack.push_back(self->item);
    self->data_stack.push_back(self->data);
    self->data = PyUnicode_New(0, 127); // reset data buffer

    const char* name;
    PyObject* attrs;
    if (!PyArg_ParseTuple(args, "sO", &name, &attrs)) {
        return NULL;
    }

    if (!PyDict_Check(attrs) || PyDict_Size(attrs) == 0) {
        self->item = Py_None;
        Py_RETURN_NONE;
    }

    PyObject* newDict = PyDict_New();
    PyObject *key, *value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(attrs, &pos, &key, &value)) {
        PyObject* prefixed_key = PyUnicode_Concat(self->attr_prefix, key);
        PyDict_SetItem(newDict, prefixed_key, value);
    }

    self->item = newDict;
    Py_RETURN_NONE;
}

static PyObject* updateChildren(PyObject*& target, PyObject* key, PyObject* value) {
    if (target == Py_None) {
        target = PyDict_New();
    }

    if (!PyDict_Contains(target, key)) {
        PyDict_SetItem(target, key, value);
    } else {
        PyObject* existing = PyDict_GetItem(target, key);
        if (PyList_Check(existing)) {
            PyList_Append(existing, value);
        } else {
            PyObject* newList = PyList_New(2);
            PyList_SetItem(newList, 0, existing);
            PyList_SetItem(newList, 1, value);
            PyDict_SetItem(target, key, newList);
        }
    }
    return target;
}

static PyObject* endElement(PyDictHandler* self, PyObject* name_obj) {
    if (!self->data_stack.empty()) {
        PyObject* temp_data = strip(self->data);
        bool has_data = (PyUnicode_GetLength(temp_data) > 0);
        PyObject* py_data = has_data ? temp_data : Py_None;
        PyObject* temp_item = self->item;

        self->item = self->item_stack.back();
        self->data = self->data_stack.back();
        self->item_stack.pop_back();
        self->data_stack.pop_back();

        if (temp_item != Py_None) {
            if (has_data) {
                PyDict_SetItem(temp_item, self->cdata_key, py_data);
            }
            temp_item = PyDict_Copy(temp_item);
            self->item = updateChildren(self->item, name_obj, temp_item);
        }
        else {
            self->item = updateChildren(self->item, name_obj, py_data);
        }
    }
    Py_RETURN_NONE;
}



static PyMethodDef PyDictHandler_methods[] = {
    {"characters", (PyCFunction)characters, METH_O, "Handle character data"},
    {"startElement", (PyCFunction)startElement, METH_VARARGS, "Handle start of an element"},
    {"endElement", (PyCFunction)endElement, METH_O, "Handle end of an element"},
    {NULL, NULL, 0, NULL}
};

static PyObject* PyDictHandler_get_item(PyDictHandler *self, void *closure)
{
    Py_INCREF(self->item);
    return self->item;
}

static PyGetSetDef PyDictHandler_getset[] = {
    {
        "item",                                   /* name */
        (getter)PyDictHandler_get_item,           /* get */
        NULL,           /* set */
        NULL,                    /* doc */
        NULL                                      /* closure */
    },
    {NULL}  /* Sentinel */
};


static PyTypeObject PyDictHandlerType = {
    PyVarObject_HEAD_INIT(NULL, 0) "pyxmlhandler._PyDictHandler", // tp_name
    sizeof(PyDictHandler),                                    // tp_basicsize
    0,                                                        // tp_itemsize
    0,                                                        // tp_dealloc
    0,                                                        // tp_vectorcall_offset
    0,                                                        // tp_getattr
    0,                                                        // tp_setattr
    0,                                                        // tp_as_async
    0,                                                        // tp_repr
    0,                                                        // tp_as_number
    0,                                                        // tp_as_sequence
    0,                                                        // tp_as_mapping
    0,                                                        // tp_hash
    0,                                                        // tp_call
    0,                                                        // tp_str
    0,                                                        // tp_getattro
    0,                                                        // tp_setattro
    0,                                                        // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                // tp_flags
    "Handler that converts XML to Python dict",               // tp_doc
    0,                                                        // tp_traverse
    0,                                                        // tp_clear
    0,                                                        // tp_richcompare
    0,                                                        // tp_weaklistoffset
    0,                                                        // tp_iter
    0,                                                        // tp_iternext
    PyDictHandler_methods,                                    // tp_methods
    0,                                                        // tp_members
    PyDictHandler_getset,                                     // tp_getset
    0,                                                        // tp_base
    0,                                                        // tp_dict
    0,                                                        // tp_descr_get
    0,                                                        // tp_descr_set
    0,                                                        // tp_dictoffset
    (initproc)PyDictHandler_init,                             // tp_init
    0,                                                        // tp_alloc
    PyDictHandler_new,                                        // tp_new
};

static PyModuleDef pyxmlhandlermodule = {
    PyModuleDef_HEAD_INIT,
    "pyxmlhandler",
    "Module that provides XML to Python dict parsing",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_pyxmlhandler(void) {
    PyObject* m;
    if (PyType_Ready(&PyDictHandlerType) < 0)
        return NULL;

    m = PyModule_Create(&pyxmlhandlermodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyDictHandlerType);
    PyModule_AddObject(m, "_PyDictHandler", (PyObject*)&PyDictHandlerType);
    return m;
}