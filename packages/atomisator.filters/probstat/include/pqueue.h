#ifndef _PQUEUE_H
#define _PQUEUE_H
#include "stats_module.h"
/*
 *  Priority queue structure
 */

typedef struct {
  int priority;
  BASETYPE data;
} node;

typedef struct {
	int size, avail, step;
	node **d;
} pqueue;


pqueue *pqinit(pqueue *q, int n);
void pqdump(pqueue *q);
int pqinsert(pqueue *q, node *newnode);
node *pqremove(pqueue *q);
node *pqpeek(pqueue *q);

#endif /* _PQUEUE_H */
