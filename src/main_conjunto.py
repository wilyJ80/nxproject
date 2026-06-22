import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from main import GraphService

def get_stable_set(graph):
    g = graph.copy()
    stable_set = set()
    
    while g.nodes():
        # vértice com grau mínimo
        node = min(g.degree, key=lambda x: x[1])[0]
        stable_set.add(node)
        
        # remover o vértice e seus vizinhos
        neighbors = list(g.neighbors(node))
        g.remove_node(node)
        g.remove_nodes_from(neighbors)
        
    return stable_set

def get_clique(graph):
    complement_graph = nx.complement(graph)
    return get_stable_set(complement_graph)

def get_vertex_cover(graph, stable_set):
    return set(graph.nodes()) - stable_set

def plot_graph(graph, nodes_subset, filename, color, highlight_edges=None):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    
    # desenha todos os nós
    all_nodes = list(graph.nodes())
    node_colors = [color if node in nodes_subset else 'grey' for node in all_nodes]
    nx.draw_networkx_nodes(graph, pos, nodelist=all_nodes, node_color=node_colors)
    nx.draw_networkx_labels(graph, pos)
    
    # desenhar arestas
    if highlight_edges:
        nx.draw_networkx_edges(graph, pos, edgelist=highlight_edges, edge_color=color, width=2)
        other_edges = [edge for edge in graph.edges() if edge not in highlight_edges and (edge[1], edge[0]) not in highlight_edges]
        nx.draw_networkx_edges(graph, pos, edgelist=other_edges, edge_color='grey')
    else:
        nx.draw_networkx_edges(graph, pos, edge_color='grey')
    plt.savefig(filename)
    plt.close()
    print(f"Imagem salva: {filename}")

def main():
    if len(sys.argv) < 3:
        print("Uso: uv run src/main_conjunto.py <arquivo_grafo> <prefixo_saida>")
        return

    input_file = sys.argv[1]
    output_prefix = sys.argv[2]
    
    service = GraphService()
    try:
        graph = service.load_from_file(input_file)
    except Exception as e:
        print(f"Erro ao carregar grafo: {e}")
        return

    stable_set = get_stable_set(graph)
    clique = get_clique(graph)
    vertex_cover = get_vertex_cover(graph, stable_set)
    
    plot_graph(graph, stable_set, f"{output_prefix}_conjunto_estavel.png", 'green')
    
    clique_graph = graph.subgraph(clique)
    plot_graph(graph, clique, f"{output_prefix}_clique.png", 'red', highlight_edges=list(clique_graph.edges()))
    
    plot_graph(graph, vertex_cover, f"{output_prefix}_cobertura.png", 'blue')

if __name__ == "__main__":
    main()
