import pytest
import networkx as nx
import sys
import os

from main4 import kosaraju_scc

def test_kosaraju_single_node():
    G = nx.DiGraph()
    G.add_node("A")
    sccs = kosaraju_scc(G)
    assert len(sccs) == 1
    assert sccs[0] == {"A"}

def test_kosaraju_simple_cycle():
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "A")])
    sccs = kosaraju_scc(G)
    assert len(sccs) == 1
    assert sccs[0] == {"A", "B", "C"}

def test_kosaraju_linear_graph():
    # A -> B -> C (três SCCs de um único nó cada)
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("B", "C")])
    sccs = kosaraju_scc(G)
    assert len(sccs) == 3
    # Cada nó deve estar em seu próprio conjunto
    found_nodes = [list(scc)[0] for scc in sccs]
    assert set(found_nodes) == {"A", "B", "C"}

def test_kosaraju_two_sccs():
    # A -> B -> C -> A (SCC 1)
    # C -> D (Aresta para outra componente)
    # D -> E -> F -> D (SCC 2)
    G = nx.DiGraph()
    G.add_edges_from([
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("C", "D"),
        ("D", "E"), ("E", "F"), ("F", "D")
    ])
    sccs = kosaraju_scc(G)
    assert len(sccs) == 2
    
    # Identifica cada SCC
    scc_sets = [set(s) for s in sccs]
    assert {"A", "B", "C"} in scc_sets
    assert {"D", "E", "F"} in scc_sets

def test_kosaraju_complex_graph():
    # Exemplo com várias SCCs
    G = nx.DiGraph()
    G.add_edges_from([
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("B", "D"), ("D", "E"), ("E", "F"), ("F", "D"),
        ("F", "G"), ("G", "H"), ("H", "G")
    ])
    sccs = kosaraju_scc(G)
    assert len(sccs) == 3
    
    scc_sets = [set(s) for s in sccs]
    assert {"A", "B", "C"} in scc_sets
    assert {"D", "E", "F"} in scc_sets
    assert {"G", "H"} in scc_sets

def test_compare_with_networkx():
    """Valida a implementação contra a função nativa do NetworkX."""
    # Gera um grafo aleatório direcionado
    G = nx.gnp_random_graph(20, 0.1, directed=True)
    
    # Implementação
    my_sccs = kosaraju_scc(G)
    
    # Implementação do NetworkX
    nx_sccs = list(nx.strongly_connected_components(G))
    
    # Ambos devem ter o mesmo número de SCCs
    assert len(my_sccs) == len(nx_sccs)
    
    # E os mesmos conjuntos de nós
    my_scc_sets = [frozenset(s) for s in my_sccs]
    nx_scc_sets = [frozenset(s) for s in nx_sccs]
    
    assert set(my_scc_sets) == set(nx_scc_sets)

def test_disconnected_graph():
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("B", "A")]) # SCC 1
    G.add_edges_from([("C", "D"), ("D", "C")]) # SCC 2 (desconexa da 1)
    sccs = kosaraju_scc(G)
    assert len(sccs) == 2
    scc_sets = [set(s) for s in sccs]
    assert {"A", "B"} in scc_sets
    assert {"C", "D"} in scc_sets

def test_invalid_input():
    with pytest.raises(ValueError, match="requer um dígrafo"):
        G = nx.Graph()
        G.add_edge(1, 2)
        kosaraju_scc(G)
