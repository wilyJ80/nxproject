import pytest
import networkx as nx
from main5 import dijkstra, bellman_ford

def test_dijkstra_simple():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=4)
    G.add_edge("A", "C", weight=2)
    G.add_edge("B", "C", weight=1)
    G.add_edge("B", "D", weight=5)
    G.add_edge("C", "D", weight=8)
    G.add_edge("C", "E", weight=10)
    G.add_edge("D", "E", weight=2)
    G.add_edge("E", "F", weight=3)
    
    path, cost = dijkstra(G, "A", "F")
    
    # NetworkX validation
    nx_cost, nx_path = nx.single_source_dijkstra(G, "A", target="F")
    
    assert path == nx_path
    assert cost == nx_cost

def test_dijkstra_undirected():
    G = nx.Graph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("B", "C", weight=2)
    G.add_edge("A", "C", weight=4)
    
    path, cost = dijkstra(G, "A", "C")
    assert path == ["A", "B", "C"]
    assert cost == 3

def test_dijkstra_no_path():
    G = nx.DiGraph()
    G.add_node("A")
    G.add_node("B")
    
    path, cost = dijkstra(G, "A", "B")
    assert path is None
    assert cost == float('infinity')

def test_dijkstra_negative_weight():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=-1)
    
    with pytest.raises(ValueError, match="Dijkstra não suporta arestas com peso negativo."):
        dijkstra(G, "A", "B")

def test_bellman_ford_simple():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=4)
    G.add_edge("A", "C", weight=2)
    G.add_edge("B", "C", weight=1)
    G.add_edge("B", "D", weight=5)
    
    path, cost = bellman_ford(G, "A", "D")
    
    nx_cost, nx_path = nx.single_source_bellman_ford(G, "A", target="D")
    
    assert path == nx_path
    assert cost == nx_cost

def test_bellman_ford_negative_weights():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=10)
    G.add_edge("A", "C", weight=3)
    G.add_edge("C", "B", weight=-5)
    
    path, cost = bellman_ford(G, "A", "B")
    assert path == ["A", "C", "B"]
    assert cost == -2

def test_bellman_ford_negative_cycle():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=1)
    G.add_edge("B", "C", weight=-5)
    G.add_edge("C", "A", weight=1)
    
    with pytest.raises(ValueError, match="O grafo contém um ciclo negativo."):
        bellman_ford(G, "A", "C")

def test_bellman_ford_undirected_negative():
    G = nx.Graph()
    G.add_edge("A", "B", weight=-1)
    
    # Em grafo não-direcionado, uma aresta negativa é um ciclo negativo (A-B-A)
    with pytest.raises(ValueError, match="O grafo contém um ciclo negativo."):
        bellman_ford(G, "A", "B")

def test_compare_random_graphs():
    import random
    
    for _ in range(10):
        n = 10
        m = 20
        G = nx.gnm_random_graph(n, m, directed=True)
        for (u, v) in G.edges():
            G.edges[u,v]['weight'] = random.randint(1, 50)
            
        nodes = list(G.nodes())
        start = random.choice(nodes)
        end = random.choice(nodes)
        
        try:
            p_d, c_d = dijkstra(G, start, end)
            p_bf, c_bf = bellman_ford(G, start, end)
            
            nx_c, nx_p = nx.single_source_dijkstra(G, start, target=end)
            
            assert c_d == nx_c
            assert p_d == nx_p
            assert c_bf == nx_c
            assert p_bf == nx_p
        except nx.NetworkXNoPath:
            assert p_d is None
            assert c_d == float('infinity')
