def rank_matches(user, others):
    scored = [(other, _compatibility(user, other)) for other in others]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def _compatibility(a, b):
    score = 0

    sleep_order = {"early": 0, "normal": 1, "late": 2}
    if a.sleep_schedule and b.sleep_schedule:
        diff = abs(sleep_order.get(a.sleep_schedule, 1) - sleep_order.get(b.sleep_schedule, 1))
        score += (2 - diff) * 3

    if a.cleanliness and b.cleanliness:
        score += max(0, 4 - abs(a.cleanliness - b.cleanliness)) * 2

    if a.noise_tolerance and b.noise_tolerance:
        score += max(0, 4 - abs(a.noise_tolerance - b.noise_tolerance)) * 2

    if a.guests_ok == b.guests_ok:
        score += 5
    if a.smoking_ok == b.smoking_ok:
        score += 5

    if a.neighborhood and b.neighborhood and a.neighborhood == b.neighborhood:
        score += 4

    if a.budget_min and a.budget_max and b.budget_min and b.budget_max:
        overlap = min(a.budget_max, b.budget_max) - max(a.budget_min, b.budget_min)
        if overlap > 0:
            score += 4

    return score


def max_possible_score():
    return (2 * 3) + (4 * 2) + (4 * 2) + 5 + 5 + 4 + 4


def pct(score):
    return round(score / max_possible_score() * 100)
