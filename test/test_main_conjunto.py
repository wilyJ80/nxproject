import pytest
import networkx as nx
from main_conjunto import get_stable_set, get_clique, get_vertex_cover

def test_stable_set_heuristic():
    # Grafo simples: caminho A-B-C-D
    G = nx.Graph()
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
    
    stable_set = get_stable_set(G)
    
    # verifica se é um conjunto estável (nenhum par conectado)
    for u in stable_set:
        for v in stable_set:
            if u != v:
                assert not G.has_edge(u, v)

def test_clique_via_complement():
    G = nx.complete_graph(3)
    
    clique = get_clique(G)
    
    assert len(clique) == 3
    for u in clique:
        for v in clique:
            if u != v:
                assert G.has_edge(u, v)

def test_vertex_cover_complement():
    G = nx.Graph()
    G.add_edge('A', 'B')
    
    stable_set = get_stable_set(G)
    vertex_cover = get_vertex_cover(G, stable_set)
    
    # verifica se a união é o conjunto de vértices
    assert stable_set.union(vertex_cover) == set(G.nodes())
    # verifica se é uma cobertura de vértices
    for u, v in G.edges():
        assert u in vertex_cover or v in vertex_cover
