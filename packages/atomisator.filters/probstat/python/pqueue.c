#include "Python.h"
#include <stdio.h>
#include "stats_module.h"
#include "pqueue.h"

#define PQueueObject_Check(v)    ((v)->ob_type == &PyQueue_Type)
 
staticforward PyTypeObject PyPQueue_Type;

typedef struct {
        PyObject_HEAD
	int direction;
	pqueue *queue;
} PQueueObject;

static void
PQueue_free_node(node *np) {
  PyObject * pob;

  pob = np->data;
  Py_DECREF(pob);
  free(np);
}

static void
PQueue_dealloc(PQueueObject *self) {
  node *p;
  while ((p = pqremove(self->queue)) != NULL) {
    PQueue_free_node(p);
  }
  free(self->queue);
  self->queue = NULL;
  PyObject_Del(self);
}

static PyObject *
PQueue_peek(PQueueObject *self, PyObject *args) {
  node *np;
  PyObject *pob;

  if ((np = pqpeek(self->queue)) == NULL)
    return NULL;
  
  pob = np->data;
  Py_INCREF(pob);
  return pob;
}

static PyObject *
PQueue_pop(PQueueObject *self, PyObject *args) {
  node *np;
  PyObject *ret_tup;

  if ((np = pqremove(self->queue)) == NULL) {
    return NULL;
  }

  ret_tup = np->data;
  Py_INCREF(ret_tup);
  PQueue_free_node(np); // calls DECREF on pob
  return ret_tup;
}

static PyObject *
PQueue_push(PQueueObject *self, PyObject *args) {
  int priority;
  node *np;
  PyObject *tup;

  if (!PyArg_ParseTuple(args, "O!:PQueue", &PyTuple_Type, &tup))
    return NULL;

  if (PyTuple_GET_SIZE(tup) != 2) {
    PyErr_SetString(PyExc_ValueError, "argument must be a tuple of size two (priority, data)");
    return NULL;
  }

  np = (node *) malloc(sizeof(node));
  Py_INCREF(tup);
  np->data = tup;
  priority = (int)PyInt_AsLong(PyTuple_GET_ITEM(tup, 0));
  if (self->direction >= 0)
    np->priority = priority;
  else
    np->priority = - priority;

  if (!pqinsert(self->queue, np)) {
    return NULL;
  }

  Py_INCREF(self);
  return (PyObject *)self; // just reutrn ourselves as an lvalue
}

static PyMethodDef PQueue_methods[] = {
  {"peek", (PyCFunction)PQueue_peek, METH_NOARGS},
  {"push", (PyCFunction)PQueue_push, METH_VARARGS},
  {"pop", (PyCFunction)PQueue_pop, METH_NOARGS},
  {NULL,                NULL}           /* sentinel */
};

static PyObject *
PQueue_getattr(PQueueObject *self, char *name)
{
        return Py_FindMethod(PQueue_methods, (PyObject *)self, name);
}

static int
PQueue_length(PQueueObject *self) {
  return (self->queue->size - 1);
}

static PySequenceMethods PQueue_as_sequence = {
        (inquiry)PQueue_length, /*sq_length*/
};

statichere PyTypeObject PyPQueue_Type = {
        PyObject_HEAD_INIT(NULL)	/* fix up the type slot in the init fucntion */
        0,                      /*ob_size*/
        "PQueue",               /*tp_name*/
        sizeof(PQueueObject),   /*tp_basicsize*/
        0,                      /*tp_itemsize*/
        /* methods */
        (destructor)PQueue_dealloc, /*tp_dealloc*/
        0,                      /*tp_print*/
        (getattrfunc)PQueue_getattr, /*tp_getattr*/
        0, //(setattrfunc)Permute_setattr, /*tp_setattr*/
        0,                      /*tp_compare*/
        0,                      /*tp_repr*/
        0,                      /*tp_as_number*/
        &PQueue_as_sequence,                      /*tp_as_sequence*/
        0,                      /*tp_as_mapping*/
        0,                      /*tp_hash*/
        0,                      /*tp_call*/
        0,                      /*tp_str*/
        0,                      /*tp_getattro*/
        0,                      /*tp_setattro*/
        0,                      /*tp_as_buffer*/
        Py_TPFLAGS_DEFAULT,     /*tp_flags*/
        0,                      /*tp_doc*/
        0,                      /*tp_traverse*/
        0,                      /*tp_clear*/
        0,                      /*tp_richcompare*/
        0,                      /*tp_weaklistoffset*/
        0,                      /*tp_iter*/
        0,                      /*tp_iternext*/
        PQueue_methods,         /*tp_methods*/
        0,                      /*tp_members*/
        0,                      /*tp_getset*/
        0,                      /*tp_base*/
        0,                      /*tp_dict*/
        0,                      /*tp_descr_get*/
        0,                      /*tp_descr_set*/
        0,                      /*tp_dictoffset*/
        0,                      /*tp_init*/
        0,                      /*tp_alloc*/
        0,                      /*tp_new*/
        0,                      /*tp_free*/
        0,                      /*tp_is_gc*/
};

// not static so stats_module.c can see it
PyObject *
stats_pqueue(PyObject *self, PyObject *args)
{
        PQueueObject *rv;
        int initial_size = 0;
	int direction = 1;
 
        if (!PyArg_ParseTuple(args, "|ii:PQueue", &initial_size, &direction))
	  return NULL;
 
	if (!initial_size)
	  initial_size = 100;

        // call object create function and return
        rv = PyObject_New(PQueueObject, &PyPQueue_Type);
        if (rv == NULL)
          return NULL;
 
	rv->queue = (pqueue *) malloc(sizeof(pqueue));
	pqinit(rv->queue, initial_size);
	rv->direction = direction;
 
        return (PyObject *)rv;
}
