#ifndef _CARTESIAN_H
#define _CARTESIAN_H
#include "stats_module.h"

typedef struct cartesian_head_ {
  BASETYPE_LL values;
  unsigned int size; // width of values
  long long total; // this could be really big
  long long count; // our current place
  long long orig_total; // used in slice, len
  long long orig_count; // used in slice, len
  unsigned int *div; // 'size' list of divs
  unsigned int *mod; // 'size' list of mods
  unsigned int *refcount; // used in slices
} cartesian_head;

cartesian_head *cartesian_new(unsigned int size, BASETYPE_LL list, unsigned int *sizes);
void cartesian_free(cartesian_head *ch);
int cartesian_smart_item(cartesian_head *ch, BASETYPE_L ret_list, long long item_num);
cartesian_head *cartesian_clone(cartesian_head *ch);
int cartesian_set_slice(cartesian_head *ch, long long start, long long finish);
long long cartesian_get_length(cartesian_head *ch);

#endif /* ifndef _CARTESIAN_H */
