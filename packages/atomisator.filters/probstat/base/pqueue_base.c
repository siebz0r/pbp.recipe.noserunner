#include <stdio.h>
#include "pqueue.h"

/* This source was adapted from a Priority Queue implementaiton
   in the public domain */

pqueue *
pqinit(pqueue *q, int n)
{
  if (!q) {
    return NULL;
  }
  if (!(q->d = (node **)malloc(sizeof(node *) * n))) {
    return NULL;
  }
  q->avail = q->step = n;
  q->size = 1;
  return q;
}

void
pqdump(pqueue *q)
{
  printf("size %d, avail %d, step %d\n", q->size, q->avail, q->step);
}

int
pqinsert(pqueue *q, node *newnode)
{
  node **tmp;
  int i, newsize;

  if (!q)
    return 0;
	
  /* allocate more memory if necessary */
  if (q->size >= q->avail) {
    newsize = q->size + q->step;
    if (!(tmp = realloc(q->d, sizeof(node *) * newsize))) {
      return 0;
    }
    q->d = tmp;
    q->avail = newsize;		
  }

  /* insert item */
  i = q->size++; // new size
  while (i > 1 && q->d[i / 2]->priority < newnode->priority) {
    // while middle < priority
    q->d[i] = q->d[i / 2];
    // set new end = middle
    i /= 2;
  }
  q->d[i] = newnode;
  return 1;	
} 

node *
pqremove(pqueue *q)
{	
  node *tmp;
  node *removed;
  int i = 1, j;
  
  if (!q || q->size == 1) return NULL;
  removed = q->d[1]; // first node

  // now reorder the other nodes
  tmp = q->d[--q->size];
  while (i <= q->size / 2) {
    j = 2 * i;
    if (j < q->size && 
	q->d[j]->priority < q->d[j + 1]->priority) {
      j++;
    }
    if (q->d[j]->priority <= tmp->priority) {
      break;
    }
    q->d[i] = q->d[j];
    i = j;
  }
  q->d[i] = tmp;

  return removed;	
} 

node *
pqpeek(pqueue *q)
{
  node *peek;
  if (!q || q->size == 1)
    return NULL;
  peek = q->d[1];
  return peek;
}
