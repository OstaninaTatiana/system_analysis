import json


def flat(r):
    res = []
    for x in r:
        if isinstance(x, list):
            res.extend(x)
        else:
            res.append(x)
    return res


def build_rel_mat(ranking, objs):
    idx = {o: i for i, o in enumerate(objs)}
    n = len(objs)
    M = [[0] * n for _ in range(n)]

    clusters = []
    for item in ranking:
        if isinstance(item, list):
            clusters.append(item)
        else:
            clusters.append([item])

    for i, c1 in enumerate(clusters):
        for j, c2 in enumerate(clusters):
            if i <= j:
                for a in c1:
                    for b in c2:
                        M[idx[a]][idx[b]] = 1

    return warshall(M)


def mat_or(X, Y):
    n = len(X)
    return [[X[i][j] | Y[i][j] for j in range(n)] for i in range(n)]


def transpose(M):
    return [list(row) for row in zip(*M)]


def warshall(M):
    n = len(M)
    R = [row[:] for row in M]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return R


def main(a: str, b: str) -> str:
    A = json.loads(a)
    B = json.loads(b)

    all_objs = sorted(set(flat(A) + flat(B)))
    n = len(all_objs)
    obj_to_idx = {o: i for i, o in enumerate(all_objs)}

    YA = build_rel_mat(A, all_objs)
    YB = build_rel_mat(B, all_objs)

    C = [[YA[i][j] & YB[i][j] for j in range(n)] for i in range(n)]

    E = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                E[i][j] = 1
            else:
                agree_i_le_j = YA[i][j] and YB[i][j]
                agree_j_le_i = YA[j][i] and YB[j][i]

                if agree_i_le_j and agree_j_le_i:
                    E[i][j] = 1
                elif not (agree_i_le_j or agree_j_le_i):
                    E[i][j] = 1

    E_star = warshall(E)

    visited = [False] * n
    clusters = []
    for i in range(n):
        if not visited[i]:
            stack = [i]
            comp = []
            visited[i] = True
            while stack:
                u = stack.pop()
                comp.append(all_objs[u])
                for v in range(n):
                    if not visited[v] and E_star[u][v]:
                        visited[v] = True
                        stack.append(v)
            clusters.append(sorted(comp))
    clusters.sort(key=min)

    m = len(clusters)
    changed = True
    while changed:
        changed = False
        for i in range(m):
            for j in range(i + 1, m):
                X, Y = clusters[i], clusters[j]
                x_le_y = all(C[obj_to_idx[x]][obj_to_idx[y]] for x in X for y in Y)
                y_le_x = all(C[obj_to_idx[y]][obj_to_idx[x]] for y in Y for x in X)
                if y_le_x and not x_le_y:
                    clusters[i], clusters[j] = clusters[j], clusters[i]
                    changed = True

    out = []
    for c in clusters:
        if len(c) == 1:
            out.append(c[0])
        else:
            out.append(c)

    return json.dumps(out, ensure_ascii=False)
