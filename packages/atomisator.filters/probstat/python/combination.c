#include "Python.h"
#include <stdio.h>
#include "stats_module.h"
#include "combination.h"

#define CombinationObject_Check(v)	((v)->ob_type == &PyCombination_Type)

staticforward PyTypeObject PyCombination_Type;

/*
 * Combination interface
 */

typedef struct {
	PyObject_HEAD
	combo_head *ch;
        BASETYPE_L orig_list; // all members of orignal list, used to manipulate ref counts
        BASETYPE_L list_buff; // ch->pick sized list, used in comination_base.c interface
} CombinationObject;

static CombinationObject *
newCombinationObject(PyObject *list, unsigned int pick)
{
        unsigned int size;
        unsigned int i;

	CombinationObject *self;
	self = PyObject_New(CombinationObject, &PyCombination_Type);
	if (self == NULL)
          return NULL;
        
        size = PyList_GET_SIZE(list);

        self->orig_list = (BASETYPE_L)malloc(size * sizeof(BASETYPE));
        if (self->orig_list == NULL)
          return NULL;

        self->list_buff = (BASETYPE_L)malloc(pick * sizeof(BASETYPE));
        if (self->list_buff == NULL)
          return NULL;

        for (i = 0; i < size; i++) {
          self->orig_list[i] = PyList_GET_ITEM(list, i);
          Py_INCREF(self->orig_list[i]);
        }

        self->ch = combination_new(size, self->orig_list, pick);
        if (self->ch == NULL)
          return NULL;
	return self;
}

static void
Combination_dealloc(CombinationObject *self)
{
  unsigned int i;

  if (*self->ch->refcount == 1) {
    // decrement the orginal list
    for (i = 0; i < self->ch->size; i++) {
      Py_DECREF(self->orig_list[i]);
    }
    free(self->orig_list);
    self->orig_list = NULL;
  }
  free(self->list_buff);
  self->list_buff = NULL;
  combination_free(self->ch); // takes care of refcount--
  PyObject_Del(self);
}

static int
Combination_length(CombinationObject *self)
{
  return (int)combination_length(self->ch);
}

static PyObject *
Combination_item(CombinationObject *self, int i)
{
  PyObject *ret_list;
  BASETYPE item;
  int ok;

  ok = combination_smart_item(self->ch, self->list_buff, i);
  if (ok == self->ch->pick) {
    // construct the list and return
    ret_list = (PyObject *)PyList_New(self->ch->pick);
    if (ret_list == NULL) {
      return NULL;
    }
    for (i = 0; i < self->ch->pick; i++) {
      item = self->list_buff[i];
      Py_INCREF(item);
      PyList_SET_ITEM(ret_list, i, item);
    }
    return ret_list;
  } else if (ok == -1) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Combination out of memory error");
    return NULL;
  } else {
    PyErr_SetString(PyExc_IndexError,
		    "Combination Index out of bounds");
  }
  return NULL;
}

static PyObject *
Combination_slice(CombinationObject *self, int ilow, int ihigh)
{
  CombinationObject *newob;
  combo_head *newhead;

  newhead = combination_clone(self->ch); /* clone our base struct */

  /* We are less forgiving that PyList for bounds */
  if (ilow < 0 || ihigh < 0 || combination_set_slice(newhead, (unsigned int)ilow, (unsigned int)ihigh) == -1) {
    combination_free(newhead);
    PyErr_SetString(PyExc_IndexError,
		    "Combination slice, index out of bounds");
    return NULL;
  }

  /* new a CombinationObject to return */
  newob = PyObject_New(CombinationObject, &PyCombination_Type);
  if (newob == NULL)
    return NULL;
  
  newob->orig_list = self->orig_list;

  /* we need our our list_buff, 
     but not orig_list and sizes can be shared (read-only) */
  newob->list_buff = (BASETYPE_L) malloc(self->ch->size * sizeof(BASETYPE));
  if (newob->list_buff == NULL)
    return NULL;
  
  newob->ch = newhead;

  return (PyObject *)newob;
}

static PySequenceMethods Combination_as_sequence = {
        (inquiry)Combination_length, /*sq_length*/
        0, /*sq_concat*/
        0, /*sq_repeat*/
        (intargfunc)Combination_item, /*sq_item*/
	(intintargfunc)Combination_slice, /*sq_slice*/
};

static PyMethodDef Combination_methods[] = {
	{NULL,		NULL}		/* sentinel */
};

static PyObject *
Combination_getattr(CombinationObject *self, char *name)
{
        return Py_FindMethod(Combination_methods, (PyObject *)self, name);
}

statichere PyTypeObject PyCombination_Type = {
    PyObject_HEAD_INIT(NULL)	/* fix up the type slot in the init fucntion */
	0,			/*ob_size*/
	"Combination",		/*tp_name*/
	sizeof(CombinationObject),	/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)Combination_dealloc, /*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)Combination_getattr, /*tp_getattr*/
	0, //(setattrfunc)Permute_setattr, /*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	&Combination_as_sequence,/*tp_as_sequence*/
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
        Combination_methods,        /*tp_methods*/
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
stats_combination(PyObject *self, PyObject *args)
{
        CombinationObject *rv;
        int int_arg, list_size;
        PyObject *list = NULL;
	
	if (!PyArg_ParseTuple(args, "O!i", &PyList_Type, &list, &int_arg))
		return NULL;

        list_size = PyList_GET_SIZE(list);
        // do more specific error checking
        if (list_size == 0) {
          PyErr_SetString(PyExc_ValueError, "List cannot be empty");
          return NULL;
        }
        if (int_arg <= 0) {
          PyErr_SetString(PyExc_IndexError, "second argument must be a positive integer");
          return NULL;
        } else if (int_arg > list_size) {
          PyErr_SetString(PyExc_ValueError, "second argument must be less than or equal to the size of the list");
          return NULL;
        }

        // call object create function and return
	rv = newCombinationObject(list, (unsigned int)int_arg);
	if ( rv == NULL )
          return NULL;
	return (PyObject *)rv;
}
