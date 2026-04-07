import pytest
import os
import networkx as nx
from main import GraphService

def test_load_undirected_unweighted():
    service = GraphService()
    service.load_from_file("grafo01.txt")
    
    assert isinstance(service.graph, nx.Graph)
    assert not isinstance(service.graph, nx.DiGraph)
    assert service.is_directed is False
    assert service.is_weighted is False
    assert "A" in service.graph
    assert "B" in service.graph
    assert service.graph.has_edge("A", "B")

def test_load_directed_weighted():
    service = GraphService()
    service.load_from_file("digrafo01.txt")
    
    assert isinstance(service.graph, nx.DiGraph)
    assert service.is_directed is True
    assert service.is_weighted is True
    assert "A" in service.graph
    assert service.graph["A"]["B"]["weight"] == 2.0

def test_add_vertex_and_edge():
    service = GraphService()
    service.graph = nx.Graph()
    service.is_weighted = True
    
    service.add_vertex("X")
    service.add_edge("X", "Y", weight=5.5)
    
    assert "X" in service.graph
    assert "Y" in service.graph
    assert service.graph["X"]["Y"]["weight"] == 5.5

def test_file_not_found():
    service = GraphService()
    with pytest.raises(FileNotFoundError):
        service.load_from_file("non_existent_file.txt")

def test_invalid_header():
    with open("invalid_test.txt", "w") as f:
        f.write("X Y\nA B\n")
    
    service = GraphService()
    with pytest.raises(ValueError, match="Invalid graph type 'X'"):
        service.load_from_file("invalid_test.txt")
    
    os.remove("invalid_test.txt")

def test_adjacency_matrix_undirected_unweighted():
    service = GraphService()
    service.load_from_file("grafo01.txt")
    nodes, matrix = service.get_adjacency_matrix()
    
    assert nodes == ["A", "B", "C", "D"]
    assert matrix[0] == [0, 1, 0, 1]
    assert matrix[1] == [1, 0, 1, 1]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            assert matrix[i][j] == matrix[j][i]

def test_adjacency_matrix_directed_weighted():
    service = GraphService()
    service.load_from_file("digrafo01.txt")
    nodes, matrix = service.get_adjacency_matrix()
    
    assert nodes == ["A", "B", "C", "D"]
    assert matrix[0] == [0.0, 2.0, 0.0, 0.0]
    assert matrix[1] == [0.0, 0.0, 1.0, 1.0]
    assert matrix[2] == [0.0, 0.0, 0.0, 3.0]
    assert matrix[3] == [2.0, 0.0, 0.0, 0.0]

def test_empty_graph_matrix():
    service = GraphService()
    nodes, matrix = service.get_adjacency_matrix()
    assert nodes == []
    assert matrix == []

def test_display_matrix_output():
    service = GraphService()
    print("\n--- Testing Adjacency Matrix Output (Undirected) ---")
    service.load_from_file("grafo01.txt")
    service.display_adjacency_matrix()
    
    print("\n--- Testing Adjacency Matrix Output (Directed Weighted) ---")
    service.load_from_file("digrafo01.txt")
    service.display_adjacency_matrix()

def test_compare_with_networkx():
    import numpy as np
    service = GraphService()
    
    service.load_from_file("grafo01.txt")
    nodes, manual_matrix = service.get_adjacency_matrix()
    nx_matrix = nx.to_numpy_array(service.graph, nodelist=nodes)
    np.testing.assert_array_almost_equal(np.array(manual_matrix), nx_matrix)

    service.load_from_file("digrafo01.txt")
    nodes, manual_matrix = service.get_adjacency_matrix()
    nx_matrix_w = nx.to_numpy_array(service.graph, nodelist=nodes, weight='weight')
    np.testing.assert_array_almost_equal(np.array(manual_matrix), nx_matrix_w)

def test_incidence_matrix_undirected():
    service = GraphService()
    service.load_from_file("grafo01.txt")
    nodes, edges, matrix = service.get_incidence_matrix()
    
    assert len(nodes) == 4
    assert len(edges) == 5
    for col in range(len(edges)):
        col_values = [matrix[row][col] for row in range(len(nodes))]
        assert sum(col_values) == 2.0

def test_incidence_matrix_directed_weighted():
    service = GraphService()
    service.load_from_file("digrafo01.txt")
    nodes, edges, matrix = service.get_incidence_matrix()
    
    for col in range(len(edges)):
        col_values = [matrix[row][col] for row in range(len(nodes))]
        non_zeros = [v for v in col_values if v != 0]
        assert len(non_zeros) == 2
        assert sum(non_zeros) == 0.0

def test_adjacency_list_unweighted():
    service = GraphService()
    service.load_from_file("grafo01.txt")
    adj = service.get_adjacency_list()
    assert adj["A"] == ["B", "D"]
    assert "C" in adj["B"]

def test_adjacency_list_weighted():
    service = GraphService()
    service.load_from_file("digrafo01.txt")
    adj = service.get_adjacency_list()
    assert ("B", 2.0) in adj["A"]

def test_weight_default_zero():
    service = GraphService()
    service.is_weighted = True
    service.graph = nx.Graph()
    service.add_vertex("A")
    service.add_vertex("B")
    service.add_edge("A", "B")
    
    nodes, matrix = service.get_adjacency_matrix()
    assert matrix[0][1] == 0.0
    
    adj = service.get_adjacency_list()
    assert adj["A"] == [("B", 0.0)]

def test_final_output_display():
    service = GraphService()
    print("\n--- FINAL TEST: UNDIRECTED ---")
    service.load_from_file("grafo01.txt")
    service.display_adjacency_matrix()
    service.display_incidence_matrix()
    service.display_adjacency_list()

    print("\n--- FINAL TEST: DIRECTED WEIGHTED ---")
    service.load_from_file("digrafo01.txt")
    service.display_adjacency_matrix()
    service.display_incidence_matrix()
    service.display_adjacency_list()
