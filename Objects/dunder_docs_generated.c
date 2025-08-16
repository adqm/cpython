#include "Python.h"
#include "pycore_dunder_docs.h"

int
_Py_BuildDunderDocs(PyObject *target) {
    fprintf(stderr, "hello!");
    return 0;
};
