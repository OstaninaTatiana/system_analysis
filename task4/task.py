import json
from typing import List, Dict

def interpolate(x: float, points: List[List[float]]) -> float:
    if not points:
        return 0.0
    pts = sorted(points, key=lambda p: p[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    if x <= xs[0] or x >= xs[-1]:
        return 0.0

    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        y0, y1 = ys[i], ys[i + 1]
        if x0 <= x <= x1:
            if x0 == x1:
                return max(y0, y1)
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return 0.0


def get_output_range(heat_mfs: Dict[str, List[List[float]]]) -> tuple:
    all_x = [p[0] for pts in heat_mfs.values() for p in pts]
    return min(all_x), max(all_x)


def main(
        temp_mf_json: str,
        heat_mf_json: str,
        rules_json: str,
        temperature: float
    ) -> float:
    temp_data = json.loads(temp_mf_json)
    heat_data = json.loads(heat_mf_json)
    rules = json.loads(rules_json)

    temp_mfs = {term["id"]: term["points"] for term in temp_data["температура"]}
    heat_mfs = {term["id"]: term["points"] for term in heat_data["температура"]}

    input_mu = {}
    for term, pts in temp_mfs.items():
        input_mu[term] = interpolate(temperature, pts)

    out_min, out_max = get_output_range(heat_mfs)
    if out_min == out_max:
        return float(out_min)

    n_steps = 1000
    dx = (out_max - out_min) / n_steps

    max_mu = 0.0
    first_max_s = None
    eps = 1e-9

    for i in range(n_steps + 1):
        s = out_min + i * dx
        mu_s = 0.0

        for in_term, out_term in rules:
            if in_term not in input_mu or out_term not in heat_mfs:
                continue
            alpha = input_mu[in_term]
            if alpha <= 0:
                continue
            mu_out = interpolate(s, heat_mfs[out_term])
            activated = min(alpha, mu_out)
            if activated > mu_s:
                mu_s = activated

        if mu_s > max_mu + eps:
            max_mu = mu_s
            first_max_s = s
        elif abs(mu_s - max_mu) <= eps and first_max_s is None:
            first_max_s = s

    return first_max_s

