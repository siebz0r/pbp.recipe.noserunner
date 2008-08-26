#include <stdio.h>
#include "cartesian.h"

cartesian_head *cartesian_new(unsigned int size, BASETYPE_LL list, unsigned int *sizes) {
  cartesian_head *newc = NULL;
  long long total, new_total;
  unsigned int i, j;

  newc = (cartesian_head *) malloc(sizeof(cartesian_head)); // alloc the head struct
  newc->size = size;

  // copy the values to the head struct
  newc->values = (BASETYPE_LL) malloc(newc->size * sizeof(BASETYPE_L));
  for (i = 0; i < newc->size; i++) {
    newc->values[i] = (BASETYPE_L) malloc(sizes[i] * sizeof(BASETYPE));
    for (j = 0; j < sizes[i]; j++) {
      newc->values[i][j] = list[i][j];
    }
  }

  newc->div = (unsigned int *) malloc(newc->size * sizeof(unsigned int));
  newc->mod = (unsigned int *) malloc(newc->size * sizeof(unsigned int));

  total = new_total = 1;
  for (i = 0;i < newc->size; i++) {
    newc->div[i] = total;
    newc->mod[i] = sizes[i];
    // make sure we aren't exceeding the size ofour counter
    new_total = total * sizes[i];
    assert(new_total > total && "multiplying the sizes of the arrays exceeds the size of the counter!");
    total = new_total;
  }

  newc->refcount = (unsigned int *) malloc(sizeof(unsigned int));
  *newc->refcount = 1;
  newc->count = 0;
  newc->orig_count = 0;
  newc->total = total;
  newc->orig_total = total;

  return newc;
}

cartesian_head *cartesian_clone(cartesian_head *oldc) {
  cartesian_head *newc = NULL;

  newc = (cartesian_head *) malloc(sizeof(cartesian_head)); // alloc the head struct

  // link or copy all the values in oldc
  newc->size = oldc->size;
  newc->values = oldc->values;
  newc->total = oldc->total;
  newc->orig_total = oldc->orig_total;
  newc->count = oldc->count;
  newc->orig_count = oldc->orig_count;
  newc->div = oldc->div;
  newc->mod = oldc->mod;
  newc->refcount = oldc->refcount;

  // inc the shared refcount
  *newc->refcount = *newc->refcount + 1;

  return newc;
}

/* start and finish are relative to orig_count and orig_total */
int cartesian_set_slice(cartesian_head *ch, long long start, long long finish) {
  long long new_start, new_finish;

  new_start = ch->orig_count + start;
  new_finish = ch->orig_count + finish;
  if (ch->total < new_start || start < 0 ||
      ch->total < new_finish || finish < 0) {
    return -1;
  }
  ch->count = new_start;
  ch->orig_count = new_start;
  ch->total = new_finish;
  ch->orig_total = new_finish;
  return 1;
}

void cartesian_free(cartesian_head *ch) {
  unsigned int i;

  assert(*ch->refcount > 0); // test for the impossible

  *ch->refcount = *ch->refcount - 1; // decrement the refcount

  // free everything if we are the last man standing
  if (*ch->refcount == 0) {
    free(ch->div);
    ch->div = NULL;
    free(ch->mod);
    ch->mod = NULL;
    for (i = 0; i < ch->size; i++) {
      free(ch->values[i]);
      ch->values[i] = NULL;
    }
    free(ch->values);
    ch->values = NULL;
    free(ch->refcount);
    ch->refcount = NULL;
  }

  // always free ourselves
  free(ch);
}

int cartesian_smart_item(cartesian_head *ch, BASETYPE_L ret_list, long long c) {
  unsigned int i;
  c += ch->orig_count; // make relative position absolute
  if (c >= ch->orig_total) {
    return 0;
  }
  for (i = 0; i < ch->size; i++) {
    ret_list[i] = ch->values[i][(c / ch->div[i]) % ch->mod[i]];
  }
  return ch->size;
}

long long cartesian_get_length(cartesian_head *ch) {
  // we have to take slices into account, use ch->orig_*

  return (ch->orig_total - ch->orig_count);
}
