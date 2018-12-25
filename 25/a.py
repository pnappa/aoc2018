

# well this one is just connected components.
# i'll use sets because i'm lazy


coords = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        coords.append(tuple(map(int, line.strip().split(','))))


# find union datastructure
class UnionFind:
    """Weighted quick-union with path compression.
    The original Java implementation is introduced at
    https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
    >>> uf = UnionFind(10)
    >>> for (p, q) in [(3, 4), (4, 9), (8, 0), (2, 3), (5, 6), (5, 9),
    ...                (7, 3), (4, 8), (6, 1)]:
    ...     uf.union(p, q)
    >>> uf._id
    [8, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    >>> uf.find(0, 1)
    True
    >>> uf._id
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    """

    def __init__(self, n):
        self._id = list(range(n))
        self._sz = [1] * n

    def _root(self, i):
        j = i
        while (j != self._id[j]):
            self._id[j] = self._id[self._id[j]]
            j = self._id[j]
        return j

    def find(self, p):
        return self._root(p)
    
    def union(self, p, q):
        i = self._root(p)
        j = self._root(q)
        if i == j:
            return
        if (self._sz[i] < self._sz[j]):
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i
            self._sz[i] += self._sz[j]

def within(ax,ay,az,aw, bx,by,bz,bw):
    return (abs(ax-bx)+abs(ay-by)+abs(az-bz)+abs(aw-bw)) <= 3

djset = UnionFind(len(coords))

# a(n) . n^2 baby
for index, pos in enumerate(coords):
    for oindex, opos in enumerate(coords):
        if within(*opos, *pos):
            djset.union(index, oindex)

reps = set()
for i in range(len(coords)):
    reps.add(djset.find(i))

print(len(reps))
