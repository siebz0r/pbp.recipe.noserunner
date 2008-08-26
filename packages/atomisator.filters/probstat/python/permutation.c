#include "Python.h"
#include <stdio.h>
#include "stats_module.h"
#include "permutation.h"

#define PermutationObject_Check(v)	((v)->ob_type == &PyPermutation_Type)

staticforward PyTypeObject PyPermutation_Type;

/*
 * Permutation interface
 */

typedef struct {
	PyObject_HEAD
	permute_head *ph;
        BASETYPE *list_buff; // we use this buffer to communicate with permute_base.c routines
        BASETYPE *orig_list; // store the orignal list, used to manipulate ref count
} PermutationObject;

static PermutationObject *
newPermutationObject(PyObject *list, int pick)
{
	PermutationObject *self;
        BASETYPE item;
        int size, i;

	self = PyObject_New(PermutationObject, &PyPermutation_Type);
	if (self == NULL)
		return NULL;

        size = PyList_GET_SIZE(list);
        self->list_buff = (BASETYPE *)malloc(pick * sizeof(BASETYPE));
        if (self->list_buff == NULL) {
          return NULL;
        }
        self->orig_list = (BASETYPE *)malloc(size * sizeof(BASETYPE));
        if (self->orig_list == NULL) {
          return NULL;
        }

        // copy the values pointers to the orig_list
        for (i = 0; i < size; i++) {
          item = PyList_GET_ITEM(list, i);
          Py_INCREF(item);
          self->orig_list[i] = item;
        }

        self->ph = permute_new((unsigned int)size, (unsigned int)pick, self->orig_list);
        if (self->ph == NULL) {
          return NULL;
        }
	return self;
}

statichere void
Permutation_dealloc(PermutationObject *self)
{
  int i;

  if (*self->ph->refcount == 1) { // free everything shared
    // DECREF self->orig_list and free
    for (i = 0; i < self->ph->size; i++) {
      Py_DECREF(self->orig_list[i]);
    }
    free(self->orig_list);
    self->orig_list = NULL;
  }
  // free everything else
  free(self->list_buff);
  self->list_buff = NULL;
  permute_free(self->ph);
  PyObject_Del(self);
}

static int
Permutation_length(PermutationObject *self)
{
  return (int)permute_length(self->ph);
}

static PyObject *
Permutation_item(PermutationObject *self, int i)
{
  PyObject *ret_list;
  BASETYPE item;
  int ok;

  ok = permute_smart_item(self->ph, self->list_buff, (unsigned int)i);
  if (ok == self->ph->pick) {
    // construct the list and return
    ret_list = (PyObject *)PyList_New(self->ph->pick);
    if (ret_list == NULL) {
      return NULL;
    }
    for (i = 0; i < self->ph->pick; i++) {
      item = self->list_buff[i];
      Py_INCREF(item);
      PyList_SET_ITEM(ret_list, i, item);
    }
    return ret_list;
  } else if (ok < 0) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Permutation out of memory error");
    return NULL;
  } else {
    PyErr_SetString(PyExc_IndexError,
		    "Permutation Index out of bounds");
  }
  return NULL;
}

static PyObject *
Permutation_slice(PermutationObject *self, int ilow, int ihigh)
{
  PermutationObject *newob;
  permute_head *newhead;

  newhead = permute_clone(self->ph); /* clone our base struct */

  /* We are less forgiving that PyList for bounds */
  if (ilow < 0 || ihigh < 0 || permute_set_slice(newhead, (unsigned int)ilow
, (unsigned int)ihigh) == -1) {
    permute_free(newhead);
    PyErr_SetString(PyExc_IndexError,
                    "Permutation slice, index out of bounds");
    return NULL;
  }

  /* new a CombinationObject to return */
  newob = PyObject_New(PermutationObject, &PyPermutation_Type);
  if (newob == NULL)
    return NULL;
  
  newob->orig_list = self->orig_list;

  /* we need our our list_buff, 
     but not orig_list and sizes can be shared (read-only) */
  newob->list_buff = (BASETYPE_L) malloc(self->ph->pick * sizeof(BASETYPE));
  if (newob->list_buff == NULL)
    return NULL;
  
  newob->ph = newhead;
  return (PyObject *)newob;
}


static PySequenceMethods Permutation_as_sequence = {
        (inquiry)Permutation_length, /*sq_length*/
        0, /*sq_concat*/
        0, /*sq_repeat*/
        (intargfunc)Permutation_item, /*sq_item*/
	(intintargfunc)Permutation_slice, /*sq_slice*/
};

static PyMethodDef Permutation_methods[] = {
	{NULL,		NULL}		/* sentinel */
};

static PyObject *
Permutation_getattr(PermutationObject *self, char *name)
{
        return Py_FindMethod(Permutation_methods, (PyObject *)self, name);
}

statichere PyTypeObject PyPermutation_Type = {
    PyObject_HEAD_INIT(NULL)	/* fix up the type slot in the init fucntion */
	0,			/*ob_size*/
	"Permutation",		/*tp_name*/
	sizeof(PermutationObject),	/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)Permutation_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)Permutation_getattr, /*tp_getattr*/
	0, //(setattrfunc)Permute_setattr, /*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	&Permutation_as_sequence,/*tp_as_sequence*/
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
        Permutation_methods,        /*tp_methods*/
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

/* Not static so stats_module.c can see it */
PyObject *
stats_permutation(PyObject *self, PyObject *args)
{
	PermutationObject *rv;
        PyObject *list = NULL;
	int int_arg = -69; // magic number, kinda
	int list_size;
	
	if (!PyArg_ParseTuple(args, "O!|i:Permutation", &PyList_Type, &list, &int_arg))
		return NULL;

        // do more specific error checking
        list_size = PyList_GET_SIZE(list);
        if (list_size == 0) {
          PyErr_SetString(PyExc_ValueError, "List cannot be empty");
          return NULL;
        }
	if (int_arg == -69) { // magic number, kinda
	  int_arg = list_size;
	} else {
	  if (int_arg <= 0) {
	    PyErr_SetString(PyExc_ValueError, "optional integer argument must be positive");
	    return NULL;
	  } else if (int_arg >= list_size) {
	    PyErr_SetString(PyExc_ValueError, "optional integer argument must be less than the list size");
	    return NULL;
	  }
	}

	rv = newPermutationObject(list, int_arg);
	if ( rv == NULL )
	    return NULL;
	return (PyObject *)rv;

}
