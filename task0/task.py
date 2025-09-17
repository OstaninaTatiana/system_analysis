def main(csv_string):
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

    if max_vertex == 0:
        return []

    n = max_vertex
    matrix = [[0] * n for i in range(n)]

    for u, v in edges:
        matrix[u-1][v-1] = 1
        matrix[v-1][u-1] = 1

    return matrix
