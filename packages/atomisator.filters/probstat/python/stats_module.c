#include "Python.h"
#include <stdio.h>
#include "stats_module.h"

/*
 * stats module interface
 */

static PyTypeObject PyCartesian_Type;
static PyTypeObject PyCombination_Type;
static PyTypeObject PyPermutation_Type;
static PyTypeObject PyPQueue_Type;

static PyObject *ErrorObject;

static PyMethodDef stats_methods[] = {
        {"Permutation",  stats_permutation,      METH_VARARGS},
        {"Combination",  stats_combination,      METH_VARARGS},
        {"Cartesian",    stats_cartesian,        METH_VARARGS},
        {"PQueue",       stats_pqueue,           METH_VARARGS},
	{NULL,		NULL}		/* sentinel */
};

/* Initialization function for the module (*must* be called initxx) */

DL_EXPORT(void)
initprobstat(void)
{
	PyObject *m, *d;
    
    /* Fix up the type slots of the type objects.   */
    PyCartesian_Type.ob_type = &PyType_Type;
	PyCombination_Type.ob_type = &PyType_Type;
    PyPermutation_Type.ob_type = &PyType_Type;
    PyPQueue_Type.ob_type = &PyType_Type;
    
    /* Create the module and add the functions */
	m = Py_InitModule("probstat", stats_methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);
	ErrorObject = PyErr_NewException("probstat.error", NULL, NULL);
	PyDict_SetItemString(d, "error", ErrorObject);
}
