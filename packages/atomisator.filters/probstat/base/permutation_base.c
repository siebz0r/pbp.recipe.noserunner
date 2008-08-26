#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "permutation.h"
#include "combination.h"
#include "size_lookup_permute.h"

/* parts of this code from http://sources.redhat.com/gsl/, which is in turn
   probably from somewhere else (public domain?) */

static void permute_init_data(permute_head *ph) { // reset ph->data to initial state
  unsigned int i;
  for (i = 0; i < ph->pick; i++) {
    ph->p_data[i] = i;
  }
  return;
}

static unsigned int permute_calculate_rows(permute_head *ph) {
  unsigned int tot = 1;
  unsigned int i;

  tot = GET_PERMUTE_SIZE(ph->size, ph->pick);
  if (!tot) { // not in the quick lookup table, try by hand
    tot = 1;
    // first the n!
    for (i = ph->pick; i > 0; i--) {
      tot *= i;
    }
    if (ph->data) { // then optional N choose k
      tot *= combination_calculate_NK(ph->size, ph->pick);
    }
  }

  return tot;
}

void permute_free(permute_head *ph) {
  assert (*ph->refcount > 0); // test for the impossible

  *ph->refcount = *ph->refcount - 1;
  if (*ph->refcount == 0) { // last one, free everything
    free(ph->values);
    ph->values = NULL;
    free(ph->refcount);
    ph->refcount = NULL;
  }
  // free personal data
  free(ph->p_data);
  ph->p_data = NULL;
  if (ph->data) { // if we are doing 5 choose 3
    free(ph->data);
    ph->data = NULL;
  }
  free(ph);
  return;
}

permute_head *permute_new(unsigned int size, unsigned int pick, BASETYPE_L list) {
  permute_head *newp = NULL;
  unsigned int i;
  unsigned int tot;

  newp = (permute_head *) malloc(sizeof(permute_head)); // alloc the head struct
  newp->size = size;
  newp->pick = pick;

  // copy the values pointers to the head struct
  newp->values = (BASETYPE_L ) malloc(newp->size * sizeof(BASETYPE));
  for (i = 0; i < newp->size; i++) {
    newp->values[i] = list[i];
  }

  // should newp->data be size or pick long?
  if (newp->pick < newp->size) {
    newp->data = (unsigned int *) malloc(newp->pick * sizeof(int));
    combination_init_data((combo_head *)newp);
  } else {
    newp->data = NULL;
  }
  newp->p_data = (unsigned int *) malloc(newp->pick * sizeof(int));
  permute_init_data(newp);

  newp->count = 0;
  newp->orig_count = 0;

  // calculate the count
  tot = permute_calculate_rows(newp);
  newp->end = tot;
  newp->orig_end = tot;

  newp->refcount = (unsigned int *) malloc(sizeof(unsigned int));
  *newp->refcount = 1;
  
  newp->one_more = 1;

  return newp;
}

permute_head *permute_clone(permute_head *oldp) {
  permute_head *newp;

  newp = (permute_head *) malloc(sizeof(permute_head)); // alloc the head struct

  newp->pick = oldp->pick;
  newp->size = oldp->size;
  newp->count = oldp->count;
  newp->orig_count = oldp->orig_count;
  newp->end = oldp->end;
  newp->orig_end = oldp->orig_end;
  newp->refcount = oldp->refcount;
  newp->values = oldp->values;
  newp->one_more = oldp->one_more;

  // should newp->data be size or pick long?
  if (oldp->data) {
    newp->data = (unsigned int *) malloc(newp->pick * sizeof(int));
    combination_init_data((combo_head *)newp);
  } else {
    newp->data = NULL;
  }
  newp->p_data = (unsigned int *) malloc(newp->pick * sizeof(int));
  permute_init_data(newp);

  *newp->refcount = *newp->refcount + 1;
  return newp;
}


static void permute_cp_current(permute_head *ph, BASETYPE_L ret_list) {
  unsigned int i;

  if (ph->data) { // combo is in use
    for (i = 0; i < ph->pick; i++) {
      // ph->data is a permutation of the values in c_data
      // ph->c_data is a list of indicies into ph->values
      ret_list[i] = ph->values[ph->data[ph->p_data[i]]];
    }
  } else {
    // ph->data is a list of indicies into ph->values
    for (i = 0; i < ph->pick; i++) {
      ret_list[i] = ph->values[ph->p_data[i]];
    }
  }
  return;
}

static int permute_plain_inc(permute_head *ph) {
  unsigned int pick = ph->pick;
  unsigned int i, j, k;
  unsigned int tmp;
  unsigned int *data = ph->p_data;

  i = pick - 2;

  while ((data[i] > data[i+1]) && (i != 0)) {
    i--;
  }

  if ((i == 0) && (data[0] > data[1])) {
    return 0;
  }

  k = i + 1;

  for (j = i + 2; j < pick; j++ ) {
    if ((data[j] > data[i]) && (data[j] < data[k])) {
      k = j;
    }
  }

  /* swap i and k */
  tmp = data[i];
  data[i] = data[k];
  data[k] = tmp;

  for (j = i + 1; j <= ((pick + i) / 2); j++) {
    tmp = data[j];
    data[j] = data[pick + i - j];
    data[pick + i - j] = tmp;
  }
  return ph->pick;
}

static int permute_combo_inc(permute_head *ph) {
  int retval;

  if ((retval = permute_plain_inc(ph)) != ph->pick) {
    // try getting another combination
    if ((retval = combination_inc((combo_head *)ph))) {
      permute_init_data(ph); // reset ph->p_data
    } else if (ph->one_more) {
      ph->one_more = 0;
      retval = ph->pick;
    }
  }
  return retval;
}

// int return value is ph->pick on success, -1 on error, 0 on finished
int permute_inc(permute_head *ph) {
  int retval;

  // increment our structs
  if (ph->data) { // N choose k
    retval = permute_combo_inc(ph);
  } else { // plain permute
    retval = permute_plain_inc(ph);
    if (ph->one_more && retval != ph->pick) {
      ph->one_more = 0;
      retval = ph->pick;
    }
  }
  return retval;
}

void permute_dump(permute_head *ch) {
  unsigned int i;

  printf("size %d, pick %d\n", ch->size, ch->pick);
  if (ch->p_data) {
    for (i = 0; i < ch->pick; i++) {
      printf("%d  ", ch->p_data[i]);
    }
    printf("\n");
  }
}


static unsigned int permute_set_count(permute_head *ph, unsigned int place) {
  unsigned int combo_mult;
  if (ph->data) {
    combo_mult = combination_calculate_NK(ph->size, ph->pick);
    ph->count = (place / combo_mult) * combo_mult;
    combination_set_count((combo_head *)ph, place / combo_mult);
    place = place % combo_mult;
  }
  if (place < ph->count) {
    permute_init_data(ph);
    ph->count = 0;
  }
  while (ph->count < place) {
    permute_inc(ph);
    ph->count++;
  }
  return ph->pick;
}

unsigned int permute_length(permute_head *ph) {
  return (ph->orig_end - ph->orig_count);
}

/*
 permute_smart_item figures out if we are iterating through a sequence,
 or just doing a one-off eg, for (i) in ob:  VS ob[123]
*/
int
permute_smart_item(permute_head *ph, BASETYPE_L ret_list, unsigned int pos) {
  // check bounds
  pos += ph->orig_count; // make relative pos absolute
  if (pos >= ph->orig_end) {
    return 0;
  }

  if (pos == ph->count) { // same as current
    // do nothing
  } else if (pos == (ph->count + 1)) { // increment
    permute_inc(ph);
    ph->count++;
  } else { // set to arbitrary
    permute_set_count(ph, pos);
  }
  permute_cp_current(ph, ret_list);
  return ph->pick;
}

int permute_set_slice(permute_head *ph, unsigned int start, unsigned int finish) {
  unsigned int new_start, new_finish;

  new_start = ph->orig_count + start;
  new_finish = ph->orig_count + finish;
  if (ph->end < new_start || start < 0 ||
      ph->end < new_finish || finish < 0) {
    return -1;
  }
  ph->count = new_start;
  ph->orig_count = new_start;
  ph->end = new_finish;
  ph->orig_end = new_finish;

  permute_set_count(ph, new_start);
  return 1;
}
  
