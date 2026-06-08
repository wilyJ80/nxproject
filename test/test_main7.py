import pytest
import networkx as nx
import os
import numpy as np
from main7 import hungarian_algorithm, solve_assignment, get_bipartite_sets, visualize_hungarian
from main import GraphService

def test_hungarian_algorithm_matrix():
    cost_matrix = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    # Esperado: 
    # (0, 1) -> 1
    # (1, 0) -> 2
    # (2, 2) -> 2
    # Total = 5
    
    assignment = hungarian_algorithm(cost_matrix)
    total_cost = sum(cost_matrix[i][assignment[i]] for i in range(len(assignment)))
    assert total_cost == 5

def test_hungarian_simple_graph():
    G = nx.Graph()
    G.add_edge("1", "4", weight=10)
    G.add_edge("1", "5", weight=19)
    G.add_edge("1", "6", weight=8)
    G.add_edge("2", "4", weight=10)
    G.add_edge("2", "5", weight=18)
    G.add_edge("2", "6", weight=7)
    G.add_edge("3", "4", weight=13)
    G.add_edge("3", "5", weight=22)
    G.add_edge("3", "6", weight=3)
    
    matching_edges, total_cost = solve_assignment(G)
    
    # Validação NetworkX
    u_set, _ = get_bipartite_sets(G)
    nx_matching = nx.bipartite.matching.minimum_weight_full_matching(G, top_nodes=u_set)
    nx_total_cost = sum(G[u][v]['weight'] for u, v in nx_matching.items()) / 2
    
    assert abs(total_cost - nx_total_cost) < 1e-9

def test_hungarian_real_file():
    service = GraphService()
    test_file = "test/hungarian_test_input.txt"
    
    assert os.path.exists(test_file)
    
    graph = service.load_from_file(test_file)
    matching_edges, total_cost = solve_assignment(graph)
    
    # Validação NetworkX
    u_set, _ = get_bipartite_sets(graph)
    nx_matching = nx.bipartite.matching.minimum_weight_full_matching(graph, top_nodes=u_set)
    nx_total_cost = sum(graph[u][v]['weight'] for u, v in nx_matching.items()) / 2
    
    assert abs(total_cost - nx_total_cost) < 1e-9
    
    # Test visualization
    output_img = "test/output/test_hungarian.png"
    visualize_hungarian(graph, matching_edges, output_img)
    assert os.path.exists(output_img)

def test_compare_with_networkx_random_bipartite():
    import random
    for _ in range(3):
        n = 5
        m = 10
        # grafo bipartido aleatório
        G = nx.bipartite.random_graph(n, n, 0.7)
        # nó com pelo menos uma aresta
        for u in range(n):
            if G.degree(u) == 0:
                G.add_edge(u, n + random.randint(0, n-1))
        for v in range(n, 2*n):
            if G.degree(v) == 0:
                G.add_edge(random.randint(0, n-1), v)
                
        for (u, v) in G.edges():
            G.edges[u,v]['weight'] = random.randint(1, 100)
            
        try:
            matching_edges, total_cost = solve_assignment(G)
            u_set, _ = get_bipartite_sets(G)
            nx_matching = nx.bipartite.matching.minimum_weight_full_matching(G, top_nodes=u_set)
            nx_total_cost = sum(G[u][v]['weight'] for u, v in nx_matching.items()) / 2
            assert abs(total_cost - nx_total_cost) < 1e-9
        except ValueError:
            continue
