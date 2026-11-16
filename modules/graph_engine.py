"""Curated learning relationships, not universal prerequisites."""
import networkx as nx
from advanced import dependencies

def competency_graph(missing_skills):
    graph = nx.DiGraph()
    graph.add_nodes_from(missing_skills)
    graph.add_edges_from(dependencies(missing_skills))
    return graph
