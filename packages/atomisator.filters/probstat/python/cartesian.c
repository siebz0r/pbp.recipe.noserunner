#include "Python.h"
#include <stdio.h>
#include "stats_module.h"
#include "permutation.h"
#include "combination.h"
#include "cartesian.h"

/*
 * NB, BASETYPE is PyObject *
 */

#define CartesianObject_Check(v)	((v)->ob_type == &PyCartesian_Type)

staticforward PyTypeObject PyCartesian_Type;

/*
 * Cartesian interface
 */

typedef struct {
	PyObject_HEAD
	cartesian_head *ch;
        BASETYPE_LL orig_list; // all members of orignal list, used to manipulate ref counts
        BASETYPE_L list_buff; // ch->k sized list, used in comination_base.c interface
        unsigned int *sizes; // sizeof the lists in orig_list
} CartesianObject;

static CartesianObject *
newCartesianObject(PyObject *list)
{
        unsigned int num_lists, size;
        unsigned int i, j;
        PyObject *tlist;
        BASETYPE item;
	CartesianObject *self;

	self = PyObject_New(CartesianObject, &PyCartesian_Type);
	if (self == NULL)
          return NULL;

        num_lists = PyList_GET_SIZE(list);

        self->orig_list = (BASETYPE_LL) malloc(num_lists * sizeof(BASETYPE_L));
        if (self->orig_list == NULL)
          return NULL;

        self->list_buff = (BASETYPE_L) malloc(num_lists * sizeof(BASETYPE));
        if (self->list_buff == NULL)
          return NULL;

        self->sizes = (unsigned int *) malloc(num_lists * sizeof(unsigned int));
        if (self->sizes == NULL)
          return NULL;

        size = 0; // keeps the compiler quiet
        for (i = 0; i < num_lists; i++) {
          tlist = PyList_GET_ITEM(list, i);
          size = PyList_GET_SIZE(tlist);
          self->sizes[i] = size;
          self->orig_list[i] = (BASETYPE_L) malloc(size * sizeof(BASETYPE));
          if (self->orig_list[i] == NULL)
            return NULL;
          for (j = 0; j < size; j++) {
            item = PyList_GET_ITEM(tlist, j);
            Py_INCREF(item);
            self->orig_list[i][j] = item;
          }
        }

        self->ch = cartesian_new(num_lists, self->orig_list, self->sizes);
        if (self->ch == NULL)
          return NULL;

	return self;
}

static void
Cartesian_dealloc(CartesianObject *self)
{
  unsigned int i, j;

  /* we are the last, free everything */
  if (*self->ch->refcount == 1) {
    // decrement the orginal list
    for (i = 0; i < self->ch->size; i++) {
      for (j = 0; j < self->sizes[i]; j++) {
	Py_DECREF(self->orig_list[i][j]);
      }
      free(self->orig_list[i]);
      self->orig_list[i] = NULL;
    }
    free(self->orig_list);
    self->orig_list = NULL;
    free(self->sizes);
    self->sizes = NULL;
  }
  /* always free list buff and the cartesian_head struct */
  free(self->list_buff);
  self->list_buff = NULL;
  cartesian_free(self->ch); /* handles ch->refcount-- */
  PyObject_Del(self);
}

static PyObject *
Cartesian_item(CartesianObject *self, int i)
{
  PyObject *ret_list;
  PyObject *item;
  int ok;

  ok = cartesian_smart_item(self->ch, self->list_buff, (long long)i);
  if (ok == self->ch->size) {
    ret_list = (PyObject *)PyList_New(self->ch->size);
    if (ret_list == NULL) {
      return NULL;
    }
    for (i = 0; i < self->ch->size; i++) {
      item = self->list_buff[i];
      Py_INCREF(item);
      PyList_SET_ITEM(ret_list, i, item);
    }
    return ret_list;
  } else if (ok < 0) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Cartesian out of memory error");
  } else {
    PyErr_SetString(PyExc_IndexError,
		    "Cartesian Index out of bounds");
  }
  return NULL;
}

static int
Cartesian_length(CartesianObject *self)
{
  return  (int)cartesian_get_length(self->ch);
}

static PyObject *
Cartesian_slice(CartesianObject *self, int ilow, int ihigh)
{
  CartesianObject *newob;
  cartesian_head *newhead;

  newhead = cartesian_clone(self->ch); /* clone our base struct */

  /* We are less forgiving that PyList for bounds */
  if (cartesian_set_slice(newhead, (long long)ilow, (long long)ihigh) == -1) {
    cartesian_free(newhead);
    PyErr_SetString(PyExc_IndexError,
		    "Cartesian slice, index out of bounds");
    return NULL;
  }

  /* new a CartesianObject to return */
  newob = PyObject_New(CartesianObject, &PyCartesian_Type);
  if (newob == NULL)
    return NULL;
  
  newob->sizes = self->sizes;
  newob->orig_list = self->orig_list;

  /* we need our our list_buff, 
     but not orig_list and sizes can be shared (read-only) */
  newob->list_buff = (BASETYPE_L) malloc(self->ch->size * sizeof(BASETYPE));
  if (newob->list_buff == NULL)
    return NULL;
  
  newob->ch = newhead;

  return (PyObject *)newob;
}
  
static PySequenceMethods Cartesian_as_sequence = {
        (inquiry)Cartesian_length, /*sq_length*/
        0, /*sq_concat*/
        0, /*sq_repeat*/
        (intargfunc)Cartesian_item, /*sq_item*/
	(intintargfunc)Cartesian_slice, /*sq_slice*/
};

static PyMethodDef Cartesian_methods[] = {
	{NULL,		NULL}		/* sentinel */
};

static PyObject *
Cartesian_getattr(CartesianObject *self, char *name)
{
        return Py_FindMethod(Cartesian_methods, (PyObject *)self, name);
}

statichere PyTypeObject PyCartesian_Type = {
    PyObject_HEAD_INIT(NULL)	/* fix up the type slot in the init fucntion */
	0,			/*ob_size*/
	"Cartesian",		/*tp_name*/
	sizeof(CartesianObject),	/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)Cartesian_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)Cartesian_getattr, /*tp_getattr*/
	0, //(setattrfunc)Permute_setattr, /*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	&Cartesian_as_sequence,	/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
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
        Cartesian_methods,        /*tp_methods*/
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

/* not static so stats_module.c can see it */
PyObject *
stats_cartesian(PyObject *self, PyObject *args)
{
        CartesianObject *rv;
        int i, list_size;
        PyObject *list = NULL;
	
	if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list))
		return NULL;

        list_size = PyList_GET_SIZE(list);
        // do more specific error checking
        if (list_size == 0) {
          PyErr_SetString(PyExc_ValueError, "List cannot be empty");
          return NULL;
        }
        for (i = 0; i < list_size; i++) {
          if (!PyList_Check(PyList_GET_ITEM(list, i))) {
            PyErr_SetString(PyExc_ValueError, "Elements of the list argument must also be lists");
            return NULL;
          }
        }

        // call object create function and return
	rv = newCartesianObject(list);
	if ( rv == NULL ) {
          return NULL;
        }
	return (PyObject *)rv;
}
