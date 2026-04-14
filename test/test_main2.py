import pytest
import networkx as nx
import os

from main import GraphService
from main2 import modified_dfs_all_paths

def test_modified_dfs_undirected_simple():
    service = GraphService()
    service.graph = nx.Graph()
    service.graph.add_edges_from([("A", "B"), ("B", "C"), ("A", "C")])
    
    count = modified_dfs_all_paths(service.graph, "A", "C", 1)
    assert count == 1
    
    count = modified_dfs_all_paths(service.graph, "A", "C", 2)
    assert count == 2
    
def test_compare_with_networkx_undirected():
    service = GraphService()
    service.load_from_file("grafo01.txt")
    
    u, v = "A", "C"
    k = 3
    
    count_manual = modified_dfs_all_paths(service.graph, u, v, k)
    
    nx_paths = list(nx.all_simple_paths(service.graph, u, v, cutoff=k))
    
    assert count_manual == len(nx_paths)

def test_compare_with_networkx_directed():
    service = GraphService()
    service.load_from_file("digrafo01.txt")
    
    u, v = "A", "D"
    k = 3
    
    count_manual = modified_dfs_all_paths(service.graph, u, v, k)
    
    nx_paths = list(nx.all_simple_paths(service.graph, u, v, cutoff=k))
    
    assert count_manual == len(nx_paths)

def test_no_path():
    service = GraphService()
    service.graph = nx.DiGraph()
    service.graph.add_edge("A", "B")
    service.graph.add_node("C")
    
    count = modified_dfs_all_paths(service.graph, "A", "C", 10)
    assert count == 0

def test_path_longer_than_k():
    service = GraphService()
    service.graph = nx.DiGraph()
    service.graph.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
    
    count = modified_dfs_all_paths(service.graph, "A", "D", 2)
    assert count == 0
    
    count = modified_dfs_all_paths(service.graph, "A", "D", 3)
    assert count == 1

def test_u_equals_v():
    service = GraphService()
    service.graph = nx.Graph()
    service.graph.add_node("A")
    
    count = modified_dfs_all_paths(service.graph, "A", "A", 0)
    assert count == 1
    
    count = modified_dfs_all_paths(service.graph, "A", "A", 1)
    assert count == 1
