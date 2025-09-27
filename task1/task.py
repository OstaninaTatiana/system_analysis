def f0(edges, max_vertex):
    if max_vertex == 0:
        return []

    n = max_vertex
    matrix = [[0] * n for i in range(n)]

    for u, v in edges:
        matrix[u-1][v-1] = 1
        matrix[v-1][u-1] = 1

    return matrix

def f1(edges, max_vertex):

    if max_vertex == 0:
        return []

    n = max_vertex
    matrix = [[0] * n for i in range(n)]

    for u, v in edges:
        matrix[u-1][v-1] = 1

    return matrix

def f2(edges, max_vertex):

    if max_vertex == 0:
        return []

    n = max_vertex
    matrix = [[0] * n for i in range(n)]

    for u, v in edges:
        matrix[v-1][u-1] = 1

    return matrix

def f3(edges, n):

    direct = f1(edges, n)

    reach = [row[:] for row in direct]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = 1

    indirect = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if reach[i][j] and not direct[i][j]:
                indirect[i][j] = 1

    return indirect

def f4(edges, n):

    direct = f2(edges, n)

    reach = [row[:] for row in direct]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = 1

    indirect = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if reach[i][j] and not direct[i][j]:
                indirect[i][j] = 1

    return indirect

def f5(edges, n):
    s = {}
    for a, b in edges:
        if a not in s:
            s[a] = []
        s[a].append(b)

    colleagues = [[0] * n for _ in range(n)]

    for n, p in s.items():
        k = len(p)
        for i in range(k):
            for j in range(i + 1, k):
                x = p[i] - 1
                y = p[j] - 1
                colleagues[p[i] - 1][p[j] - 1] = 1
                colleagues[p[j] - 1][p[i] - 1] = 1

    return colleagues

def main(csv_string, er):
    if not csv_string.strip():
        return []

    edges = []
    max_vertex = 0

    lines = csv_string.strip().split('\n')
    for line in lines:
        parts = line.split(',')
        u = int(parts[0].strip())
        v = int(parts[1].strip())
        edges.append((u, v))
        max_vertex = max(max_vertex, u, v)

    return (f0(edges, max_vertex),
            f1(edges, max_vertex),
            f2(edges, max_vertex),
            f3(edges, max_vertex),
            f4(edges, max_vertex),
            f5(edges, max_vertex))

