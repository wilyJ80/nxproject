import pytest
import networkx as nx
from main3 import verify_sequence

@pytest.fixture
def undirected_graph():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D")])
    return G

@pytest.fixture
def directed_graph():
    D = nx.DiGraph()
    D.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D")])
    return D

def test_walk_undirected(undirected_graph):
    res = verify_sequence(undirected_graph, ["A", "B", "C"])
    assert res["is_walk"] is True
    
    res = verify_sequence(undirected_graph, ["A", "C"])
    assert res["is_walk"] is False

def test_path_undirected(undirected_graph):
    res = verify_sequence(undirected_graph, ["A", "B", "C", "D"])
    assert res["is_path"] is True
    
    res = verify_sequence(undirected_graph, ["A", "B", "C", "B", "D"])
    assert res["is_path"] is False

def test_trail_undirected(undirected_graph):
    res = verify_sequence(undirected_graph, ["A", "B", "C"])
    assert res["is_trail"] is True
    
    res = verify_sequence(undirected_graph, ["A", "B", "A"])
    assert res["is_trail"] is False
    
    res = verify_sequence(undirected_graph, ["A", "B", "D", "C", "B"])
    assert res["is_trail"] is True
    assert res["is_path"] is False

def test_circuit_undirected(undirected_graph):
    res = verify_sequence(undirected_graph, ["A", "B", "D", "A"])
    assert res["is_circuit"] is True
    assert res["is_trail"] is True
    assert res["is_path"] is False 
    
    res = verify_sequence(undirected_graph, ["A", "B", "D"])
    assert res["is_circuit"] is False

def test_trail_directed(directed_graph):
    directed_graph.add_edge("B", "A")
    
    res = verify_sequence(directed_graph, ["A", "B", "A"])
    assert res["is_trail"] is True
    assert res["is_walk"] is True
    
    res = verify_sequence(directed_graph, ["A", "B", "A", "B"])
    assert res["is_trail"] is False

def test_single_vertex(undirected_graph):
    res = verify_sequence(undirected_graph, ["A"])
    assert res["is_walk"] is True
    assert res["is_path"] is True
    assert res["is_trail"] is True
    assert res["is_circuit"] is False

def test_empty_sequence(undirected_graph):
    res = verify_sequence(undirected_graph, [])
    assert res["is_walk"] is False

def test_non_existent_vertex(undirected_graph):
    res = verify_sequence(undirected_graph, ["A", "Z"])
    assert res["is_walk"] is False
