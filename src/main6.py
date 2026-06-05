import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from main import GraphService

class DisjointSet:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] == node:
            return node
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False

def kruskal_algorithm(graph):
    """
    Implementação manual do algoritmo de Kruskal para encontrar a MST.
    """
    # 1. Obter todas as arestas com seus pesos
    edges = []
    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1.0)
        edges.append((u, v, weight))
    
    # 2. Ordenar as arestas por peso
    edges.sort(key=lambda x: x[2])
    
    # 3. Inicializar DSU com todos os nós
    ds = DisjointSet(graph.nodes())
    
    mst_edges = []
    total_weight = 0
    
    # 4. Iterar sobre as arestas ordenadas
    for u, v, weight in edges:
        if ds.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
    return mst_edges, total_weight

def visualize_kruskal(graph, mst_edges, output_path="mst_result.png"):
    """
    Visualiza o grafo destacando a MST em azul com layout bem espaçado.
    """
    plt.figure(figsize=(14, 12))
    pos = nx.spring_layout(graph, k=2.5, iterations=100, seed=42)
    
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color='lightblue', alpha=0.9)
    nx.draw_networkx_labels(graph, pos, font_size=14, font_family='sans-serif', font_weight='bold')
    
    mst_set = set()
    for u, v, w in mst_edges:
        mst_set.add(tuple(sorted((u, v))))
        
    normal_edges = []
    blue_edges = []
    
    for u, v in graph.edges():
        if tuple(sorted((u, v))) in mst_set:
            blue_edges.append((u, v))
        else:
            normal_edges.append((u, v))
            
    nx.draw_networkx_edges(graph, pos, edgelist=normal_edges, edge_color='lightgray', width=1, style='dashed', alpha=0.4)
    
    nx.draw_networkx_edges(graph, pos, edgelist=blue_edges, edge_color='blue', width=5, alpha=1.0)
    
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(
        graph, pos, 
        edge_labels=edge_labels, 
        font_size=11, 
        label_pos=0.5,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0.2')
    )
    
    plt.title("Grafo com Árvore Geradora Mínima (Kruskal)")
    plt.axis('off')
    
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        gitignore_path = os.path.join(output_dir, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write("*.png\n*.jpg\n*.jpeg\n*.pdf\n")
    
    plt.savefig(output_path)
    print(f"Imagem salva em: {output_path}")
    plt.close()

def main():
    service = GraphService()
    
    # Solicitar entradas do usuário
    input_file = input("Informe o caminho do arquivo de grafo: ").strip()
    if not input_file:
        input_file = "grafo_exemplo.txt"
        
    output_image = input("Informe o nome do arquivo de imagem de saída (ex: mst.png): ").strip()
    if not output_image:
        output_image = "output/mst.png"

    if not os.path.exists(input_file):
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        return

    try:
        graph = service.load_from_file(input_file)
        
        if service.is_directed:
            print("Aviso: Kruskal é geralmente aplicado em grafos não-direcionados. Prosseguindo como grafo não-direcionado.")
            graph = graph.to_undirected()

        print(f"Processando grafo com {graph.number_of_nodes()} vértices e {graph.number_of_edges()} arestas.")
        
        mst_edges, total_weight = kruskal_algorithm(graph)
        
        print("\n--- Árvore Geradora Mínima (Kruskal Manual) ---")
        for u, v, w in mst_edges:
            print(f"Aresta: {u} - {v}, Peso: {w}")
        print(f"Custo total da MST: {total_weight}")
        
        # Validar com NetworkX
        nx_mst = nx.minimum_spanning_edges(graph, algorithm='kruskal', data=True)
        nx_weight = sum(d['weight'] for u, v, d in nx_mst)
        print(f"\nValidação NetworkX - Custo total: {nx_weight}")
        
        if abs(total_weight - nx_weight) < 1e-9:
            print("Sucesso! A implementação manual coincide com o resultado do NetworkX.")
        else:
            print("Atenção: Os pesos totais divergem. Verifique a implementação.")
            
        # visualizar
        visualize_kruskal(graph, mst_edges, output_image)
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
