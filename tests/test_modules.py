from modules.parser import mask_pii, extract_sections
from modules.counterfactual import rank_actions
from modules.graph_engine import competency_graph
from engine import analyze

def test_privacy():
    assert "[EMAIL]" in mask_pii("Email me at student@example.com")

def test_sections():
    assert extract_sections("Skills\nPython\nProjects\nDemo")['Skills']

def test_counterfactual_ranking():
    report = analyze("Skills\nPython", "Python Docker Git")
    assert len(rank_actions(report)) == 2

def test_graph_direction():
    assert ("Linux", "Docker") in competency_graph(["Docker"]).edges
