import json
from itertools import combinations

def ranks(arr):
    r = {}
    for i, g in enumerate(arr):
        for x in g:
            r[x] = i
    return r

def main(s1, s2):
    r1 = ranks(json.loads(s1))
    r2 = ranks(json.loads(s2))
    res = []
    for x, y in combinations(r1.keys(), 2):
        if (r1[x] < r1[y] and r2[x] > r2[y]) or (r1[x] > r1[y] and r2[x] < r2[y]):
            res.append((x, y))
    return res
