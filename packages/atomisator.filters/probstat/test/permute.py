import probstat

# FIRST
# try straight permutations (all the ways to write a list)

c = probstat.Permutation(range(1,4))
should_be = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

cp = []
for (i) in c:
  cp.append(i)

if (should_be != cp):
  raise 'Output isnt what it should be'

if (len(cp) != len(c)):
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

if (c[-1] != cp[-1]):
  raise 'last elements not equal'

if (c[-1] != cp[-1]):
  raise 'last elements not equal'

if (c[0] != cp[0]):
  raise 'first elements not equal'

if (c[0] != cp[0]):
  raise 'first elements not equal'

# SECOND
# try 5 pick 3

c = probstat.Permutation(range(1,5),3)
should_be = [[1, 2, 3],[1, 3, 2],[2, 1, 3],[2, 3, 1],[3, 1, 2],[3, 2, 1],
             [1, 2, 4],[1, 4, 2],[2, 1, 4],[2, 4, 1],[4, 1, 2],[4, 2, 1],
             [1, 3, 4],[1, 4, 3],[3, 1, 4],[3, 4, 1],[4, 1, 3],[4, 3, 1],
             [2, 3, 4],[2, 4, 3],[3, 2, 4],[3, 4, 2],[4, 2, 3],[4, 3, 2]]

cp = []
for (i) in c:
  cp.append(i)

if (should_be != cp):
  raise 'Output isnt what it should be'

if (len(cp) != len(c)):
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

if (slice_cp[-1] != slice_list[-1]):
  raise 'last elements not equal'

if (slice_cp[-1] != slice_list[-1]):
  raise 'last elements not equal'

if (slice_cp[0] != slice_list[0]):
  raise 'first elements not equal'

if (slice_cp[0] != slice_list[0]):
  raise 'first elements not equal'

p = probstat.Permutation(range(3,12))
dummy = p[1234:-1] # shouldn't affect anything
plen = len(p)

for (i) in p:
  plen -= 1

if (plen < 0):
  raise 'Permutation overran'

sl = p[1234:12345]
plen = len(sl)

for (i) in sl:
  plen -= 1

if (plen != 0):
  print 'plen is %d, should be 0' % (plen)
  raise 'Permutation over/under run'

if (len(probstat.Permutation(range(150), 2)) != 22350):
  raise 'Permutation len not in cache table calculated WRONG'
