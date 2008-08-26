#ifndef _PERMUTATION_H
#define _PERMUTATION_H

#include "stats_module.h"

typedef struct {
  // Begin donchange (these must match combination.h)
  unsigned int size;
  unsigned int pick;
  unsigned int *data; // if we are picking, combo info goes here
  // End dontchange
  BASETYPE_L values;
  unsigned int *p_data; // data being permuted
  unsigned int count; // how many have we stepped through?
  unsigned int end; // when count == end, we are done
  unsigned int orig_count; // used for slices
  unsigned int orig_end; // used for slices
  unsigned int *refcount; // our ref count (used for slices)
  unsigned char one_more; // because of the algo, we need a flag for last call!
} permute_head;

/* prototypes */
permute_head *permute_new(unsigned int list_size, unsigned int pick, BASETYPE_L list);
void permute_free(permute_head *ph);
unsigned int permute_length(permute_head *ph);
permute_head *permute_clone(permute_head *ph);
int permute_set_slice(permute_head *ph, unsigned int start, unsigned int finish);
int permute_smart_item(permute_head *ph, BASETYPE_L ret_list, unsigned int place);
void permute_dump(permute_head *ph); // DEBUG
#endif /* ifndef _PERMUTATION_H */
