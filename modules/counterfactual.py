"""Score-preserving counterfactual skill analysis."""
from advanced import simulate

def rank_actions(report):
    actions = []
    for skill in report["missing"]:
        _, gain = simulate(report, [skill])
        actions.append({"skill": skill, "score_gain_points": gain})
    return sorted(actions, key=lambda x: (-x["score_gain_points"], x["skill"]))
