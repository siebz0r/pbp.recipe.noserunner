#ifndef _STATS_MODULE_H
#define _STATS_MODULE_H

#include "Python.h"

#define BASETYPE PyObject *
#define BASETYPE_L PyObject **
#define BASETYPE_LL PyObject *** // if this makes your head hurt, just pretend it didn't happen

PyObject *
stats_combination(PyObject *, PyObject *);

PyObject *
stats_permutation(PyObject *, PyObject *);

PyObject *
stats_cartesian(PyObject *, PyObject *);

PyObject *
stats_pqueue(PyObject *, PyObject *);
#endif /* _STATS_MODULE_H */
