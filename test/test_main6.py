import pytest
import networkx as nx
import os
from main6 import kruskal_algorithm, DisjointSet, visualize_kruskal
from main import GraphService

def test_disjoint_set():
    nodes = ["A", "B", "C", "D"]
    ds = DisjointSet(nodes)
    
    assert ds.find("A") == "A"
    assert ds.find("B") == "B"
    
    assert ds.union("A", "B") is True
    assert ds.find("A") == ds.find("B")
    
    assert ds.union("A", "B") is False
    
    ds.union("C", "D")
    assert ds.find("C") == ds.find("D")
    assert ds.find("A") != ds.find("C")
    
    ds.union("B", "C")
    assert ds.find("A") == ds.find("D")

def test_kruskal_simple():
    G = nx.Graph()
    G.add_edge("A", "B", weight=4)
    G.add_edge("A", "C", weight=3)
    G.add_edge("B", "C", weight=2)
    G.add_edge("B", "D", weight=5)
    G.add_edge("C", "D", weight=7)
    
    mst_edges, total_weight = kruskal_algorithm(G)
    
    # NetworkX validation
    nx_mst = nx.minimum_spanning_edges(G, algorithm='kruskal', data=True)
    nx_weight = sum(d['weight'] for u, v, d in nx_mst)
    
    assert total_weight == nx_weight
    assert len(mst_edges) == len(G.nodes()) - 1

def test_kruskal_disconnected():
    G = nx.Graph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("C", "D", weight=1)
    
    mst_edges, total_weight = kruskal_algorithm(G)
    assert total_weight == 2
    assert len(mst_edges) == 2

def test_kruskal_real_file():
    service = GraphService()
    test_file = "test/kruskal_test_input.txt"
    
    assert os.path.exists(test_file)
    
    graph = service.load_from_file(test_file)
    if service.is_directed:
        graph = graph.to_undirected()
        
    mst_edges, total_weight = kruskal_algorithm(graph)
    
    # NetworkX validation
    nx_mst = nx.minimum_spanning_edges(graph, algorithm='kruskal', data=True)
    nx_weight = sum(d['weight'] for u, v, d in nx_mst)
    
    assert total_weight == nx_weight
    
    # Test visualization
    output_img = "test/output/test_mst.png"
    visualize_kruskal(graph, mst_edges, output_img)
    assert os.path.exists(output_img)
    assert os.path.exists("test/output/.gitignore")

def test_compare_with_networkx_random():
    import random
    for _ in range(5):
        n = 15
        m = 30
        G = nx.gnm_random_graph(n, m)
        for (u, v) in G.edges():
            G.edges[u,v]['weight'] = random.randint(1, 100)
            
        mst_edges, total_weight = kruskal_algorithm(G)
        
        nx_mst = nx.minimum_spanning_edges(G, algorithm='kruskal', data=True)
        nx_weight = sum(d['weight'] for u, v, d in nx_mst)
        
        assert abs(total_weight - nx_weight) < 1e-9
