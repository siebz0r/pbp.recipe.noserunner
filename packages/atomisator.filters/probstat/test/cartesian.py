import probstat

arg1 = range(1,4)
arg2 = ['A', 'B']
arg3 = ['!', '@', '#']

should_be = [[1, 'A', '!'],[2, 'A', '!'],[3, 'A', '!'],[1, 'B', '!'],[2, 'B', '!'],
             [3, 'B', '!'],[1, 'A', '@'],[2, 'A', '@'],[3, 'A', '@'],[1, 'B', '@'],
             [2, 'B', '@'],[3, 'B', '@'],[1, 'A', '#'],[2, 'A', '#'],[3, 'A', '#'],
             [1, 'B', '#'],[2, 'B', '#'],[3, 'B', '#']]

c = probstat.Cartesian([arg1, arg2, arg3])

cp = []
for (i) in c:
  cp.append(i)

if (cp != should_be):
  raise Exception('cartesian didnt return expected result')

slice = c[3:8]
slice_cp = []
for (i) in slice:
  slice_cp.append(i)

if (slice_cp != cp[3:8]):
  raise Exception('slice output doesnt match expected')

if (len(slice_cp) != len(slice)):
  raise Exception('slice returns bad length')

if (len(slice) != len(cp[3:8])):
  raise Exception('slice len returns bad length')


if (cp[0] != c[0]):
  raise Exception('first elements dont match')

if (cp[-1] != c[-1]):
  raise Exception('last elements dont match')

if (c[-1] != c[-1]):
  raise Exception('last element doesnt match self')

if (slice[0] != slice_cp[0]):
  raise Exception('first slice element doesnt match')

if (slice[-1] != slice_cp[-1]):
  raise Exception('last slice element doesnt match')
