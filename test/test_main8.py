import pytest
import networkx as nx
import os
from main8 import check_planarity_boyer_myrvold, visualize_planar_embedding
from main import GraphService

def create_temp_graph_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def test_planar_graph():
    # Grafo de um ciclo (C4) - Planar
    G = nx.cycle_graph(4)
    is_planar, result = check_planarity_boyer_myrvold(G)
    assert is_planar is True
    assert isinstance(result, nx.PlanarEmbedding)

def test_k5_non_planar():
    G = nx.complete_graph(5)
    is_planar, result = check_planarity_boyer_myrvold(G)
    assert is_planar is False
    # não planar, o resultado deve ser um subgrafo de Kuratowski
    # K5 contém a si mesmo como subgrafo de Kuratowski
    assert len(result.nodes()) == 5
    assert len(result.edges()) == 10

def test_k33_non_planar():
    G = nx.complete_bipartite_graph(3, 3)
    is_planar, result = check_planarity_boyer_myrvold(G)
    assert is_planar is False
    # K3,3 contém a si mesmo como subgrafo de Kuratowski
    assert len(result.nodes()) == 6
    assert len(result.edges()) == 9

def test_visualization_output():
    G = nx.path_graph(5)
    is_planar, embedding = check_planarity_boyer_myrvold(G)
    output_path = "test/output/test_planar_output.png"
    
    if is_planar:
        visualize_planar_embedding(G, embedding, output_path)
        assert os.path.exists(output_path)

def test_with_file_input():
    # criar um arquivo temporário de teste para K5
    test_file = "test/k5_test.txt"
    content = "G N\n0 1\n0 2\n0 3\n0 4\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4"
    create_temp_graph_file(test_file, content)
    
    service = GraphService()
    G = service.load_from_file(test_file)
    
    is_planar, result = check_planarity_boyer_myrvold(G)
    assert is_planar is False
    assert len(result.nodes()) == 5
    
    if os.path.exists(test_file):
        os.remove(test_file)

def test_validation_with_networkx_native():
    import random
    for _ in range(5):
        n = random.randint(3, 10)
        m = random.randint(n-1, n*(n-1)//2)
        G = nx.gnm_random_graph(n, m)
        
        is_planar_manual, _ = check_planarity_boyer_myrvold(G)
        is_planar_nx = nx.is_planar(G)
        
        assert is_planar_manual == is_planar_nx
