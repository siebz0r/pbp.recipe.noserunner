import probstat

c = probstat.Combination(range(1,5),3)
should_be = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]

cp = []
for (i) in c:
  cp.append(i)

if (should_be != cp):
  raise 'Output isnt what it should be'

if (len(cp) != len(c)):
  print len(cp), len(c)
  raise 'Len of output does not match len of object'

slice_cp = cp[0:1]
slice = c[0:1]

slice_list = []
for (i) in slice:
  slice_list.append(i)
if (slice_list != slice_cp):
  raise "slice doesn't equal real output"

if (len(slice) != len(slice_cp)):
  raise 'len of slice doesnt match len of real slice'

if (c[0] != cp[0] or c[-1] != c[-1]):
  raise 'first or last elements not equal'

if (c[0] != cp[0] or c[-1] != c[-1]):
  raise 'first or last elements not equal'

c = probstat.Combination(range(3,15),6)
plen = len(c)
for (i) in c:
  plen -= 1

if (plen != 0):
  raise 'len not equal to actually count'

sl = c[120:450]

plen = len(sl)
for (i) in sl:
  plen -= 1

if (plen != 0):
  print 'len over/under ran by %d' % (plen)
  raise 'slice len not equal to actual count'

c = probstat.Combination(range(100),2)
if len(c) != 4950:
  print 'Failed test for longish initial length'
  raise 'Wrong seq length for Combination(100,2)'
