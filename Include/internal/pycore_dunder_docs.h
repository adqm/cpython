#ifndef Py_INTERNAL_DUNDER_DOCS_H
#define Py_INTERNAL_DUNDER_DOCS_H
#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"

PyAPI_FUNC(int) _Py_BuildDunderDocs(PyObject *target);

#ifdef __cplusplus
}
#endif
#endif
