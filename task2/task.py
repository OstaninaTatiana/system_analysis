import csv
from io import StringIO
from typing import Tuple
import math
from collections import defaultdict, deque

def task(s: str, e: str) -> Tuple[float, float]:
    f = StringIO(s)
    reader = csv.reader(f)
    edges = [(row[0], row[1]) for row in reader]

    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    n = len(nodes)

    r1 = set()
    for u, v in edges:
        r1.add((u, v))

    r2 = {(v, u) for (u, v) in r1}

    graph = defaultdict(list)
    for u, v in r1:
        graph[u].append(v)

    r3 = set()
    for start in nodes:
        visited = set()
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            for nxt in graph[cur]:
                if nxt not in visited and nxt != start:
                    visited.add(nxt)
                    r3.add((start, nxt))
                    queue.append(nxt)

    r4 = {(v, u) for (u, v) in r3}

    parent = {}
    for u, v in r1:
        parent[v] = u

    r5 = set()
    child_of = defaultdict(list)
    for child, par in parent.items():
        child_of[par].append(child)

    for par, kids in child_of.items():
        for i in range(len(kids)):
            for j in range(len(kids)):
                if i != j:
                    r5.add((kids[i], kids[j]))

    relations = [r1, r2, r3, r4, r5]
    k = len(relations)

    max_out = n - 1
    H = 0.0

    for node in nodes:
        for rel in relations:
            l = sum(1 for (u, v) in rel if u == node)
            if max_out == 0:
                p = 0.0
            else:
                p = l / max_out
            if p > 0:
                entropy = -p * math.log2(p)
                H += entropy

    c = 1 / (math.e * math.log(2))
    href = c * n * k
    H_n = H / href

    return round(H, 1), round(H_n, 1)



# print(task('1,2\n1,3\n3,4\n3,5', str(1)))
