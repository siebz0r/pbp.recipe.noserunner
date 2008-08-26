#include <stdio.h>
#include <stdlib.h>
#undef NDEBUG
#include <assert.h>
#include "combination.h"
#include "size_lookup_combo.h"

/* parts of this code from http://sources.redhat.com/gsl/, which is in turn
   probably from somewhere else (public domain?) */

combo_head *combination_new(unsigned int size, BASETYPE_L list, unsigned int pick) {
  combo_head *ch;
  unsigned int i, tot;

  ch = (combo_head *) malloc(sizeof(combo_head));
  ch->values = (BASETYPE_L) malloc(size * sizeof(BASETYPE));

  for (i = 0; i < size; i++) {
    ch->values[i] = list[i];
  }
  ch->pick = pick;
  ch->size = size;

  ch->data = (unsigned int *) malloc(pick * sizeof(unsigned int));
  combination_init_data(ch); // reset ->data

  ch->refcount = (unsigned int *) malloc(sizeof(unsigned int));
  *ch->refcount = 1;

  ch->count = 0;
  ch->orig_count = 0;

  // calculate n!/(k! * (n-k)!)
  tot = combination_calculate_NK(ch->size, ch->pick);
  ch->end = tot;
  ch->orig_end = tot;

  return ch;
}

combo_head *combination_clone(combo_head *oldp) {
  combo_head *newp;

  newp = (combo_head *) malloc(sizeof(combo_head));
  newp->values = oldp->values;
  newp->pick = oldp->pick;
  newp->size = oldp->size;
  newp->count = oldp->count;
  newp->orig_count = oldp->orig_count;
  newp->end = oldp->end;
  newp->orig_end = oldp->orig_end;

  newp->data = (unsigned int *) malloc(newp->pick * sizeof(unsigned int));
  combination_init_data(newp); // reset ->data

  newp->refcount = oldp->refcount;
  *newp->refcount = *newp->refcount + 1;

  return newp;
}
  

void combination_free(combo_head *ch) {
  assert(*ch->refcount > 0);

  *ch->refcount = *ch->refcount - 1;
  if (*ch->refcount == 0) {
    free(ch->values);
    ch->values = NULL;
    free(ch->refcount);
    ch->refcount = NULL;
  }
  free(ch->data);
  ch->data = NULL;
  free(ch);
  return;
}

static
void combination_cp_current(combo_head *ch, BASETYPE_L ret_list) {
    unsigned int i;
    for (i = 0; i < ch->pick; i++) { // or ch->stack_size, should be identical
      ret_list[i] = ch->values[ch->data[i]];
    }
}

int combination_inc(combo_head *ch) {
  unsigned int size = ch->size;
  unsigned int pick = ch->pick;
  unsigned int *data = ch->data;
  unsigned int i;

  i = pick - 1;

  while(i > 0 && data[i] == size - pick + i) {
    i--;
  }

  // this is just for safety in case a caller calls too many times
  // NB, also used by permute_base.c!
  if(i == 0 && data[i] == size - pick) {
    return 0;
  }

  data[i]++;

  for(; i < pick - 1; i++) {
    data[i + 1] = data[i] + 1;
  }

  return ch->pick;
}
/* The algo for this is a bit complicated: for a 7, pick 5 example
   with the data being A,B,C,D,E,F,G
   here is a matrix of the standard order, the 4th column is just
   calculated by looking at whats left over
   '15 A' means A is repeated 15 times in that position
   '6P4' means that 15 == the number of possibilities in 6P4
   '!' means just one possibility 1P1
   0      1      2      3      4
   15 A   10 B   6 C    3 D    {E,F,G}
   6P4    5P3    4P2    3P1    

                        2 E    {F,G}
                        2P1
			
			1 F    {G}
			1P1
   
		 3 D    2 E    {F,G}
		 3P2    2P1

		        1 F    {G}
			1P1

		 1 E    1 F    {G}
		 2P2    1P1
   5 B
   5P4   and so on

   As you travel to the right, subtract from both n and k (in nPk)
   if you have to move down, subtract more from k
   for the last column, just iterate over the few members

*/
void combination_set_count(combo_head *ch, unsigned int place) {
  unsigned int n, k, p;
  unsigned int parent_n, parent_k;
  unsigned int j;
  unsigned int level_max;
  unsigned int curr;
  p = place;
  n = ch->size;
  k = ch->pick;
  ch->data[0] = 0;

  j = 0; // moves left to right
  parent_n = n - 1;
  parent_k = k - 1;
  curr = 0;
  while (j < k) {
    level_max = combination_calculate_NK(parent_n, parent_k);
    ch->data[j] = curr++;
    if (p >= level_max) {
      p -= level_max;
      level_max = combination_calculate_NK(parent_n, parent_k);
      parent_n--;
    } else {
      parent_n--;
      parent_k--;
      j++;
    }
  }
  /* 
    We don't do this here because permutation fakes like a combo,
    and it would overwrite its data!
    ch->count = place;
  */
  return;
}

void combination_init_data(combo_head *ch) { // reset ->data to intial state
  unsigned int i;
  for (i = 0; i < ch->pick; i++) {
    ch->data[i] = i;
  }
  return;
}

int combination_length(combo_head *ch) {
  return (ch->orig_end - ch->orig_count);
}

int combination_smart_item(combo_head *ch, BASETYPE_L ret_list, unsigned int pos) {
  pos += ch->orig_count; // make relative pos absolute
   // check bounds
  if (pos >= ch->orig_end) {
    return 0;
  }
 
  if (pos == ch->count) { // same as current
    // do nothing
  } else if (pos == (ch->count + 1)) { // increment
    combination_inc(ch);
    ch->count++;
  } else { // set to arbitrary
    combination_set_count(ch, pos + ch->orig_count);
  }
  combination_cp_current(ch, ret_list);
  return ch->pick;
}

int combination_set_slice(combo_head *ch, unsigned int start, unsigned int finish) {
  unsigned int new_start, new_finish;

  new_start = ch->orig_count + start;
  new_finish = ch->orig_count + finish;
  if (ch->end < new_start || start < 0 ||
      (ch->end+1) < new_finish || finish < 0) {
    return -1;
  }
  ch->count = new_start;
  ch->orig_count = new_start;
  ch->end = new_finish;
  ch->orig_end = new_finish;

  combination_set_count(ch, new_start);
  ch->count = new_start;
  return 1;
}


unsigned int combination_calculate_NK(unsigned int n, unsigned int k) {
  unsigned long long tot;
  
  assert(n >= k);
  // check pre-cacled sizes
  tot = GET_COMBO_SIZE(n,k);
  if (!tot) { // not in our quick-lookup table, try calcing by hand
    int amult = n;
    int amult_stop = k;
    int adiv = n - k;
    int tdiv = 1;
    tot = 1;
    if (n - k > k) { // reverse the order if it means less iterations through the loop
      amult = n;
      amult_stop = n - k;
      adiv = k;
    }
    for (; amult > amult_stop; amult--) {
      tot *= amult;
      if (adiv > 0) {
	tdiv *= adiv;
	adiv--;
      }
      // find and divide by the GCD to keep the tot from overflowing
      if (tdiv > 1) { 
	int d;
	int r;

	if (adiv > tot) {
	  d = tdiv;
	  r = tot;
	} else {
	  d = tot;
	  r = tdiv;
	}
    
	while( r != 0 ){ 
	  d = r;
	  r = tot % r;
	}
	// divide both by the greatest common denominator
	tot /= d;
	tdiv /= d;
      }
    }
  }
  return (unsigned int)tot;
}

void combo_dump(combo_head *ch) {
  unsigned int i;

  printf("size %d, pick %d, count %d\n", ch->size, ch->pick, ch->count);
  if (ch->data) {
    for (i = 0; i < ch->pick; i++) {
      printf("%d  ", ch->data[i]);
    }
    printf("\n");
  }
}
