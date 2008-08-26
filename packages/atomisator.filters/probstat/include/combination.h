#ifndef _COMBINATION_H
#define _COMBINATION_H
#include "stats_module.h"

typedef struct combo_head_ {
  // Begin donchange (these must match permutation.h)
  unsigned int size;
  unsigned int pick;
  unsigned int *data;
  // End dontchange
  BASETYPE_L values;
  unsigned int count; // counter of our steps
  unsigned int orig_count; // used for slices
  unsigned int end; // when count == end, we are done
  unsigned int orig_end; // used for slices
  unsigned int *refcount; // our ref count (used for slices)
} combo_head;

combo_head *combination_new(unsigned int size, BASETYPE_L list, unsigned int pick);
void combination_free(combo_head *ch);
int combination_length(combo_head *ch);
int combination_set_slice(combo_head *ch, unsigned int start, unsigned int finish);
combo_head *combination_clone(combo_head *ch);
int combination_smart_item(combo_head *ch, BASETYPE_L ret_list, unsigned int item);

/* Also called from premutation */
void combination_set_count(combo_head *ch, unsigned int place);
int combination_inc(combo_head *ch); // increment the struct
void combination_init_data(combo_head *ch); // reset ch->data to inital form
void combo_dump(combo_head *ch); // DEBUG
unsigned int combination_calculate_NK(unsigned int n, unsigned int k);
#endif /* ifndef _COMBINATION_H */
